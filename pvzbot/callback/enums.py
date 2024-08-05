from enum import IntEnum, auto

from aiogram.filters.callback_data import CallbackData


class Callback:
    MENU = "menu_callback"
    INFO = "info_callback"
    SHIFT = "shift_callback"
    TROUBLE = "trouble_callback"
    TECH = "tech_callback"
    MONEY = "money_callback"
    TECH_FORM = "tech_help_form_callback"


class Office:
    INFOLINK = "Infolink"
    PRETENTIOUS = "Pretentious"
    SHIFT = "Shift"
    MONEY = "Money"
    TECH = "Technician"


class OfficeAction(IntEnum):
    add = auto()
    remove = auto()
    show = auto()


class OfficeCbData(CallbackData, prefix="office"):
    type: str
    action: OfficeAction


class AdminCallback:
    MENU = "admin_menu_callback"

    # Points
    POINTS = "points_callback"
    POINTS_LIST = "points_list_callback"
    POINTS_ADD = "points_add_callback"
    POINTS_REMOVE = "points_remove_callback"

    # Office
    OFFICE = "office_callback"
    OFFICE_PRETENT = "office_pretentious_callback"
    OFFICE_INFOLINK = "office_infolink_callback"
    OFFICE_MONEY = "office_money_callback"
    OFFICE_SHIFT = "office_shift_callback"
    OFFICE_TECHNICIAN = ...
