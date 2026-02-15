import os
import telebot
import insightface
from insightface.app import FaceAnalysis
import cv2
import numpy as np
# التعديل النهائي لحل مشكلة السجل: حذف .editor تماماً
try:
    from moviepy import VideoFileClip, AudioFileClip, ImageSequenceClip
except ImportError:
    from moviepy.editor import VideoFileClip, AudioFileClip, ImageSequenceClip

from flask import Flask
from threading import Thread

# --- 1. خادم ويب صغير (إلزامي لـ Render) ---
app = Flask(__name__)
@app.route('/')
def home(): return "SUKUNA IS ONLINE"

def run_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# تشغيل السيرفر في الخلفية
Thread(target=run_server, daemon=True).start()

# --- 2. تحميل الموديل تلقائياً ---
if not os.path.exists('inswapper_128.onnx'):
    os.system("wget https://huggingface.co/ezioruan/inswapper_128.onnx/resolve/main/inswapper_128.onnx -O inswapper_128.onnx")

# --- 3. إعدادات البوت والذكاء الاصطناعي ---
TOKEN = '8382035555:AAEyKqioQySc5HNLSJ3Nw6rDh89p3RpRDPY'
bot = telebot.TeleBot(TOKEN)
target_face = None

# إعداد المحرك للعمل على الـ CPU
face_app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
face_app.prepare(ctx_id=0, det_size=(640, 640))
swapper = insightface.model_zoo.get_model('inswapper_128.onnx', download=False)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "نظام SUKUNA جاهز.\nأرسل صورة الوجه أولاً.")

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
            bot.reply_to(message, "✅ تم حفظ الوجه الهدف. أرسل الآن الصورة/الفيديو.")
        elif target_face:
            res = img.copy()
            for face in faces:
                res = swapper.get(res, face, target_face, paste_back=True)
            _, enc = cv2.imencode('.jpg', res)
            bot.send_photo(message.chat.id, enc.tobytes(), caption="🔥 تم التنفيذ")
    except Exception as e:
        bot.reply_to(message, f"خطأ: {e}")

if __name__ == "__main__":
    print("البوت بدأ العمل فعلياً...")
    bot.polling(none_stop=True)
