import os
import logging
from fetch_news import fetch_news
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler 
import datetime
import pytz

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
count = 0
subscribe = False
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE, count = 0):
    count +=1
    logging.info('User Number: '+ str(count) + ' - ' + update.effective_user.first_name)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello "+ update.effective_user.first_name + ", thanks for subscribing! What time would you like to receive news?")
    await set_schedule(update, context)

async def end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global subscribe
    subscribe = False
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sure, I will stop sending news!")

async def set_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sure, I will send you your news daily!")
    context.job_queue.run_daily(get_news, time= datetime.time(hour=8, minute=0, tzinfo=pytz.timezone('Asia/Singapore')),chat_id=update.message.chat_id)



async def get_news(context: ContextTypes.DEFAULT_TYPE):
    print("fetching news now")
    top_news = fetch_news()
    await context.bot.send_message(chat_id=context.job.chat_id, text=top_news)


if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_API_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('end', end))
    application.add_handler(CommandHandler('schedule', set_schedule))

    application.run_polling()
