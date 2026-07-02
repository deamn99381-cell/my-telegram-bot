import telebot
import yt_dlp
import os

# ==== التوكن الخاص ببوت مصطفى طه ====
BOT_TOKEN = "8867029282:AAHNg8hGKgalqkjotPWVvTnsFZ28qIHn8I4"

bot = telebot.TeleBot(BOT_TOKEN)

DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(
        message,
        "أهلاً بك في بوت مصطفى للتحميل السريع! 🚀\nأرسل لي رابط فيديو من يوتيوب أو تيك توك وسأقوم بتحميله لك فوراً."
    )

@bot.message_handler(func=lambda message: True)
def handle_link(message):
    url = message.text.strip()

    if not url.startswith("http"):
        bot.reply_to(message, "من فضلك أرسل رابطاً صحيحاً.")
        return

    processing_msg = bot.reply_to(message, "⏳ جاري معالجة الرابط وتحميل الفيديو بسيرفر طيارة...")

    output_template = os.path.join(DOWNLOAD_FOLDER, f"{message.chat.id}_%(id)s.%(ext)s")

    # إعدادات معدلة للعمل على السيرفرات مباشرة وبأقل استهلاك
    ydl_opts = {
        'format': 'b',  # يجلب أفضل صيغة مدموجة وجاهزة مباشرة
        'outtmpl': output_template,
        'quiet': True,
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

        with open(file_path, 'rb') as video_file:
            bot.send_video(message.chat.id, video_file, caption="✅ تم التحميل بنجاح بواسطة بوت مصطفى")

        os.remove(file_path)

    except Exception as e:
        bot.reply_to(message, f"❌ حدث خطأ أثناء التحميل:\n{str(e)}")

    finally:
        try:
            bot.delete_message(message.chat.id, processing_msg.message_id)
        except:
            pass

if __name__ == "__main__":
    print("البوت السحابي يعمل الآن...")
    bot.infinity_polling()