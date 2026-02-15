import os
import telebot
import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis
from flask import Flask
from threading import Thread

# 1. خادم ويب بسيط جداً لضمان عمل Render
app = Flask(__name__)
@app.route('/')
def home(): return "SUKUNA IS ALIVE"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

Thread(target=run, daemon=True).start()

# 2. إعداد البوت
TOKEN = '8382035555:AAEyKqioQySc5HNLSJ3Nw6rDh89p3RpRDPY'
bot = telebot.TeleBot(TOKEN)
target_face = None

# 3. تحميل نموذج خفيف جداً (لتجنب نفاد الذاكرة Out of Memory)
# قمنا بتصغير حجم det_size لتقليل استهلاك الرام
face_app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
face_app.prepare(ctx_id=0, det_size=(320, 320)) 

# تحميل موديل التبديل
if not os.path.exists('inswapper_128.onnx'):
    os.system("wget https://huggingface.co/ezioruan/inswapper_128.onnx/resolve/main/inswapper_128.onnx -O inswapper_128.onnx")
swapper = insightface.model_zoo.get_model('inswapper_128.onnx', download=False)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "✅ سكونا يعمل الآن بنجاح!\nأرسل صورة الوجه أولاً.")

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
                bot.reply_to(message, "👤 تم حفظ الوجه. أرسل الصورة المراد تعديلها.")
            else:
                bot.reply_to(message, "لم أجد وجهاً.")
        else:
            res = img.copy()
            for face in faces:
                res = swapper.get(res, face, target_face, paste_back=True)
            _, enc = cv2.imencode('.jpg', res)
            bot.send_photo(message.chat.id, enc.tobytes(), caption="🔥 تم بواسطة سكونا")
    except Exception as e:
        bot.reply_to(message, f"خطأ بسيط: {e}")

if __name__ == "__main__":
    bot.polling(none_stop=True)
