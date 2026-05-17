from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import aiosqlite
from datetime import date

router = Router()

class AddEquipment(StatesGroup):
    waiting_base = State()
    waiting_fh = State()
    waiting_bh = State()

@router.message(F.text == "📊 Моя экипировка")
async def equipment_menu(message: types.Message):
    async with aiosqlite.connect("spinbox.db") as db:
        async with db.execute(
            "SELECT id, base, fh_rubber, bh_rubber, install_date FROM my_equipment WHERE user_id=? AND active=1",
            (message.from_user.id,)
        ) as cursor:
            rows = await cursor.fetchall()
    if rows:
        text = "🎾 <b>Ваша экипировка:</b>\n\n"
        for r in rows:
            text += f"🆔 {r[0]}: {r[1]} / {r[2]} / {r[3]} (установлена {r[4]})\n"
        await message.answer(text, parse_mode="HTML")
    else:
        await message.answer("У вас нет сохранённой экипировки.")
    # Кнопка добавления
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="➕ Добавить сборку", callback_data="add_equipment")]
    ])
    await message.answer("Действия:", reply_markup=kb)

@router.callback_query(F.data == "add_equipment")
async def start_add_equipment(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Введите модель основания:")
    await state.set_state(AddEquipment.waiting_base)

@router.message(AddEquipment.waiting_base)
async def base_entered(message: types.Message, state: FSMContext):
    await state.update_data(base=message.text)
    await message.answer("Введите модель накладки на форхенд (FH):")
    await state.set_state(AddEquipment.waiting_fh)

@router.message(AddEquipment.waiting_fh)
async def fh_entered(message: types.Message, state: FSMContext):
    await state.update_data(fh_rubber=message.text)
    await message.answer("Введите модель накладки на бэкхенд (BH):")
    await state.set_state(AddEquipment.waiting_bh)

@router.message(AddEquipment.waiting_bh)
async def bh_entered(message: types.Message, state: FSMContext):
    data = await state.get_data()
    async with aiosqlite.connect("spinbox.db") as db:
        await db.execute(
            "INSERT INTO my_equipment (user_id, base, fh_rubber, bh_rubber, install_date) VALUES (?,?,?,?,?)",
            (message.from_user.id, data["base"], data["fh_rubber"], message.text, date.today().isoformat())
        )
        await db.commit()
    await message.answer("✅ Сборка сохранена! Теперь она будет доступна при записи тренировок.", reply_markup=main_menu)
    await state.clear()