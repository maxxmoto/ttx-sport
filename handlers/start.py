from aiogram import Router, types
from aiogram.filters import Command
from keyboards import main_menu

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "🏓 Привет! Я SpinBox — твой персональный ассистент для настольного тенниса.\n"
        "Я помогу подобрать ракетку, вести учёт тренировок и изучать соперников.",
        reply_markup=main_menu
    )