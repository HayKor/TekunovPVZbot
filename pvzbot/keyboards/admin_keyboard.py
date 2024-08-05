from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from callback.enums import AdminCallback, Office, OfficeAction, OfficeCbData


def build_main_kb() -> InlineKeyboardMarkup:
    points_btn = InlineKeyboardButton(
        text="Пункты",
        callback_data=AdminCallback.POINTS,
    )
    office_btn = InlineKeyboardButton(
        text="Офис",
        callback_data=AdminCallback.OFFICE,
    )
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [points_btn, office_btn],
        ]
    )
    return markup


def build_points_menu_kb() -> InlineKeyboardMarkup:
    list_btn = InlineKeyboardButton(
        text="Все пункты",
        callback_data=AdminCallback.POINTS_LIST,
    )
    add_btn = InlineKeyboardButton(
        text="Добавить",
        callback_data=AdminCallback.POINTS_ADD,
    )
    remove_btn = InlineKeyboardButton(
        text="Удалить",
        callback_data=AdminCallback.POINTS_REMOVE,
    )
    back_btn = InlineKeyboardButton(
        text="Назад",
        callback_data=AdminCallback.MENU,
    )
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [list_btn],
            [add_btn, remove_btn],
            [back_btn],
        ]
    )
    return markup


def build_back_to_points_menu_kb() -> InlineKeyboardMarkup:
    back_btn = InlineKeyboardButton(
        text="Назад",
        callback_data=AdminCallback.POINTS,
    )
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [back_btn],
        ]
    )
    return markup


def build_office_menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for name, _type in [
        ("⚠️ Претензия", Office.PRETENTIOUS),
        ("🗓  График", Office.SHIFT),
        ("ℹ Ссылка", Office.INFOLINK),
        ("💰 Касса", Office.MONEY),
        ("🪛 Техник", Office.TECH),
    ]:
        builder.button(
            text=name,
            callback_data=OfficeCbData(
                type=_type,
                action=OfficeAction.show,
            ).pack(),
        )
    builder.button(
        text="Назад",
        callback_data=AdminCallback.MENU,
    )
    builder.adjust(2, 2, 1, 1)
    return builder.as_markup()


def build_office_crud_kb(_type: str) -> InlineKeyboardMarkup:
    add_btn = InlineKeyboardButton(
        text="Добавить",
        callback_data=OfficeCbData(
            type=_type,
            action=OfficeAction.add,
        ).pack(),
    )
    remove_btn = InlineKeyboardButton(
        text="Удалить",
        callback_data=OfficeCbData(
            type=_type,
            action=OfficeAction.remove,
        ).pack(),
    )
    back_btn = InlineKeyboardButton(
        text="Назад",
        callback_data=AdminCallback.OFFICE,
    )
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [add_btn, remove_btn],
            [back_btn],
        ]
    )
    return markup


def build_back_to_office_kb() -> InlineKeyboardMarkup:
    back_btn = InlineKeyboardButton(
        text="Назад",
        callback_data=AdminCallback.OFFICE,
    )
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [back_btn],
        ]
    )
    return markup
