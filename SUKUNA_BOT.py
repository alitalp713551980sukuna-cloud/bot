import os
import telebot
import insightface
from insightface.app import FaceAnalysis
import cv2
import numpy as np
# تصحيح الاستدعاء هنا (حذفنا .editor ليتوافق مع النسخة الجديدة)
from moviepy import VideoFileClip, AudioFileClip, ImageSequenceClip
from flask import Flask
from threading import Thread

# --- 1. خادم ويب صغير (لإرضاء منصة Render ومنع التوقف) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "SUKUNA BOT IS ONLINE"

def run_server():
    # Render يفرض فتح منفذ (Port) وإلا سيغلق البوت
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_server)
    t.daemon = True
    t.start()

# --- 2. تحميل موديل التبديل تلقائياً إذا لم يكن موجوداً ---
if not os.path.exists('inswapper_128.onnx'):
    print("جاري تحميل الموديل الثقيل... انتظر قليلاً")
    os.system("wget https://huggingface.co/ezioruan/inswapper_128.onnx/resolve/main/inswapper_128.onnx -O inswapper_128.onnx")

# --- 3. إعدادات البوت والذكاء الاصطناعي ---
TOKEN = '8382035555:AAEyKqioQySc5HNLSJ3Nw6rDh89p3RpRDPY'
bot = telebot.TeleBot(TOKEN)
target_face = None

# إعداد محرك تحليل الوجوه (استخدام CPU ليتناسب مع خطة Render المجانية)
face_app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
face_app.prepare(ctx_id=0, det_size=(640, 640))
المبادلة = insightface.model_zoo.get_model('inswapper_128.onnx', download=False)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "مرحباً بك في نظام SUKUNA.\n1. أرسل صورة الوجه (Target).\n2. ثم أرسل الصورة أو الفيديو المراد تبديله.")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    global target_face
    bot.reply_to(message, "جاري معالجة الصورة...")
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded = bot.download_file(file_info.file_path)
        img = cv2.imdecode(np.frombuffer(downloaded, np.uint8), cv2.IMREAD_COLOR)
        faces = face_app.get(img)
        
        if not target_face:
            if faces:
                target_face = faces[0]
                bot.reply_to(message, "✅ تم حفظ الوجه الهدف. الآن أرسل المادة المراد تنفيذ التبديل عليها.")
            else:
                bot.reply_to(message, "❌ لم يتم العثور على وجه واضح.")
        else:
            res = img.copy()
            for face in faces:
                res = المبادلة.get(res, face, target_face, paste_back=True)
            _, enc = cv2.imencode('.jpg', res)
            bot.send_photo(message.chat.id, enc.tobytes(), caption="🔥 تم التنفيذ بواسطة SUKUNA")
    except Exception as e:
        bot.reply_to(message, f"⚠️ خطأ: {e}")

@bot.message_handler(content_types=['video'])
def handle_video(message):
    global target_face
    if not target_face:
        bot.reply_to(message, "⚠️ أرسل صورة الوجه أولاً!")
        return
    
    bot.reply_to(message, "⚙️ جاري معالجة الفيديو... قد يستغرق وقتاً طويلاً.")
    try:
        file_info = bot.get_file(message.video.file_id)
        downloaded = bot.download_file(file_info.file_path)
        with open("input_v.mp4", "wb") as f:
            f.write(downloaded)
        
        video = VideoFileClip("input_v.mp4")
        frames = []
        
        for frame in video.iter_frames():
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            faces = face_app.get(frame_bgr)
            res_frame = frame_bgr.copy()
            for face in faces:
                res_frame = المبادلة.get(res_frame, face, target_face, paste_back=True)
            frames.append(cv2.cvtColor(res_frame, cv2.COLOR_BGR2RGB))
        
        new_video = ImageSequenceClip(frames, fps=video.fps)
        if video.audio:
            video.audio.write_audiofile("temp_a.mp3", logger=None)
            new_video = new_video.set_audio(AudioFileClip("temp_a.mp3"))
        
        new_video.write_videofile("out.mp4", codec="libx264", audio_codec="aac", logger=None)
        
        with open("out.mp4", "rb") as v:
            bot.send_video(message.chat.id, v, caption="✅ تم تبديل الفيديو بنجاح.")
            
    except Exception as e:
        bot.reply_to(message, f"❌ فشل المعالجة: {e}")

if __name__ == "__main__":
    keep_alive() 
    print("البوت شغال الآن...")
    bot.polling(none_stop=True)
