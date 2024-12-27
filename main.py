‏import logging
‏from aiogram import Bot, Dispatcher, types
‏from aiogram.utils import executor
‏import yt_dlp
‏import os
‏from flask import Flask
‏from threading import Thread

# إعدادات البوت
‏API_TOKEN = "7613632266:AAF_ixgcRdl_jvzY8dY_aODz4RkD3576meY"

# إعداد تسجيل الأخطاء
‏logging.basicConfig(level=logging.INFO)

# إنشاء البوت والموزع
‏bot = Bot(token=API_TOKEN)
‏dp = Dispatcher(bot)

# إعداد Flask للحفاظ على النشاط
‏app = Flask('')

‏@app.route('/')
‏def home():
‏    return "البوت يعمل الآن بشكل دائم!"

‏def run():
‏    app.run(host='0.0.0.0', port=8080)

‏def keep_alive():
‏    t = Thread(target=run)
‏    t.start()

# مسار التخزين المؤقت
‏DOWNLOAD_PATH = "downloads"

# التحقق من وجود مجلد التنزيل
‏if not os.path.exists(DOWNLOAD_PATH):
‏    os.makedirs(DOWNLOAD_PATH)

# إعداد yt-dlp
‏ydl_opts = {
‏    'outtmpl': f'{DOWNLOAD_PATH}/%(title)s.%(ext)s',
‏    'format': 'best',
‏    'quiet': True,
‏    'no_warnings': True,
}

# أوامر البدء
‏@dp.message_handler(commands=['start', 'help'])
‏async def send_welcome(message: types.Message):
‏    await message.reply(
        "👋 مرحبًا! أرسل لي رابط فيديو من YouTube, Twitter, أو Instagram وسأقوم بتنزيله لك.\n"
        "إذا كنت تريد تحويل الفيديو إلى صوت، أرسل الرابط بصيغة: audio:<الرابط>"
    )

# التعامل مع الروابط
‏@dp.message_handler()
‏async def download_video(message: types.Message):
‏    url = message.text.strip()

    # التحقق من وجود كلمة "audio:" لتحويل الفيديو إلى صوت
‏    is_audio = url.startswith("audio:")
‏    if is_audio:
‏        url = url.replace("audio:", "").strip()

‏    await message.reply("⏳ جاري معالجة الرابط، انتظر قليلاً...")

‏    try:
        # تحميل الفيديو أو الصوت باستخدام yt-dlp
‏        options = ydl_opts.copy()
‏        if is_audio:
‏            options['format'] = 'bestaudio'
‏            options['postprocessors'] = [{
‏                'key': 'FFmpegExtractAudio',
‏                'preferredcodec': 'mp3',
‏                'preferredquality': '192',
            }]

‏        with yt_dlp.YoutubeDL(options) as ydl:
‏            info_dict = ydl.extract_info(url, download=True)
‏            file_path = ydl.prepare_filename(info_dict)

        # إرسال الملف إلى المستخدم
‏        with open(file_path, 'rb') as file:
‏            if is_audio:
‏                await bot.send_audio(message.chat.id, file, caption="🎵 تم تحويل الفيديو إلى صوت!")
‏            else:
‏                await bot.send_video(message.chat.id, file, caption="🎥 تم تحميل الفيديو بنجاح!")

        # حذف الملف بعد الإرسال
‏        os.remove(file_path)

‏    except yt_dlp.utils.DownloadError as e:
‏        await message.reply(f"❌ خطأ أثناء التنزيل: {str(e)}")
‏    except Exception as e:
‏        await message.reply(f"⚠️ حدث خطأ غير متوقع: {str(e)}")

# تشغيل البوت
‏if __name__ == '__main__':
‏    while True:  # الحفاظ على البوت يعمل بشكل مستمر
‏        try:
‏            keep_alive()  # تشغيل Flask للحفاظ على النشاط
‏            executor.start_polling(dp, skip_updates=True)
‏        except Exception as e:
‏            logging.error(f"⚠️ حدث خطأ أثناء تشغيل البوت: {str(e)}. إعادة التشغيل...")
