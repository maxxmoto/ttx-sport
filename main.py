import asyncio
import logging
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config import BOT_TOKEN
from database import init_db
from services.racket_selector import load_rackets
from services.statistics import check_wear
from handlers import start, training, opponents, test_racket, equipment, profile

logging.basicConfig(level=logging.INFO)

async def main():
    await init_db()
    load_rackets()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(training.router)
    dp.include_router(opponents.router)
    dp.include_router(test_racket.router)
    dp.include_router(equipment.router)
    dp.include_router(profile.router)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_wear, 'cron', hour=12, args=(bot,))
    scheduler.start()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())