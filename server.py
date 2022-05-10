import logging
import os

import aiohttp
from aiogram import Bot, Dispatcher, executor, types

import exceptions
import expenses
import incomes
from categories import Categories

# Инициализация бота по его токену
bot = Bot('5375384328:AAEUlNxptWy6Z0kBdhdt5rm5KUKGJsL_nw0')
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    # Первое сообщение телеграм аккаунту или при вводе комманд /start, /help
    await message.answer(
        "Бот для трекинга доходов и расходов\n\n"
        "Чтобы добавить расход введите сообщение по формату: /expense число категория. Пример: /expense 250 еда\n\n"
        "Чтобы добавить доход введите сообщение по формату: /income число доход. Пример: /income 500 доход\n\n"
        "Сегодняшняя статистика расходов: /today\n"
        "Статистика расходов за месяц: /month\n"
        "Последние внесённые расходы: /expenses\n"
        "Категории трат: /categories")


@dp.message_handler(lambda message: message.text.startswith('/del'))
async def del_expense(message: types.Message):
    # Удаление записи о расходе
    row_id = int(message.text[4:])
    expenses.delete_expense(row_id)
    answer_message = "Удалил"
    await message.answer(answer_message)


@dp.message_handler(commands=['categories'])
async def categories_list(message: types.Message):
    # Вывод категорий
    categories = Categories().get_all_categories()
    answer_message = "Категории трат:\n\n* " + \
                     ("\n* ".join([c.name + ' (' + ", ".join(c.aliases) + ')' for c in categories]))
    await message.answer(answer_message)


@dp.message_handler(commands=['today'])
async def today_statistics(message: types.Message):
    # Статистика сегодняшних трат
    answer_message = expenses.get_today_statistics()
    await message.answer(answer_message)


@dp.message_handler(commands=['month'])
async def month_statistics(message: types.Message):
    # Траты за текущий месяц
    answer_message = expenses.get_month_statistics()
    await message.answer(answer_message)


@dp.message_handler(commands=['expenses'])
async def list_expenses(message: types.Message):
    # Последние расходы
    last_expenses = expenses.last()
    if not last_expenses:
        await message.answer("Расходы ещё не заведены")
        return

    last_expenses_rows = [
        f"{expense.amount} руб. на {expense.category_name} — нажми "
        f"/del{expense.id} для удаления"
        for expense in last_expenses]
    answer_message = "Последние сохранённые траты:\n\n* " + "\n\n* " \
        .join(last_expenses_rows)
    await message.answer(answer_message)


@dp.message_handler(lambda message: message.text.startswith('/expense '))
async def add_expense(message: types.Message):
    # Добавление в БД нового расхода
    try:
        expense = expenses.add_expense(message.text[9:])
    except exceptions.NotCorrectMessage as e:
        await message.answer(str(e))
        return
    answer_message = (
        f"Добавлены траты {expense.amount} руб на {expense.category_name}.\n\n"
        f"{expenses.get_today_statistics()}")
    await message.answer(answer_message)


@dp.message_handler(lambda message: message.text.startswith('/income '))
async def add_income(message: types.Message):
    # Добавление в БД нового дохода
    try:
        income = incomes.add_income(message.text[8:])
    except exceptions.NotCorrectMessage as e:
        await message.answer(str(e))
        return
    answer_message = (
        f"Добавлены доходы {income.amount} руб на {income.category_name}.\n\n")
    await message.answer(answer_message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
