import os
import telegram
import datetime
import pytz
from telegram.ext import Updater
from telegram.ext import CommandHandler

telegram_bot_token = "#token"
directory_in_str = 'E:/Repos/tst1/'

updater = Updater(token=telegram_bot_token, use_context=True)
dispatcher = updater.dispatcher
daily_flag = 1

def daily_job(update, context):
    """ Running on Mon, Tue, Wed, Thu, Fri = tuple(range(5)) """
    global daily_flag
    if daily_flag == 1:
        daily_flag = 0
        chat_id = update.effective_chat.id
        context.bot.send_message(chat_id=chat_id, text='Setting a daily motywator!')
        context.job_queue.run_repeating(send_photo, interval=30, first=1, context=update.message.chat_id)

        #t = datetime.time(hour=12, minute=45, tzinfo=pytz.timezone('Europe/Warsaw'))
        #context.job_queue.run_daily(send_photo, t, days=tuple(range(5)), context=update.message.chat_id)


def send_photo(context):
    chat_id = context.job.context
    fnames = os.listdir(directory_in_str)
    fjpeg = list(filter(lambda k: 'jpg' in k, fnames))
    photo_name = fjpeg[0]
    caption_file_path = directory_in_str + os.path.splitext(photo_name)[0] + '.txt'
    caption_string = open(caption_file_path, 'r', encoding="utf-8").read()
    clean_caption_string = caption_string[:caption_string.find('\n➡️')]
    photo_path = directory_in_str + photo_name
    context.bot.send_photo(chat_id=chat_id, photo=open(photo_path, 'rb'), caption=clean_caption_string)
    os.remove(photo_path)
    os.remove(caption_file_path)


dispatcher.add_handler(CommandHandler("daily", daily_job, pass_job_queue=True))
updater.start_polling()