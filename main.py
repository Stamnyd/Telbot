from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests

# إعداد التوكنات
TELEGRAM_TOKEN = 'توكن_البوت_الخاص_بك'
DEEPSEEK_API_KEY = 'مفتاح_API_الخاص_بـ_DeepSeek'
DEEPSEEK_API_URL = 'رابط_API_الخاص_بـ_DeepSeek'  # مثال: https://api.deepseek.com/v1/chat

# دالة لمعالجة الأمر /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text('مرحبًا! أنا بوت يعتمد على DeepSeek. كيف يمكنني مساعدتك؟')

# دالة لمعالجة الرسائل النصية
def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text

    # إرسال الرسالة إلى DeepSeek API
    headers = {
        'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'prompt': user_message,
        'max_tokens': 150  # يمكنك تعديل هذا حسب الحاجة
    }

    response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)

    if response.status_code == 200:
        # إرسال الرد إلى المستخدم
        bot_response = response.json().get('choices', [{}])[0].get('text', 'عذرًا، لم أتمكن من فهم ذلك.')
        update.message.reply_text(bot_response)
    else:
        update.message.reply_text('عذرًا، حدث خطأ أثناء الاتصال بـ DeepSeek.')

def main():
    # إنشاء Updater وإضافة التوكن
    updater = Updater(TELEGRAM_TOKEN)

    # الحصول على Dispatcher للتسجيل
    dp = updater.dispatcher

    # تسجيل الدوال
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # بدء البوت
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()