import os
import telegram
import datetime
import pytz
from telegram.ext import Updater
from telegram.ext import CommandHandler

telegram_bot_token = "#token#"

updater = Updater(token=telegram_bot_token, use_context=True)
dispatcher = updater.dispatcher

def send_photo(context):
   chat_id = context.job.context
   context.bot.send_photo(chat_id = chat_id, photo=open('C:/Users/mkozi/Desktop/daily_motywator/photos/1.png', 'rb'))

def daily_job(update, context):
    """ Running on Mon, Tue, Wed, Thu, Fri = tuple(range(5)) """
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text='Setting a daily notifications!')
    t = datetime.time(hour=11, minute=00, tzinfo=pytz.timezone('Europe/Warsaw'))
    context.job_queue.run_daily(send_photo, t, days=tuple(range(5)), context=update.message.chat_id)

dispatcher.add_handler(CommandHandler("daily", daily_job, pass_job_queue=True))
updater.start_polling()