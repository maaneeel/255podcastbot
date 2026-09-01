import asyncio
import logging
import os

from flask import Flask, request
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.getenv("PORT", "10000"))


URL_AMAZON = "https://music.amazon.es/podcasts/6e78231a-cc7b-4d40-b7c5-57e22a7eb69d/255-podcast"
URL_SPOTIFY = "https://open.spotify.com/show/1u6QrtoKrEZYmto2Et803R"
URL_YOUTUBE = "https://www.youtube.com/playlist?list=PLPZXQokR3S9FQuucjHH2Yg7DN_4jEY8dU"
URL_IVOOX = "https://go.ivoox.com/sq/3164442"
URL_APPLE = "https://podcasts.apple.com/ci/podcast/255-podcast/id1896825324"
URL_RSS = "https://255podcast.molinaig.es/feed.xml"


async def amazon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(URL_AMAZON)


async def spotify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(URL_SPOTIFY)


async def youtube(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(URL_YOUTUBE)


async def ivoox(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(URL_IVOOX)


async def apple(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(URL_APPLE)


async def rss(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(URL_RSS)


if not TOKEN:
    raise RuntimeError("Falta TELEGRAM_BOT_TOKEN")

if not WEBHOOK_URL:
    raise RuntimeError("Falta WEBHOOK_URL")


application = (
    Application.builder()
    .token(TOKEN)
    .updater(None)
    .build()
)


application.add_handler(CommandHandler("amazon", amazon))
application.add_handler(CommandHandler("spotify", spotify))
application.add_handler(CommandHandler("youtube", youtube))
application.add_handler(CommandHandler("ivoox", ivoox))
application.add_handler(CommandHandler("apple", apple))
application.add_handler(CommandHandler("rss", rss))


app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return "255 Podcast Bot OK", 200


@app.route("/health", methods=["GET"])
def health():
    return "OK", 200


@app.route("/telegram", methods=["POST"])
def telegram_webhook():
    update = Update.de_json(
        request.get_json(force=True),
        application.bot
    )

    asyncio.run(
        application.update_queue.put(update)
    )

    return "OK", 200


async def iniciar_bot():
    await application.initialize()
    await application.start()

    webhook = f"{WEBHOOK_URL}/telegram"

    await application.bot.set_webhook(
        url=webhook
    )

    logger.info("Webhook configurado: %s", webhook)


if __name__ == "__main__":
    asyncio.run(iniciar_bot())

    app.run(
        host="0.0.0.0",
        port=PORT
    )
