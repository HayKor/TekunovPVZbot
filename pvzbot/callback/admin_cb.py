from typing import Any

from aiogram import F, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from callback.enums import AdminCallback, Office, OfficeAction, OfficeCbData
from database.engine import async_session
from database.office_crud import (
    create_office_thing,
    get_office_thing_all_params,
    get_office_thing_by_occupation,
)
from database.point_crud import get_points
from filters import IsAdmin
from keyboards.admin_keyboard import (
    build_back_to_office_kb,
    build_back_to_points_menu_kb,
    build_main_kb,
    build_office_crud_kb,
    build_office_menu_kb,
    build_points_menu_kb,
)
from keyboards.menu_keyboard import build_cancel_kb
from states.admin_states import AddOfficeEntity, RemoveOfficeEntity


router = Router(name=__name__)


@router.message(Command("admin"), IsAdmin())
@router.callback_query(F.data == AdminCallback.MENU)
async def handle_help(
    message: types.Message | types.CallbackQuery,
    state: FSMContext,
) -> None:
    await state.clear()
    markup = build_main_kb()
    text = "Выберите категорию.\n"
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


@router.callback_query(F.data == AdminCallback.POINTS, IsAdmin())
async def handle_points_query(callback: types.CallbackQuery) -> None:
    markup = build_points_menu_kb()
    await callback.message.edit_text(
        text="Выберите категорию",
        reply_markup=markup,
    )


@router.callback_query(F.data == AdminCallback.POINTS_LIST, IsAdmin())
async def handle_points_list_query(callback: types.CallbackQuery) -> None:
    points_list = await get_points(async_session)
    text = "<b>Список всех пунктов:</b>\n"
    markup = build_back_to_points_menu_kb()
    if points_list:
        for count, point in enumerate(points_list):
            text += f"<b>{count + 1}.</b> <code>{point.address} {point.type}</code>\n"
        await callback.message.edit_text(
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=markup,
        )
    else:
        await callback.message.edit_text(
            text="Нету(((",
            parse_mode=ParseMode.HTML,
            reply_markup=markup,
        )


@router.callback_query(F.data == AdminCallback.OFFICE, IsAdmin())
async def handle_office_query(callback: types.CallbackQuery) -> None:
    markup = build_office_menu_kb()
    await callback.message.edit_text(
        text="Выберите категорию",
        reply_markup=markup,
    )


@router.callback_query(
    OfficeCbData.filter(F.action == OfficeAction.show),
)
async def handle_show_office_by_type(
    callback: types.CallbackQuery,
    callback_data: OfficeCbData,
) -> None:
    await callback.answer()
    markup = build_office_crud_kb(callback_data.type)
    text = f"К типу {callback_data.type} относятся:\n"
    office_workers = await get_office_thing_by_occupation(
        async_session,
        occupation=callback_data.type,
    )
    for worker in office_workers:
        text += (
            f"<b>{worker.name}</b> (@{worker.tg_nickname}) {worker.schedule if worker.schedule else ''}"
            f" {worker.description if worker.description else ''} <code>{worker.phone if worker.phone else ''}</code>\n"
        )
    await callback.message.edit_text(
        text=text,
        reply_markup=markup,
        parse_mode=ParseMode.HTML,
    )


@router.callback_query(
    OfficeCbData.filter(F.action == OfficeAction.add),
)
async def handle_add_to_office(
    callback: types.CallbackQuery,
    callback_data: OfficeCbData,
    state: FSMContext,
) -> None:
    await callback.answer()
    await state.set_state(AddOfficeEntity.name)
    await state.update_data(occupation=callback_data.type)
    await callback.message.reply(
        text="Напиши имя и фамилию нового мембера вашей пати:",
        reply_markup=build_cancel_kb(),
    )


@router.message(AddOfficeEntity.name)
async def handle_name(
    message: types.Message,
    state: FSMContext,
) -> None:
    await state.update_data(name=message.text)
    await state.set_state(AddOfficeEntity.tg_nickname)
    await message.reply(
        text="Введите никнейм в тг без @:",
        reply_markup=build_cancel_kb(),
    )


