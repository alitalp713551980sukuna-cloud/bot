import requests
import time
import json

# التوكن الخاص بك
TOKEN = "8382035555:AAEyKqioQySc5HNLSJ3Nw6rDh89p3RpRDPY"
URL = f"https://api.telegram.org/bot{TOKEN}/"

def send_welcome_with_buttons(chat_id):
    # إنشاء الأزرار
    keyboard = {
        "inline_keyboard": [
            [{"text": "📸 اختراق الكاميرا", "callback_data": "cam"}, {"text": "📍 اختراق الموقع", "callback_data": "loc"}],
            [{"text": "🛠 أدوات إضافية", "callback_data": "tools"}],
            [{"text": "🆘 المساعدة", "callback_data": "help"}]
        ]
    }
    
    text = "🚀 أهلاً بك في لوحة التحكم! اختر الخدمة التي تريدها من الأسفل:"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "reply_markup": json.dumps(keyboard)
    }
    requests.post(URL + "sendMessage", data=payload)

def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += f"&offset={offset}"
    return requests.get(url).json()

print("البوت يعمل الآن... أرسل /start لتجربة الأزرار")
last_update_id = None

while True:
    updates = get_updates(last_update_id)
    if "result" in updates and updates["result"]:
        for update in updates["result"]:
            last_update_id = update["update_id"] + 1
            
            # التعامل مع رسالة البداية
            if "message" in update:
                chat_id = update["message"]["chat"]["id"]
                text = update["message"].get("text", "")
                if text == "/start":
                    send_welcome_with_buttons(chat_id)
            
            # التعامل مع ضغطات الأزرار
            elif "callback_query" in update:
                chat_id = update["callback_query"]["message"]["chat"]["id"]
                data = update["callback_query"]["data"]
                
                if data == "cam":
                    requests.post(URL + "sendMessage", data={"chat_id": chat_id, "text": "قريباً سأعطيك رابط الكاميرا الخاص بك!"})
                elif data == "help":
                    requests.post(URL + "sendMessage", data={"chat_id": chat_id, "text": "هذا البوت مخصص للتجارب التعليمية."})

    time.sleep(1)
