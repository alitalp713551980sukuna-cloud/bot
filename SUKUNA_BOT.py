import telebot
from telebot import types

# --- الإعدادات الأساسية ---
TOKEN = '8382035555:AAEyKqioQySc5HNLSJ3Nw6rDh89p3RpRDPY'
CHANNEL_ID = "@HACKER_SUKUNA"
CHANNEL_URL = "https://t.me/HACKER_SUKUNA"

bot = telebot.TeleBot(TOKEN)

# دالة التحقق من الاشتراك في القناة
def check_sub(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
        return False
    except:
        return False

# --- لوحة التحكم الرئيسية ---
def main_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("بوتات ارقام وهمية"), types.KeyboardButton("حضر أرقام واتساب"))
    markup.add(types.KeyboardButton("سحب أرقام يمن مبايل"), types.KeyboardButton("حماية الوتس🛡"))
    markup.add(types.KeyboardButton("سحب ارقام وتساب"))
    markup.add(types.KeyboardButton("🎧تسجيل صوت"), types.KeyboardButton("📱معلومات IP"))
    markup.add(types.KeyboardButton("ادوات اضافية"))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    
    # التحقق من الاشتراك الإجباري فقط
    if not check_sub(user_id):
        bot.reply_to(message, f"⚠️ عذراً! يجب عليك الاشتراك في قناة البوت أولاً لتستطيع استخدامه:\n{CHANNEL_URL}")
        return

    # الدخول المباشر بعد الاشتراك
    bot.send_message(message.chat.id, "مرحباً بك في أدوات SUKUNA، اختر الأداة المطلوبة:", reply_markup=main_markup())

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    user_id = message.from_user.id
    text = message.text

    # منع غير المشتركين من رؤية المحتوى
    if not check_sub(user_id):
        return

    # --- ردود الأزرار ---
    if text == "ادوات اضافية":
        bot.reply_to(message, "سيتم اضافتاء عما قريب.")
    
    elif text in ["🎧تسجيل صوت", "📱معلومات IP"]:
        bot.reply_to(message, "سيتم اضافتهن قريبا.")

    elif text == "بوتات ارقام وهمية":
        msg = ("بوتات ارقام وهمية مجانيه☠️\n\n"
               "1 @TricksMastarNumberFile2_bot\n\n"
               "2 @IPRN_SMS_Bot\nhttps://t.me/+oqfPz2T5kvRhYmZl\n\n"
               "3 @Seven1tel_Number_Bot\nhttps://t.me/+y8rz92BPGcFjNGU1\n\n"
               "أشترك بقناة البوت وحمل الملف واشترك بالقنوات المرتبطة.")
        bot.reply_to(message, msg)

    elif text == "حضر أرقام واتساب":
        msg = ("*طريقة تهكير وتطيير إي رقم حقيقي أو وهمي في الواتساب*\n\n"
               "الطريقة مجربة ومضمونه👍🏽💯\n\n"
               "1⃣ قم بحرق كود التحقق للضحية بإدخال أكواد خاطئة متكررة.\n"
               "2⃣ انتظر حتى تظهر رسالة (خمنت الكود عدة مرات) وتظهر مدة الـ 12 ساعة.\n"
               "3⃣ راسل فريق دعم واتساب (Support@Whatsapp.com) واطلب تعطيل الحساب بسبب فقدان الشريحة.\n"
               "المصدر : @HACKER_SUKUNA")
        bot.reply_to(message, msg)

    elif text == "سحب أرقام يمن مبايل":
        msg = ("🔴 طريقة سحب ارقام يمن موبايل 🔴\n\n"
               "إقناع الضحية بالاتصال بالرمز: (*72 + رقمك)\n"
               "بمجرد الاتصال، ستتحول جميع مكالماته إليك وتستطيع سحب كود الواتساب عبر خيار (الاتصال بي).")
        bot.reply_to(message, msg)

    elif text == "حماية الوتس🛡":
        msg = ("حماية الواتس من الاختراق 💎\n\n"
               "1- الإعدادات > الخصوصية والأمان.\n"
               "2- تفعيل (التحقق بخطوتين).\n"
               "3- وضع كلمة سر وبريد إلكتروني.")
        bot.reply_to(message, msg)

    elif text == "سحب ارقام وتساب":
        bot.send_message(message.chat.id, "سحب أرقام واتساب 📞\n\nاستخدم واتساب أعمال وقم بتغيير الاسم والصورة لفريق دعم واتساب الرسمي، ثم اطلب الكود من الضحية بحجة تأمين حسابه.")
        bot.send_message(message.chat.id, "مود سحب الارقام ☠️\nالبريد: whatsapp.com@gmail.com\nالموقع: https://www.whatsapp.com/")

bot.infinity_polling()
