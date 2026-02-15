import os
import telebot
import insightface
from insightface.app import FaceAnalysis
import cv2
import numpy as np
# تصحيح الاستدعاء ليتوافق مع تحديثات Render الجديدة
from moviepy import VideoFileClip, AudioFileClip, ImageSequenceClip
from flask import Flask
from threading import Thread

# --- 1. خادم ويب صغير (إلزامي لمنصة Render) ---
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

# --- 2. تحميل موديل التبديل تلقائياً ---
if not os.path.exists('inswapper_128.onnx'):
    os.system("wget https://huggingface.co/ezioruan/inswapper_128.onnx/resolve/main/inswapper_128.onnx -O inswapper_128.onnx")

# --- 3. إعدادات البوت والذكاء الاصطناعي ---
TOKEN = '8382035555:AAEyKqioQySc5HNLSJ3Nw6rDh89p3RpRDPY'
bot = telebot.TeleBot(TOKEN)
target_face = None

face_app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
face_app.prepare(ctx_id=0, det_size=(640, 640))
swapper = insightface.model_zoo.get_model('inswapper_128.onnx', download=False)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "نظام SUKUNA جاهز.\nأرسل صورة الوجه (Target) أولاً.")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    global target_face
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded = bot.download_file(file_info.file_path)
        img = cv2.imdecode(np.frombuffer(downloaded, np.uint8), cv2.IMREAD_COLOR)
        faces = face_app.get(img)
        if not target_face and faces:
            target_face = faces[0]
            bot.reply_to(message, "✅ تم حفظ الوجه الهدف. الآن أرسل الصورة أو الفيديو المراد تبديله.")
        elif target_face:
            res = img.copy()
            for face in faces:
                res = swapper.get(res, face, target_face, paste_back=True)
            _, enc = cv2.imencode('.jpg', res)
            bot.send_photo(message.chat.id, enc.tobytes(), caption="🔥 تم التنفيذ بواسطة SUKUNA")
    except Exception as e:
        bot.reply_to(message, f"⚠️ خطأ: {e}")

# استمر في استخدام نفس المنطق للفيديو مع حذف .editor
@bot.message_handler(content_types=['video'])
def handle_video(message):
    bot.reply_to(message, "⚙️ جاري معالجة الفيديو... قد يستغرق هذا بضع دقائق على السيرفر المجاني.")
    # (كود معالجة الفيديو الخاص بك مع التأكد من استخدام الاستدعاء الجديد)

if __name__ == "__main__":
    keep_alive() # تشغيل السيرفر لضمان حالة Live
    print("البوت بدأ العمل...")
    bot.polling(none_stop=True)
