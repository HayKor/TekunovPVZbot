from aiogram import Router, types
from database.engine import async_session
from database.polls_crud import update_poll_answer_true


router = Router(name=__name__)


@router.poll_answer()
async def handle_poll_answer(answer: types.PollAnswer):
    poll_id = answer.poll_id
    try:
        option_id = answer.option_ids[0]
        await update_poll_answer_true(async_session, int(poll_id), option_id)
    except:
        pass
