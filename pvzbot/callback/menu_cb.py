from typing import Any

from aiogram import F, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from callback.enums import Callback
from config import config
from keyboards.menu_keyboard import (
    build_back_to_menu_kb,
    build_cancel_kb,
    build_info_kb,
    build_menu_kb,
    build_tech_kb,
)
from states.common_states import TechHelp


router = Router(name=__name__)


@router.message(Command("help"))
@router.callback_query(F.data == Callback.MENU)
async def handle_help(message: types.Message | types.CallbackQuery) -> None:
    markup = build_menu_kb()
    text = "Выберите наиболее подходящую категорию.\nВы можете получить помощь по всем из них!\n"
    if isinstance(message, types.Message):
        await message.reply(
            text=text,
            reply_markup=markup,
        )
    else:
        await message.message.edit_text(
            text=text,
            reply_markup=markup,
        )


@router.callback_query(F.data == Callback.INFO)
async def handle_info_query(callback_query: types.CallbackQuery) -> None:
    markup = build_info_kb()
    await callback_query.message.edit_text(
        text="Всю информацию  по структуре офиса можно найти в информационном рабочем чате",
        reply_markup=markup,
    )


@router.callback_query(F.data == Callback.TROUBLE)
async def handle_trouble_query(callback_query: types.CallbackQuery) -> None:
    markup = build_back_to_menu_kb()
    await callback_query.message.edit_text(
        text="По всем вопросам претензионного характера обращаться к:\n<b>Марку Андреевичу</b> (@AbsoluteM1337)\nИ к Даниилу Кирилловичу (@Danthepretentious)",
        reply_markup=markup,
        parse_mode=ParseMode.HTML,
    )


@router.callback_query(F.data == Callback.SHIFT)
async def handle_shift_query(callback_query: types.CallbackQuery) -> None:
    markup = build_back_to_menu_kb()
    await callback_query.message.edit_text(
        text="""По всем вопросам графика обращаться к:\n<b>Михаилу Андреевичу</b> (@AbsoluteM1488) ПН-ПТ \n""",
        reply_markup=markup,
        parse_mode=ParseMode.HTML,
    )


@router.callback_query(F.data == Callback.MONEY)
async def handle_money_query(callback_query: types.CallbackQuery) -> None:
    markup = build_back_to_menu_kb()
    await callback_query.message.edit_text(
        text="""По всем вопросам касаемо денег и расходников обращаться к:\n<b>Дарье Дмитриевне</b> (@tarya17) ПН-ПТ 10:00-19:00""",
        reply_markup=markup,
        parse_mode=ParseMode.HTML,
    )


@router.callback_query(F.data == Callback.TECH)
async def handle_tech_query(callback_query: types.CallbackQuery) -> None:
    markup = build_tech_kb()
    await callback_query.message.edit_text(
        text="""Если проблема <b>срочная</b> (угрожает рабочему процессу), то стоит <b>как можно скорее</b> позвонить или сообщить техническому специалисту
<b>Дмитрию Сергеевичу</b>:
<code>89654781772</code> @BingoB0ngo
Также можете создать заявку и подробно описать проблему.""",
        reply_markup=markup,
        parse_mode=ParseMode.HTML,
    )


@router.callback_query(F.data == Callback.TECH_FORM)
async def handle_tech_form_query(
    callback_query: types.CallbackQuery, state: FSMContext
) -> None:
    await state.set_state(TechHelp.address)
    await callback_query.message.reply(
        text="Напишите полный адрес пункта:",
        reply_markup=build_cancel_kb(),
    )


@router.message(TechHelp.address)
async def handle_tech_form_address(
    message: types.Message, state: FSMContext
) -> None:
    await state.update_data(address=message.text)
    await state.update_data(name=message.from_user.username)
    await state.set_state(TechHelp.category)
    await message.reply(
        text="Напишите категорию проблемы:",
        reply_markup=build_cancel_kb(),
    )


@router.message(TechHelp.category)
async def handle_tech_form_category(
    message: types.Message, state: FSMContext
) -> None:
    await state.update_data(category=message.text)
    await state.set_state(TechHelp.desc)
    await message.reply(
        text="Опишите проблему:",
        reply_markup=build_cancel_kb(),
    )


@router.message(TechHelp.desc)
async def handle_tech_form_desc(
    message: types.Message, state: FSMContext
) -> None:
    data = await state.update_data(desc=message.text)
    await state.clear()
    await message.reply(
        text="""Спасибо! Ваша заявка принята в обработку.\nНапоминаем, что если проблема срочная, то обращаться к:\n 
<b>Дмитрию Сергеевичу</b> <code>89654781772</code> @BingoB0ngo""",
        parse_mode=ParseMode.HTML,
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await create_form(message, data)


async def create_form(message: types.Message, data: dict[str, Any]) -> None:
    chat_id = config.pvz_tech_chat_id
    text = "Новая заявка! @BingoB0ngo\n"
    text += f"<b>От:</b> @{data['name']}\n"
    text += f"<b>Адрес:</b> {data['address']}\n"
    text += f"<b>Категория:</b> {data['category']}\n"
    text += f"<b>Описание:</b> {data['desc']}"
    await message.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode=ParseMode.HTML,
    )
