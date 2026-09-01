```python
import logging
import os

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


URL_AMAZON = "https://music.amazon.es/podcasts/6e78231a-cc7b-4d40-b7c5-57e22a7eb69d/255-podcast"
URL_SPOTIFY = "https://open.spotify.com/show/1u6QrtoKrEZYmto2Et803R"
URL_YOUTUBE = "https://www.youtube.com/playlist?list=PLPZXQokR3S9FQuucjHH2Yg7DN_4jEY8dU"
URL_IVOOX = "https://go.ivoox.com/sq/3164442"
URL_APPLE = "https://podcasts.apple.com/ci/podcast/255-podcast/id1896825324"
URL_RSS = "https://255podcast.molinaig.es/feed.xml"


async def amazon(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(URL_AMAZON)


async def spotify(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(URL_SPOTIFY)


async def youtube(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(URL_YOUTUBE)


async def ivoox(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(URL_IVOOX)


async def apple(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(URL_APPLE)


async def rss(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(URL_RSS)


def main() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not token:
        raise RuntimeError(
            "No se ha definido la variable de entorno TELEGRAM_BOT_TOKEN"
        )

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("amazon", amazon))
    application.add_handler(CommandHandler("spotify", spotify))
    application.add_handler(CommandHandler("youtube", youtube))
    application.add_handler(CommandHandler("ivoox", ivoox))
    application.add_handler(CommandHandler("apple", apple))
    application.add_handler(CommandHandler("rss", rss))

    logger.info("Bot de 255 Podcast iniciado. Esperando mensajes...")

    application.run_polling()


if __name__ == "__main__":
    main()
```

