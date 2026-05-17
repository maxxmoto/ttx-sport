from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards import *
from services.racket_selector import get_recommendation

router = Router()

class TestStates(StatesGroup):
    waiting_style = State()
    waiting_level = State()
    waiting_grip = State()
    waiting_speed = State()
    waiting_spin = State()
    waiting_budget = State()
    waiting_problem = State()
    waiting_weight = State()

@router.message(F.text == "🔍 Тест ракетки")
async def start_test(message: types.Message, state: FSMContext):
    await message.answer("Выберите ваш стиль игры:", reply_markup=style_inline)
    await state.set_state(TestStates.waiting_style)

@router.callback_query(TestStates.waiting_style)
async def style_chosen(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(style=callback.data)
    await callback.message.edit_text("Ваш текущий уровень:", reply_markup=level_inline)
    await state.set_state(TestStates.waiting_level)

@router.callback_query(TestStates.waiting_level)
async def level_chosen(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(level=callback.data)
    await callback.message.edit_text("Ваша хватка:", reply_markup=grip_inline)
    await state.set_state(TestStates.waiting_grip)

@router.callback_query(TestStates.waiting_grip)
async def grip_chosen(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(grip=callback.data)
    await callback.message.edit_text("Предпочтения по скорости:", reply_markup=speed_pref_inline)
    await state.set_state(TestStates.waiting_speed)

@router.callback_query(TestStates.waiting_speed)
async def speed_chosen(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(speed=callback.data)
    await callback.message.edit_text("Предпочтения по вращению:", reply_markup=spin_pref_inline)
    await state.set_state(TestStates.waiting_spin)

@router.callback_query(TestStates.waiting_spin)
async def spin_chosen(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(spin=callback.data)
    await callback.message.edit_text("Ваш бюджет:", reply_markup=budget_inline)
    await state.set_state(TestStates.waiting_budget)

@router.callback_query(TestStates.waiting_budget)
async def budget_chosen(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(budget=callback.data)
    await callback.message.edit_text("Основная проблема текущей ракетки:", reply_markup=problem_inline)
    await state.set_state(TestStates.waiting_problem)

@router.callback_query(TestStates.waiting_problem)
async def problem_chosen(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(problem=callback.data)
    await callback.message.edit_text("Предпочитаемый вес основания:", reply_markup=weight_pref_inline)
    await state.set_state(TestStates.waiting_weight)

@router.callback_query(TestStates.waiting_weight)
async def weight_chosen(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(weight=callback.data)
    # Все данные собраны
    answers = await state.get_data()
    result = get_recommendation(answers)
    await callback.message.edit_text(result, parse_mode="HTML")
    await state.clear()
    # Предложить сохранить сборку (опционально)
    await callback.message.answer("Вы можете сохранить эту сборку в «Моя экипировка», если приобретёте.")