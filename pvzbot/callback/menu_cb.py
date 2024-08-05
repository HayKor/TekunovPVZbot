from typing import Any

from aiogram import F, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaPhoto
from aiogram.utils.media_group import MediaGroupBuilder
from callback.enums import Callback, Office
from config import config
from database.engine import async_session
from database.office_crud import (
    get_office_thing,
    get_office_thing_by_occupation,
)
from keyboards.menu_keyboard import (
    build_back_to_menu_kb,
    build_cancel_kb,
    build_category_kb,
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
    url = await get_office_thing(async_session, name=Office.INFOLINK)
    markup = build_info_kb(url=url.description)
    await callback_query.message.edit_text(
        text="Всю информацию  по структуре офиса можно найти в информационном рабочем чате",
        reply_markup=markup,
    )


@router.callback_query(F.data == Callback.TROUBLE)
async def handle_trouble_query(callback_query: types.CallbackQuery) -> None:
    markup = build_back_to_menu_kb()
    text = "По всем вопросам претензионного характера обращаться к:\n"
    office_workers = await get_office_thing_by_occupation(
        async_session, occupation=Office.PRETENTIOUS
    )
    for worker in office_workers:
        text += f"<b>{worker.name}</b> (@{worker.tg_nickname}) {worker.schedule if worker.schedule else ''}\n"
    await callback_query.message.edit_text(
        text=text,
        reply_markup=markup,
        parse_mode=ParseMode.HTML,
    )


@router.callback_query(F.data == Callback.SHIFT)
async def handle_shift_query(callback_query: types.CallbackQuery) -> None:
    markup = build_back_to_menu_kb()
    text = "По всем вопросам графика обращаться к:\n"
    office_workers = await get_office_thing_by_occupation(
        async_session, occupation=Office.SHIFT
    )
    for worker in office_workers:
        text += f"<b>{worker.name}</b> (@{worker.tg_nickname}) {worker.schedule if worker.schedule else ''}\n"
    await callback_query.message.edit_text(
        text=text,
        reply_markup=markup,
        parse_mode=ParseMode.HTML,
    )


@router.callback_query(F.data == Callback.MONEY)
async def handle_money_query(callback_query: types.CallbackQuery) -> None:
    markup = build_back_to_menu_kb()
    text = "По всем вопросам касаемо денег и расходников обращаться к:\n"
    office_workers = await get_office_thing_by_occupation(
        async_session, occupation=Office.MONEY
    )
    for worker in office_workers:
        text += f"<b>{worker.name}</b> (@{worker.tg_nickname}) {worker.schedule if worker.schedule else ''}\n"
    await callback_query.message.edit_text(
        text=text,
        reply_markup=markup,
        parse_mode=ParseMode.HTML,
    )


@router.callback_query(F.data == Callback.TECH)
async def handle_tech_query(callback_query: types.CallbackQuery) -> None:
    await callback_query.answer()
    markup = build_tech_kb()
    technician = await get_office_thing_by_occupation(
        async_session, occupation=Office.TECH
    )
    technician = technician[0]
    await callback_query.message.edit_text(
        text=f"""Если проблема <b>срочная</b> (угрожает рабочему процессу), то стоит <b>как можно скорее</b> позвонить или сообщить техническому специалисту
<b>{technician.name}</b>:
<code>{technician.phone}</code> @{technician.tg_nickname}
Также можете создать заявку и подробно описать проблему.""",
        reply_markup=markup,
        parse_mode=ParseMode.HTML,
    )


@router.callback_query(F.data == Callback.TECH_FORM)
async def handle_tech_form_query(
    callback_query: types.CallbackQuery, state: FSMContext
) -> None:
    await callback_query.answer()
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
        text="Выберите категорию проблемы:",
        reply_markup=build_category_kb(),
    )


@router.message(TechHelp.category)
async def handle_tech_form_category(
    message: types.Message, state: FSMContext
) -> None:
    await state.update_data(category=message.text)
    await state.set_state(TechHelp.desc)
    await message.reply(
        text="Опишите проблему.\nМожете прикрепить <b>ОДНО</b> фото:",
        reply_markup=build_cancel_kb(),
        parse_mode=ParseMode.HTML,
    )


@router.message(TechHelp.desc)
async def handle_tech_form_desc(
    message: types.Message, state: FSMContext
) -> None:
    photo = None

    if message.photo:
        photo = message.photo[-1].file_id

    if message.text:
        desc = message.text
    elif message.caption:
        desc = message.caption
    else:
        desc = "Без описания"

    data = await state.update_data(
        desc=desc,
        photo=photo,
    )
    text = "Спасибо! Ваша заявка принята в обработку.\nНапоминаем, что если проблема срочная, то обращаться к:\n"
    office_workers = await get_office_thing_by_occupation(
        async_session, occupation=Office.TECH
    )
    for worker in office_workers:
        text += f"<b>{worker.name}</b> (@{worker.tg_nickname}) {worker.phone if worker.phone else ''}\n"
    await state.clear()
    await message.reply(
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await create_form(message, data)


async def create_form(message: types.Message, data: dict[str, Any]) -> None:
    chat_id = config.pvz_tech_chat_id
    technicians = await get_office_thing_by_occupation(
        async_session, occupation=Office.TECH
    )
    text = "Новая заявка!\n"
    for technician in technicians:
        text += f"@{technician.tg_nickname}\n"
    text += f"<b>От:</b> @{data['name']}\n"
    text += f"<b>Адрес:</b> {data['address']}\n"
    text += f"<b>Категория:</b> {data['category']}\n"
    text += f"<b>Описание:</b> {data['desc']}"
    # await message.bot.send_media_group(
    #     chat_id=chat_id,
    #     media=data["media_group"],
    # )
    await message.bot.send_photo(
        chat_id=chat_id,
        photo=data["photo"],
        caption=text,
        parse_mode=ParseMode.HTML,
    )
