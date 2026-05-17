from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import aiosqlite
from keyboards import main_menu, skip_kb

router = Router()

# Состояния создания соперника
class CreateOpponent(StatesGroup):
    waiting_name = State()
    waiting_level = State()
    waiting_style = State()
    waiting_grip = State()
    waiting_hand = State()
    waiting_base = State()
    waiting_fh = State()
    waiting_bh = State()
    waiting_special = State()
    waiting_speed = State()
    waiting_serve = State()
    waiting_receive = State()
    waiting_spin = State()
    waiting_fh_game = State()
    waiting_bh_game = State()
    waiting_footwork = State()
    waiting_psychology = State()
    waiting_tactical = State()

@router.message(F.text == "🃏 Соперники")
async def opponents_menu(message: types.Message):
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="➕ Новый соперник", callback_data="new_opponent")],
        [types.InlineKeyboardButton(text="📋 Список соперников", callback_data="list_opponents")]
    ])
    await message.answer("Управление соперниками:", reply_markup=kb)

@router.callback_query(F.data == "new_opponent")
async def new_opponent(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Введите имя/ник соперника:")
    await state.set_state(CreateOpponent.waiting_name)

# Универсальная функция для обработки полей с возможностью пропуска
async def ask_optional_field(message: types.Message, state: FSMContext, next_state: State, prompt: str, field_name: str):
    if message.text == "/skip":
        await state.update_data({field_name: None})
        await message.answer(prompt, reply_markup=skip_kb)
        await state.set_state(next_state)
    else:
        await state.update_data({field_name: message.text})
        await message.answer(prompt, reply_markup=skip_kb)
        await state.set_state(next_state)

@router.message(CreateOpponent.waiting_name)
async def name_entered(message: types.Message, state: FSMContext):
    if not message.text.strip():
        await message.answer("Имя не может быть пустым.")
        return
    await state.update_data(name=message.text.strip())
    await message.answer("Уровень (например: новичок, любитель, КМС, МС). Или нажмите /skip:", reply_markup=skip_kb)
    await state.set_state(CreateOpponent.waiting_level)

@router.message(CreateOpponent.waiting_level)
async def level_entered(message: types.Message, state: FSMContext):
    await ask_optional_field(message, state, CreateOpponent.waiting_style, "Стиль игры (атакующий, защитник, универсал и т.п.). /skip:", "level")

@router.message(CreateOpponent.waiting_style)
async def style_entered(message: types.Message, state: FSMContext):
    await ask_optional_field(message, state, CreateOpponent.waiting_grip, "Хватка (европейская, азиатская). /skip:", "style")

@router.message(CreateOpponent.waiting_grip)
async def grip_entered(message: types.Message, state: FSMContext):
    await ask_optional_field(message, state, CreateOpponent.waiting_hand, "Основная рука (левая/правая). /skip:", "grip")

@router.message(CreateOpponent.waiting_hand)
async def hand_entered(message: types.Message, state: FSMContext):
    await ask_optional_field(message, state, CreateOpponent.waiting_base, "Основание ракетки соперника. /skip:", "hand")

@router.message(CreateOpponent.waiting_base)
async def base_entered(message: types.Message, state: FSMContext):
    await ask_optional_field(message, state, CreateOpponent.waiting_fh, "Накладка на форхенд. /skip:", "base")

@router.message(CreateOpponent.waiting_fh)
async def fh_entered(message: types.Message, state: FSMContext):
    await ask_optional_field(message, state, CreateOpponent.waiting_bh, "Накладка на бэкхенд. /skip:", "fh_rubber")

@router.message(CreateOpponent.waiting_bh)
async def bh_entered(message: types.Message, state: FSMContext):
    await ask_optional_field(message, state, CreateOpponent.waiting_special, "Шипы/антиспин и сторона (если есть). /skip:", "bh_rubber")

@router.message(CreateOpponent.waiting_special)
async def special_entered(message: types.Message, state: FSMContext):
    await ask_optional_field(message, state, CreateOpponent.waiting_speed, "Оценка скорости атаки (1-5). /skip:", "special_rubber")

@router.message(CreateOpponent.waiting_speed)
async def speed_entered(message: types.Message, state: FSMContext):
    # Можно преобразовать в int
    val = message.text if message.text != "/skip" else None
    if val and not val.isdigit():
        await message.answer("Введите число или /skip")
        return
    await state.update_data(speed_attack=int(val) if val else None)
    await message.answer("Сила подач (1-5). /skip:", reply_markup=skip_kb)
    await state.set_state(CreateOpponent.waiting_serve)

@router.message(CreateOpponent.waiting_serve)
async def serve_entered(message: types.Message, state: FSMContext):
    val = message.text if message.text != "/skip" else None
    if val and not val.isdigit():
        await message.answer("Введите число или /skip")
        return
    await state.update_data(serve_strength=int(val) if val else None)
    await message.answer("Приём подач (1-5). /skip:", reply_markup=skip_kb)
    await state.set_state(CreateOpponent.waiting_receive)

@router.message(CreateOpponent.waiting_receive)
async def receive_entered(message: types.Message, state: FSMContext):
    val = message.text if message.text != "/skip" else None
    if val and not val.isdigit():
        await message.answer("Введите число или /skip")
        return
    await state.update_data(receive=int(val) if val else None)
    await message.answer("Вращение топ-спина (1-5). /skip:", reply_markup=skip_kb)
    await state.set_state(CreateOpponent.waiting_spin)

@router.message(CreateOpponent.waiting_spin)
async def spin_entered(message: types.Message, state: FSMContext):
    val = message.text if message.text != "/skip" else None
    if val and not val.isdigit():
        await message.answer("Введите число или /skip")
        return
    await state.update_data(topspin_spin=int(val) if val else None)
    await message.answer("Игра справа (1-5). /skip:", reply_markup=skip_kb)
    await state.set_state(CreateOpponent.waiting_fh_game)

@router.message(CreateOpponent.waiting_fh_game)
async def fh_game_entered(message: types.Message, state: FSMContext):
    val = message.text if message.text != "/skip" else None
    if val and not val.isdigit():
        await message.answer("Введите число или /skip")
        return
    await state.update_data(fh_game=int(val) if val else None)
    await message.answer("Игра слева (1-5). /skip:", reply_markup=skip_kb)
    await state.set_state(CreateOpponent.waiting_bh_game)

@router.message(CreateOpponent.waiting_bh_game)
async def bh_game_entered(message: types.Message, state: FSMContext):
    val = message.text if message.text != "/skip" else None
    if val and not val.isdigit():
        await message.answer("Введите число или /skip")
        return
    await state.update_data(bh_game=int(val) if val else None)
    await message.answer("Движение ног (1-5). /skip:", reply_markup=skip_kb)
    await state.set_state(CreateOpponent.waiting_footwork)

@router.message(CreateOpponent.waiting_footwork)
async def footwork_entered(message: types.Message, state: FSMContext):
    val = message.text if message.text != "/skip" else None
    if val and not val.isdigit():
        await message.answer("Введите число или /skip")
        return
    await state.update_data(footwork=int(val) if val else None)
    await message.answer("Психология (стабильность, эмоции). Текст или /skip:", reply_markup=skip_kb)
    await state.set_state(CreateOpponent.waiting_psychology)

@router.message(CreateOpponent.waiting_psychology)
async def psychology_entered(message: types.Message, state: FSMContext):
    if message.text == "/skip":
        await state.update_data(psychology=None)
    else:
        await state.update_data(psychology=message.text)
    await message.answer("Тактические заметки (слабые/сильные стороны, как играть). Текст или /skip:", reply_markup=skip_kb)
    await state.set_state(CreateOpponent.waiting_tactical)

@router.message(CreateOpponent.waiting_tactical)
async def tactical_entered(message: types.Message, state: FSMContext):
    if message.text == "/skip":
        tactical = None
    else:
        tactical = message.text
    data = await state.get_data()
    async with aiosqlite.connect("spinbox.db") as db:
        await db.execute('''
            INSERT INTO opponents (user_id, name, level, style, grip, hand, base, fh_rubber, bh_rubber, special_rubber,
                                  speed_attack, serve_strength, receive, topspin_spin, fh_game, bh_game, footwork,
                                  psychology, tactical_notes)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ''', (
            message.from_user.id,
            data["name"],
            data.get("level"),
            data.get("style"),
            data.get("grip"),
            data.get("hand"),
            data.get("base"),
            data.get("fh_rubber"),
            data.get("bh_rubber"),
            data.get("special_rubber"),
            data.get("speed_attack"),
            data.get("serve_strength"),
            data.get("receive"),
            data.get("topspin_spin"),
            data.get("fh_game"),
            data.get("bh_game"),
            data.get("footwork"),
            data.get("psychology"),
            tactical
        ))
        await db.commit()
    await message.answer("✅ Соперник сохранён!", reply_markup=main_menu)
    await state.clear()

# Список соперников
@router.callback_query(F.data == "list_opponents")
async def list_opponents(callback: types.CallbackQuery):
    async with aiosqlite.connect("spinbox.db") as db:
        async with db.execute(
            "SELECT id, name, level, style FROM opponents WHERE user_id=? ORDER BY name",
            (callback.from_user.id,)
        ) as cursor:
            opps = await cursor.fetchall()
    if not opps:
        await callback.answer("Список пуст", show_alert=True)
        return
    kb = types.InlineKeyboardMarkup(inline_keyboard=[])
    for o in opps:
        kb.inline_keyboard.append([types.InlineKeyboardButton(
            text=f"{o[1]} ({o[2]}, {o[3]})",
            callback_data=f"opponent_{o[0]}"
        )])
    await callback.message.answer("Список соперников:", reply_markup=kb)
    await callback.answer()

@router.callback_query(F.data.startswith("opponent_"))
async def opponent_detail(callback: types.CallbackQuery):
    opp_id = int(callback.data.split("_")[1])
    async with aiosqlite.connect("spinbox.db") as db:
        async with db.execute("SELECT * FROM opponents WHERE id=?", (opp_id,)) as cursor:
            opp = await cursor.fetchone()
    if not opp:
        await callback.answer("Не найден", show_alert=True)
        return
    # Формируем текстовое представление
    text = f"🃏 <b>{opp[2]}</b>\n"
    if opp[3]: text += f"Уровень: {opp[3]}\n"
    if opp[4]: text += f"Стиль: {opp[4]}\n"
    if opp[5]: text += f"Хватка: {opp[5]}\n"
    if opp[6]: text += f"Рука: {opp[6]}\n"
    if opp[7]: text += f"Основание: {opp[7]}\n"
    if opp[8]: text += f"FH: {opp[8]}\n"
    if opp[9]: text += f"BH: {opp[9]}\n"
    if opp[10]: text += f"Спец. накладки: {opp[10]}\n"
    if opp[19]: text += f"\n📌 <b>Тактические заметки:</b>\n{opp[19]}"
    # Кнопки действий
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🔎 Тактика на матч", callback_data=f"tactics_{opp_id}")],
        [types.InlineKeyboardButton(text="📝 Редактировать заметки", callback_data=f"edit_notes_{opp_id}")],
        [types.InlineKeyboardButton(text="🗑 Удалить", callback_data=f"delete_opp_{opp_id}")]
    ])
    await callback.message.answer(text, parse_mode="HTML", reply_markup=kb)
    await callback.answer()

