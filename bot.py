import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from services.iris_api import iris
from services.telethon_client import telethon_client
from handlers import balance, history, send_sweets, send_gold, pocket_settings, pocket_permissions

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_routers(
    balance.router,
    history.router,
    send_sweets.router,
    send_gold.router,
    pocket_settings.router,
    pocket_permissions.router,
)


async def main():
    logger.info("Бот запускается...")
    await telethon_client.start()
    await dp.start_polling(bot)
    await iris.close()
    await telethon_client.stop()
    logger.info("Бот остановлен.")


if __name__ == "__main__":
    asyncio.run(main())
