```python
import asyncio
import logging
import os

import uvicorn

from quart import Quart, request, Response
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


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


async def amazon(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    await update.message.reply_text(URL_AMAZON)


async def spotify(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    await update.message.reply_text(URL_SPOTIFY)


async def youtube(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    await update.message.reply_text(URL_YOUTUBE)


async def ivoox(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    await update.message.reply_text(URL_IVOOX)


async def apple(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    await update.message.reply_text(URL_APPLE)


async def rss(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    await update.message.reply_text(URL_RSS)


async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:

    mensaje = (
        "🎙 Comandos disponibles de 255 Podcast\n\n"
        "/amazon - Escuchar en Amazon Music\n"
        "/spotify - Escuchar en Spotify\n"
        "/youtube - Escuchar en YouTube\n"
        "/ivoox - Escuchar en iVoox\n"
        "/apple - Escuchar en Apple Podcasts\n"
        "/rss - Obtener el feed RSS del podcast\n"
        "/help - Mostrar esta ayuda"
    )

    await update.message.reply_text(mensaje)


if not TOKEN:
    raise RuntimeError("Falta TELEGRAM_BOT_TOKEN")

if not WEBHOOK_URL:
    raise RuntimeError("Falta WEBHOOK_URL")


telegram_app = (
    Application.builder()
    .token(TOKEN)
    .updater(None)
    .build()
)


telegram_app.add_handler(
    CommandHandler("amazon", amazon)
)

telegram_app.add_handler(
    CommandHandler("spotify", spotify)
)

telegram_app.add_handler(
    CommandHandler("youtube", youtube)
)

telegram_app.add_handler(
    CommandHandler("ivoox", ivoox)
)

telegram_app.add_handler(
    CommandHandler("apple", apple)
)

telegram_app.add_handler(
    CommandHandler("rss", rss)
)

telegram_app.add_handler(
    CommandHandler("help", help_command)
)


web_app = Quart(__name__)


@web_app.get("/")
async def home():
    return "255 Podcast Bot funcionando", 200


@web_app.get("/health")
async def health():
    return "OK", 200


@web_app.post("/telegram")
async def telegram_webhook():

    data = await request.get_json()

    update = Update.de_json(
        data=data,
        bot=telegram_app.bot
    )

    await telegram_app.update_queue.put(update)

    return Response(status=200)


async def main():

    webhook_url = (
        f"{WEBHOOK_URL.rstrip('/')}/telegram"
    )

    await telegram_app.bot.set_webhook(
        url=webhook_url,
        allowed_updates=Update.ALL_TYPES
    )

    logger.info(
        "Webhook configurado en: %s",
        webhook_url
    )

    server = uvicorn.Server(
        uvicorn.Config(
            app=web_app,
            host="0.0.0.0",
            port=PORT,
            log_level="info"
        )
    )

    async with telegram_app:

        await telegram_app.start()

        logger.info("Bot iniciado")
        logger.info("Puerto: %s", PORT)

        await server.serve()

        await telegram_app.stop()


if __name__ == "__main__":
    asyncio.run(main())
```
