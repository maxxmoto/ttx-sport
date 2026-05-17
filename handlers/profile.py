from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import aiosqlite
from keyboards import main_menu

router = Router()

class EditProfile(StatesGroup):
    waiting_level = State()
    waiting_style = State()
    waiting_grip = State()
    waiting_strong = State()
    waiting_weak = State()
    waiting_rating = State()
    waiting_goal = State()

@router.message(F.text == "⚙️ Профиль")
async def profile_menu(message: types.Message):
    async with aiosqlite.connect("spinbox.db") as db:
        async with db.execute(
            "SELECT level, style, grip, strong_sides, weak_sides, rating, goal FROM users WHERE user_id=?",
            (message.from_user.id,)
        ) as cursor:
            user = await cursor.fetchone()
    if user:
        text = "👤 <b>Ваш профиль</b>\n"
        if user[0]: text += f"Уровень: {user[0]}\n"
        if user[1]: text += f"Стиль: {user[1]}\n"
        if user[2]: text += f"Хватка: {user[2]}\n"
        if user[3]: text += f"Сильные стороны: {user[3]}\n"
        if user[4]: text += f"Слабые стороны: {user[4]}\n"
        if user[5]: text += f"Рейтинг: {user[5]}\n"
        if user[6]: text += f"Цель: {user[6]}\n"
    else:
        text = "Профиль пока пуст."
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="✏️ Заполнить/редактировать", callback_data="edit_profile")]
    ])
    await message.answer(text, parse_mode="HTML", reply_markup=kb)

@router.callback_query(F.data == "edit_profile")
async def start_edit(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Введите ваш уровень (или /skip):")
    await state.set_state(EditProfile.waiting_level)

@router.message(EditProfile.waiting_level)
async def level_edit(message: types.Message, state: FSMContext):
    if message.text != "/skip":
        await state.update_data(level=message.text)
    await message.answer("Стиль игры (или /skip):")
    await state.set_state(EditProfile.waiting_style)

@router.message(EditProfile.waiting_style)
async def style_edit(message: types.Message, state: FSMContext):
    if message.text != "/skip":
        await state.update_data(style=message.text)
    await message.answer("Хватка:")
    await state.set_state(EditProfile.waiting_grip)

@router.message(EditProfile.waiting_grip)
async def grip_edit(message: types.Message, state: FSMContext):
    if message.text != "/skip":
        await state.update_data(grip=message.text)
    await message.answer("Сильные стороны:")
    await state.set_state(EditProfile.waiting_strong)

@router.message(EditProfile.waiting_strong)
async def strong_edit(message: types.Message, state: FSMContext):
    if message.text != "/skip":
        await state.update_data(strong=message.text)
    await message.answer("Слабые стороны:")
    await state.set_state(EditProfile.waiting_weak)

@router.message(EditProfile.waiting_weak)
async def weak_edit(message: types.Message, state: FSMContext):
    if message.text != "/skip":
        await state.update_data(weak=message.text)
    await message.answer("Рейтинг (число):")
    await state.set_state(EditProfile.waiting_rating)

@router.message(EditProfile.waiting_rating)
async def rating_edit(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(rating=int(message.text))
    await message.answer("Цель на сезон (или /skip):")
    await state.set_state(EditProfile.waiting_goal)

@router.message(EditProfile.waiting_goal)
async def goal_edit(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if message.text != "/skip":
        data["goal"] = message.text
    else:
        data["goal"] = None
    # Сохраняем в БД
    async with aiosqlite.connect("spinbox.db") as db:
        await db.execute(
            "INSERT OR REPLACE INTO users (user_id, username, level, style, grip, strong_sides, weak_sides, rating, goal) VALUES (?,?,?,?,?,?,?,?,?)",
            (message.from_user.id, message.from_user.username, data.get("level"), data.get("style"),
             data.get("grip"), data.get("strong"), data.get("weak"), data.get("rating"), data.get("goal"))
        )
        await db.commit()
    await message.answer("✅ Профиль обновлён!", reply_markup=main_menu)
    await state.clear()