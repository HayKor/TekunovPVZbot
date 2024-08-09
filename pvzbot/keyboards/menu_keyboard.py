from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from callback.enums import Callback


def build_menu_kb() -> InlineKeyboardMarkup:
    info_btn = InlineKeyboardButton(
        text="ℹ Информация",
        callback_data=Callback.INFO,
    )
    shifting_btn = InlineKeyboardButton(
        text="🗓  График",
        callback_data=Callback.SHIFT,
    )
    trouble_btn = InlineKeyboardButton(
        text="⚠️  Проблема с товаром",
        callback_data=Callback.TROUBLE,
    )
    tech_btn = InlineKeyboardButton(
        text="🪛 Техническая проблема",
        callback_data=Callback.TECH,
    )
    money_btn = InlineKeyboardButton(
        text="💰 Касса",
        callback_data=Callback.MONEY,
    )
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [info_btn, shifting_btn],
            [trouble_btn],
            [money_btn],
            [tech_btn],
        ]
    )
    return markup


def build_info_kb(url: str) -> InlineKeyboardMarkup:
    info_btn = InlineKeyboardButton(
        text="🔗 Ссылка",
        url=url,
    )
    back_btn = InlineKeyboardButton(
        text="Назад",
        callback_data=Callback.MENU,
    )
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [info_btn],
            [back_btn],
        ]
    )
    return markup


def build_back_to_menu_kb() -> InlineKeyboardMarkup:
    back_btn = InlineKeyboardButton(
        text="Назад",
        callback_data=Callback.MENU,
    )
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [back_btn],
        ]
    )
    return markup


def build_tech_kb() -> InlineKeyboardMarkup:
    back_btn = InlineKeyboardButton(
        text="Назад",
        callback_data=Callback.MENU,
    )
    get_tech_help_btn = InlineKeyboardButton(
        text="📝 Создать заявку",
        callback_data=Callback.TECH_FORM,
    )
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [get_tech_help_btn],
            [back_btn],
        ]
    )
    return markup


def build_cancel_kb() -> ReplyKeyboardMarkup:
    cancel_btn = KeyboardButton(text="/cancel")
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [cancel_btn],
        ],
        resize_keyboard=True,
    )
    return markup


def build_category_kb() -> ReplyKeyboardMarkup:
    cancel_btn = KeyboardButton(text="/cancel")
    internet_btn = KeyboardButton(text="Интернет")
    terminal_btn = KeyboardButton(text="Терминал")
    printer_btn = KeyboardButton(text="Принтер")
    scanner_btn = KeyboardButton(text="Сканер")
    other_btn = KeyboardButton(text="Другое")
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [internet_btn, terminal_btn, printer_btn, scanner_btn],
            [other_btn],
            [cancel_btn],
        ],
        resize_keyboard=True,
    )
    return markup