# Быстрый вывод тактики (только заметки)
@router.callback_query(F.data.startswith("tactics_"))
async def show_tactics(callback: types.CallbackQuery):
    opp_id = int(callback.data.split("_")[1])
    async with aiosqlite.connect("spinbox.db") as db:
        async with db.execute("SELECT name, tactical_notes FROM opponents WHERE id=?", (opp_id,)) as cursor:
            opp = await cursor.fetchone()
    if opp:
        await callback.message.answer(f"🔎 Тактика против <b>{opp[0]}</b>:\n\n{opp[1] or 'Нет заметок'}", parse_mode="HTML")
    await callback.answer()

# Другие действия (заглушки)
@router.callback_query(F.data.startswith("edit_notes_"))
async def edit_notes(callback: types.CallbackQuery, state: FSMContext):
    # Можно реализовать редактирование заметок через отдельный FSM, оставим для будущего
    await callback.answer("Функция в разработке", show_alert=True)

@router.callback_query(F.data.startswith("delete_opp_"))
async def delete_opponent(callback: types.CallbackQuery):
    opp_id = int(callback.data.split("_")[2])
    async with aiosqlite.connect("spinbox.db") as db:
        await db.execute("DELETE FROM opponents WHERE id=? AND user_id=?", (opp_id, callback.from_user.id))
        await db.commit()
    await callback.answer("Соперник удалён")
    await callback.message.delete()