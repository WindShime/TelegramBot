import datetime
import re
from typing import List, NamedTuple, Optional

import pytz

import db
import exceptions
from categories import Categories


class Message(NamedTuple):
    # Инициализация полученного сообщения
    amount: int
    category_text: str


class Income(NamedTuple):
    # Инициализируем доход
    id: Optional[int]
    amount: int
    category_name: str


def _get_now_formatted() -> str:
    # Получение даты
    return _get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


def _get_now_datetime() -> datetime.datetime:
    # Дата по МСК
    tz = pytz.timezone("Europe/Moscow")
    now = datetime.datetime.now(tz)
    return now


def _parse_message(raw_message: str) -> Message:
    # Обрабатываем полученное сообщение.
    # Отделяем на сумму, категорию, введенный текст и проверяем корректность ввода.
    regexp_result = re.match(r"([\d ]+) (.*)", raw_message)
    if not regexp_result or not regexp_result.group(0) \
            or not regexp_result.group(1) or not regexp_result.group(2):
        raise exceptions.NotCorrectMessage(
            "Пожалуйста, введите сообщение по правильному формату\n"
            "Например:\n5000 зарплата")

    amount = regexp_result.group(1).replace(" ", "")
    category_text = regexp_result.group(2).strip().lower()
    return Message(amount=amount, category_text=category_text)


def add_income(raw_message: str) -> Income:
    # Добавляем новый доход
    parsed_message = _parse_message(raw_message)
    category = Categories().get_category(
        parsed_message.category_text)
    inserted_row_id = db.insert("income", {
        "amount": parsed_message.amount,
        "created": _get_now_formatted(),
        "category_codename": category.codename,
        "raw_text": raw_message
    })
    return Income(id=None,
                   amount=parsed_message.amount,
                   category_name=category.name)