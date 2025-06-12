import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import yt_dlp

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Send me a video link and I'll download it.")

def download_video(update: Update, context: CallbackContext):
    url = update.message.text.strip()
    update.message.reply_text("Downloading... Please wait.")
    try:
        ydl_opts = {'outtmpl': 'video.%(ext)s', 'format': 'best'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir():
            if file.startswith("video."):
                with open(file, 'rb') as vid:
                    update.message.reply_video(vid)
                os.remove(file)
    except Exception as e:
        update.message.reply_text(f"Error: {e}")

def main():
    TOKEN = os.environ.get("8137272336:AAGhhrLvQvFOf0Gl3EKaROIbCwdEbAEy6Zk")
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, download_video))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
