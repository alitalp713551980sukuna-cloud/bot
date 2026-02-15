import os
import telebot
import insightface
from insightface.app import FaceAnalysis
import cv2
import numpy as np
# التعديل الذهبي: حذفنا .editor ليتوافق مع تحديث السيرفر
from moviepy import VideoFileClip, AudioFileClip, ImageSequenceClip
from flask import Flask
from threading import Thread

# تشغيل سيرفر وهمي لإبقاء Render سعيداً
app = Flask(__name__)
@app.route('/')
def home(): return "SUKUNA IS LIVE"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# تشغيل السيرفر في الخلفية
if not os.environ.get("KEEP_ALIVE_STARTED"):
    Thread(target=run, daemon=True).start()
    os.environ["KEEP_ALIVE_STARTED"] = "true"

# إعدادات البوت الأساسية
TOKEN = '8382035555:AAEyKqioQySc5HNLSJ3Nw6rDh89p3RpRDPY'
bot = telebot.TeleBot(TOKEN)
target_face = None

# تحميل الموديلات (CPU)
face_app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
face_app.prepare(ctx_id=0, det_size=(640, 640))
swapper = insightface.model_zoo.get_model('inswapper_128.onnx', download=False) if os.path.exists('inswapper_128.onnx') else None

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "نظام سكونا جاهز. أرسل صورة الوجه الهدف أولاً.")

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
            bot.reply_to(message, "✅ تم حفظ الوجه. أرسل الآن الصورة/الفيديو المراد تبديله.")
        elif target_face:
            res = img.copy()
            for face in faces:
                res = swapper.get(res, face, target_face, paste_back=True)
            _, enc = cv2.imencode('.jpg', res)
            bot.send_photo(message.chat.id, enc.tobytes(), caption="🔥 تم التنفيذ")
    except Exception as e:
        bot.reply_to(message, f"خطأ: {e}")

# (يمكنك إضافة معالجة الفيديو هنا لاحقاً بنفس الطريقة)

if __name__ == "__main__":
    print("جاري تشغيل سكونا...")
    bot.polling(none_stop=True)