@router.message(AddOfficeEntity.tg_nickname)
async def handle_tg_nickname(
    message: types.Message,
    state: FSMContext,
) -> None:
    await state.update_data(tg_nickname=message.text)
    await state.set_state(AddOfficeEntity.phone)
    await message.reply(
        text="Введите номер телефона (хоть какой-нибудь пж):",
        reply_markup=build_cancel_kb(),
    )


@router.message(AddOfficeEntity.phone)
async def handle_phone(
    message: types.Message,
    state: FSMContext,
) -> None:
    await state.update_data(phone=message.text)
    await state.set_state(AddOfficeEntity.schedule)
    await message.reply(
        text="Введите график работы пж.\nТипа 'ПН-ПТ 11:00-13:00':",
        reply_markup=build_cancel_kb(),
    )


@router.message(AddOfficeEntity.schedule)
async def handle_schedule(
    message: types.Message,
    state: FSMContext,
) -> None:
    await state.update_data(schedule=message.text)
    await state.set_state(AddOfficeEntity.description)
    await message.reply(
        text="Введите пжпжп описание (для инфоссылки - это сама ссылка и есть):",
        reply_markup=build_cancel_kb(),
    )


@router.message(AddOfficeEntity.description)
async def handle_desc(
    message: types.Message,
    state: FSMContext,
) -> None:
    data = await state.update_data(description=message.text)

    await make_conclusion_add(message=message, data=data)


async def make_conclusion_add(
    message: types.Message, data: dict[str, Any]
) -> Office | None:
    check = await get_office_thing_all_params(async_session, **data)
    if check:
        await message.reply(
            text="Такой челик уже есть как бэ",
            reply_markup=build_back_to_office_kb(),
        )
    else:
        office_thing = await create_office_thing(async_session, **data)
        text = (
            f"Успешно создан офисник с параметрами:\n"
            f"<b>{office_thing.name}</b> (@{office_thing.tg_nickname}) {office_thing.schedule if office_thing.schedule else ''}"
            f" {office_thing.description if office_thing.description else ''} <code>{office_thing.phone if office_thing.phone else ''}</code>\n"
        )
        await message.reply(
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=build_back_to_office_kb(),
        )


#
@router.callback_query(
    OfficeCbData.filter(F.action == OfficeAction.remove),
)
async def handle_remove_from_office(
    callback: types.CallbackQuery,
    callback_data: OfficeCbData,
    state: FSMContext,
) -> None:
    await callback.answer()
    await state.update_data(occupation=callback_data.type)
    await state.set_state(RemoveOfficeEntity.number)
    text = "Введите номер офисника для удаления:\n"
    office_workers = await get_office_thing_by_occupation(
        async_session,
        occupation=callback_data.type,
    )
    for idx, worker in enumerate(office_workers):
        text += (
            f"<b>{idx}</b>. <b>{worker.name}</b> (@{worker.tg_nickname}) {worker.schedule if worker.schedule else ''}"
            f" {worker.description if worker.description else ''} <code>{worker.phone if worker.phone else ''}</code>\n"
        )
    await callback.message.reply(
        text=text,
        reply_markup=build_cancel_kb(),
        parse_mode=ParseMode.HTML,
    )


@router.message(RemoveOfficeEntity.number)
async def handle_remove_office_entity_number(
    message: types.Message,
    state: FSMContext,
) -> None:
    data = await state.update_data(number=message.text)
    office_workers = await get_office_thing_by_occupation(
        async_session,
        occupation=data["occupation"],
    )
    try:
        async with async_session() as session:
            office = await session.delete(office_workers[int(data["number"])])
            await session.commit()
    except:
        await message.reply(text="Что-то пошло не так")
    else:
        await message.reply(
            text="Успех!",
            reply_markup=build_back_to_office_kb(),
            parse_mode=ParseMode.HTML,
        )
    await state.clear()
