from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import aiosqlite
from datetime import datetime
from keyboards import main_menu

router = Router()

class AddTraining(StatesGroup):
    waiting_datetime = State()
    waiting_duration = State()
    waiting_type = State()
    waiting_notes = State()
    waiting_racket = State()

@router.message(F.text == "🎯 Тренировка")
async def training_start(message: types.Message, state: FSMContext):
    await message.answer("Введите дату и время тренировки в формате ГГГГ-ММ-ДД ЧЧ:ММ\nИли напишите «сейчас» для текущего момента:")
    await state.set_state(AddTraining.waiting_datetime)

@router.message(AddTraining.waiting_datetime)
async def process_datetime(message: types.Message, state: FSMContext):
    text = message.text.strip().lower()
    if text == "сейчас" or text == "now":
        dt = datetime.now().strftime("%Y-%m-%d %H:%M")
    else:
        dt = text
    await state.update_data(datetime=dt)
    await message.answer("Длительность тренировки (минут):")
    await state.set_state(AddTraining.waiting_duration)

@router.message(AddTraining.waiting_duration)
async def process_duration(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Введите число минут.")
        return
    await state.update_data(duration_minutes=int(message.text))
    # Кнопки выбора типа тренировки
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🏓 Общая (игра на счёт)")],
            [KeyboardButton(text="🔄 Отработка подач")],
            [KeyboardButton(text="🎾 Тренировка с тренером")],
            [KeyboardButton(text="💪 ОФП/имитация")],
            [KeyboardButton(text="🧠 Теория/анализ")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("Тип тренировки:", reply_markup=kb)
    await state.set_state(AddTraining.waiting_type)

@router.message(AddTraining.waiting_type)
async def process_type(message: types.Message, state: FSMContext):
    valid_types = ["🏓 Общая (игра на счёт)", "🔄 Отработка подач", "🎾 Тренировка с тренером", "💪 ОФП/имитация", "🧠 Теория/анализ"]
    if message.text not in valid_types:
        await message.answer("Выберите тип из меню.")
        return
    await state.update_data(type=message.text)
    await message.answer("Заметки (или нажмите /skip):", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AddTraining.waiting_notes)

@router.message(AddTraining.waiting_notes)
async def process_notes(message: types.Message, state: FSMContext):
    if message.text == "/skip":
        notes = ""
    else:
        notes = message.text
    await state.update_data(notes=notes)
    # Подбор ракетки
    async with aiosqlite.connect("spinbox.db") as db:
        async with db.execute(
            "SELECT id, base, fh_rubber, bh_rubber FROM my_equipment WHERE user_id=? AND active=1",
            (message.from_user.id,)
        ) as cursor:
            rackets = await cursor.fetchall()
    if not rackets:
        await message.answer("Нет сохранённой экипировки. Пропускаем.", reply_markup=main_menu)
        racket_id = None
        await save_training(message, state, racket_id)
        return
    kb = types.InlineKeyboardMarkup(inline_keyboard=[])
    for r in rackets:
        kb.inline_keyboard.append([types.InlineKeyboardButton(
            text=f"{r[1]} + {r[2]}/{r[3]}",
            callback_data=f"racket_{r[0]}"
        )])
    await message.answer("Выберите используемую ракетку:", reply_markup=kb)
    await state.set_state(AddTraining.waiting_racket)

async def save_training(message: types.Message, state: FSMContext, racket_id=None):
    data = await state.get_data()
    async with aiosqlite.connect("spinbox.db") as db:
        await db.execute(
            "INSERT INTO trainings (user_id, datetime, duration_minutes, type, notes, racket_id) VALUES (?,?,?,?,?,?)",
            (message.from_user.id, data["datetime"], data["duration_minutes"], data["type"], data["notes"], racket_id)
        )
        await db.commit()
    await message.answer("✅ Тренировка сохранена!", reply_markup=main_menu)
    await state.clear()

@router.callback_query(F.data.startswith("racket_"))
async def racket_chosen(callback: types.CallbackQuery, state: FSMContext):
    racket_id = int(callback.data.split("_")[1])
    await callback.answer()
    # Удалить инлайн-клавиатуру
    await callback.message.edit_reply_markup(reply_markup=None)
    await save_training(callback.message, state, racket_id)

# Журнал тренировок
@router.message(F.text == "📋 Журнал")
async def show_journal(message: types.Message):
    async with aiosqlite.connect("spinbox.db") as db:
        async with db.execute(
            "SELECT datetime, duration_minutes, type, notes FROM trainings WHERE user_id=? ORDER BY datetime DESC LIMIT 10",
            (message.from_user.id,)
        ) as cursor:
            rows = await cursor.fetchall()
    if not rows:
        await message.answer("Записей пока нет.")
        return
    text = "📋 <b>Последние тренировки:</b>\n\n"
    for r in rows:
        text += f"📅 {r[0]} | ⏱ {r[1]} мин | {r[2]}\n{r[3]}\n\n"
    await message.answer(text, parse_mode="HTML")