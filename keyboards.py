from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎯 Тренировка"), KeyboardButton(text="📋 Журнал")],
        [KeyboardButton(text="🃏 Соперники"), KeyboardButton(text="🔍 Тест ракетки")],
        [KeyboardButton(text="📊 Моя экипировка"), KeyboardButton(text="⚙️ Профиль")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие"
)

# Инлайн-клавиатуры для теста ракетки
style_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Атакующий", callback_data="style_attacking")],
    [InlineKeyboardButton(text="Защитник", callback_data="style_defensive")],
    [InlineKeyboardButton(text="Универсал", callback_data="style_allround")],
    [InlineKeyboardButton(text="С шипами/антиспином", callback_data="style_pimples")]
])

level_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Новичок", callback_data="level_beginner")],
    [InlineKeyboardButton(text="Любитель", callback_data="level_amateur")],
    [InlineKeyboardButton(text="Разрядник", callback_data="level_semi_pro")],
    [InlineKeyboardButton(text="Профессионал", callback_data="level_professional")]
])

grip_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Европейская прямая", callback_data="grip_shakehand")],
    [InlineKeyboardButton(text="Азиатская (перо)", callback_data="grip_penhold")]
])

speed_pref_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Контроль превыше всего", callback_data="speed_control")],
    [InlineKeyboardButton(text="Баланс скорости и контроля", callback_data="speed_balanced")],
    [InlineKeyboardButton(text="Максимальная скорость", callback_data="speed_max")]
])

spin_pref_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Сильное вращение", callback_data="spin_high")],
    [InlineKeyboardButton(text="Умеренное", callback_data="spin_medium")],
    [InlineKeyboardButton(text="Плоские удары", callback_data="spin_low")]
])

budget_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Эконом (до 3000₽)", callback_data="budget_low")],
    [InlineKeyboardButton(text="Средний (3000-8000₽)", callback_data="budget_medium")],
    [InlineKeyboardButton(text="Высокий (8000-15000₽)", callback_data="budget_high")],
    [InlineKeyboardButton(text="Без ограничений", callback_data="budget_unlimited")]
])

problem_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Не хватает вращения", callback_data="problem_spin")],
    [InlineKeyboardButton(text="Слишком быстрая ракетка", callback_data="problem_speed")],
    [InlineKeyboardButton(text="Устаёт кисть (тяжёлая)", callback_data="problem_weight")],
    [InlineKeyboardButton(text="Плохой контроль на приёме", callback_data="problem_control")],
    [InlineKeyboardButton(text="Ничего из перечисленного", callback_data="problem_none")]
])

weight_pref_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Лёгкое (до 80 г)", callback_data="weight_light")],
    [InlineKeyboardButton(text="Среднее (80-90 г)", callback_data="weight_medium")],
    [InlineKeyboardButton(text="Тяжёлое (90+ г)", callback_data="weight_heavy")],
    [InlineKeyboardButton(text="Не знаю / не важно", callback_data="weight_any")]
])

# Клавиатура для пропуска необязательных полей
skip_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Пропустить", callback_data="skip_field")]
])