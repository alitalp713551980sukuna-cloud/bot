import telebot
from telebot import types

# --- الإعدادات الأساسية ---
TOKEN = '8382035555:AAEyKqioQySc5HNLSJ3Nw6rDh89p3RpRDPY'
ADMIN_ID = 6709215417  # الايدي الخاص بك للتحكم والمراقبة
CHANNEL_ID = "@HACKER_SUKUNA"
CHANNEL_URL = "https://t.me/HACKER_SUKUNA"

bot = telebot.TeleBot(TOKEN)

# قائمة المستخدمين المسموح لهم (مؤقتة في الرام)
allowed_users = set()

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
    markup.add(types.KeyboardButton("ادوات اضافية") )
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    
    # 1. التحقق من الاشتراك الإجباري
    if not check_sub(user_id):
        bot.reply_to(message, f"⚠️ عذراً! يجب عليك الاشتراك في قناة البوت أولاً لتستطيع استخدامه:\n{CHANNEL_URL}")
        return

    # 2. نظام الموافقة (يستثنى منه المطور)
    if user_id not in allowed_users and user_id != ADMIN_ID:
        bot.send_message(ADMIN_ID, f"🔔 طلب انضمام جديد:\nالاسم: {message.from_user.first_name}\nاليوزر: @{message.from_user.username}\nالايدي: `{user_id}`\nللموافقة أرسل: `/approve {user_id}`", parse_mode="Markdown")
        bot.reply_to(message, "⏳ تم إرسال طلبك للمطور. انتظر الموافقة لتتمكن من استخدام الأدوات.")
        return

    bot.send_message(message.chat.id, "مرحباً بك في أدوات SUKUNA، اختر الأداة المطلوبة:", reply_markup=main_markup())

@bot.message_handler(commands=['approve'])
def approve(message):
    if message.from_user.id == ADMIN_ID:
        try:
            target_id = int(message.text.split()[1])
            allowed_users.add(target_id)
            bot.send_message(target_id, "✅ تمت الموافقة على طلبك! يمكنك الآن استخدام البوت بالكامل.")
            bot.reply_to(message, f"تم تفعيل المستخدم {target_id} بنجاح.")
        except:
            bot.reply_to(message, "استخدم الأمر هكذا: /approve ايدي_المستخدم")

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    user_id = message.from_user.id
    text = message.text

    # منع غير المشتركين أو غير الموافق عليهم من رؤية المحتوى
    if not check_sub(user_id) or (user_id not in allowed_users and user_id != ADMIN_ID):
        return

    # نظام مراقبة المستخدمين (يصل للمطور فقط)
    if user_id != ADMIN_ID:
        bot.send_message(ADMIN_ID, f"👀 المستخدم @{message.from_user.username} ضغط على: {text}")

    # --- ردود الأزرار ---
    if text == "ادوات اضافية":
        bot.reply_to(message, "سيتم اضافتاء عما قريب.")
    
    elif text in ["🎧تسجيل صوت", "📱معلومات IP"]:
        bot.reply_to(message, "سيتم اضافتهن قريبا.")

    elif text == "بوتات ارقام وهمية":
        bot.reply_to(message, "بوتات ارقام وهمية مجانيه☠️\n\n1 @TricksMastarNumberFile2_bot\n\n2 @IPRN_SMS_Bot\nhttps://t.me/+oqfPz2T5kvRhYmZl\n\n3 @Seven1tel_Number_Bot\nhttps://t.me/+y8rz92BPGcFjNGU1\n\nأشترك بقناة البوت وحمل الملف واشترك بالقنوات المرتبطة.")

    elif text == "حضر أرقام واتساب":
        # (يتم وضع النص الكامل لطريقة حظر الأرقام الذي أرسلته هنا)
        bot.reply_to(message, "تم إرسال شرح حظر الأرقام بالكامل.. راجع المصدر: @HACKER_SUKUNA")

    elif text == "سحب أرقام يمن مبايل":
        bot.reply_to(message, "🔴 طريقة سحب ارقام يمن موبايل 🔴\n\nإقناع الضحية بالاتصال بالرمز: (*72 + رقمك)")

    elif text == "حماية الوتس🛡":
        bot.reply_to(message, "حماية الواتس من الاختراق 💎\n\nقم بتفعيل التحقق بخطوتين من الإعدادات.")

    elif text == "سحب ارقام وتساب":
        bot.send_message(message.chat.id, "سحب أرقام واتساب 📞\nاستخدم حساب واتساب أعمال باسم فريق الدعم..")

bot.infinity_polling()
