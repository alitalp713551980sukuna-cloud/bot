import os
import telebot
import insightface
from insightface.app import FaceAnalysis
import cv2
import numpy as np
# تم تحديث السطر التالي ليناسب النسخة الجديدة المثبتة على Render
from moviepy import VideoFileClip, AudioFileClip, ImageSequenceClip
from flask import Flask
from threading import Thread

# --- 1. خادم الويب لضمان عمل Render ---
app = Flask(__name__)
@app.route('/')
def home(): return "SUKUNA IS ACTIVE"

def run_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_server)
    t.daemon = True
    t.start()

# --- 2. تحميل الموديل تلقائياً ---
if not os.path.exists('inswapper_128.onnx'):
    os.system("wget https://huggingface.co/ezioruan/inswapper_128.onnx/resolve/main/inswapper_128.onnx -O inswapper_128.onnx")

# --- 3. إعدادات البوت والذكاء الاصطناعي ---
TOKEN = '8382035555:AAEyKqioQySc5HNLSJ3Nw6rDh89p3RpRDPY'
bot = telebot.TeleBot(TOKEN)
target_face = None

face_app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
face_app.prepare(ctx_id=0, det_size=(640, 640))
المبادلة = insightface.model_zoo.get_model('inswapper_128.onnx', download=False)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "نظام SUKUNA جاهز.\nارسل صورة الوجه اولاً.")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    global target_face
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded = bot.download_file(file_info.file_path)
        img = cv2.imdecode(np.frombuffer(downloaded, np.uint8), cv2.IMREAD_COLOR)
        faces = face_app.get(img)
        if not target_face:
            if faces:
                target_face = faces[0]
                bot.reply_to(message, "✅ تم حفظ الوجه. ارسل الصورة او الفيديو الان.")
            else:
                bot.reply_to(message, "❌ لم اجد وجهاً.")
        else:
            res = img.copy()
            for face in faces:
                res = المبادلة.get(res, face, target_face, paste_back=True)
            _, enc = cv2.imencode('.jpg', res)
            bot.send_photo(message.chat.id, enc.tobytes(), caption="تم التنفيذ")
    except Exception as e:
        bot.reply_to(message, f"خطأ: {e}")

@bot.message_handler(content_types=['video'])
def handle_video(message):
    global target_face
    if not target_face:
        bot.reply_to(message, "⚠️ ارسل صورة الوجه اولاً!")
        return
    bot.reply_to(message, "⚙️ جاري معالجة الفيديو...")
    try:
        file_info = bot.get_file(message.video.file_id)
        downloaded = bot.download_file(file_info.file_path)
        with open("input_v.mp4", "wb") as f: f.write(downloaded)
        
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
            video.audio.write_audiofile("temp.mp3", logger=None)
            new_video = new_video.set_audio(AudioFileClip("temp.mp3"))
        
        new_video.write_videofile("out.mp4", codec="libx264", audio_codec="aac", logger=None)
        with open("out.mp4", "rb") as v:
            bot.send_video(message.chat.id, v, caption="✅ تم بنجاح")
    except Exception as e:
        bot.reply_to(message, f"فشل: {e}")

if __name__ == "__main__":
    keep_alive()
    bot.polling(none_stop=True)
