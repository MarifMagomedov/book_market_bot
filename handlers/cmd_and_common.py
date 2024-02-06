from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from keyboards.keyboards import Keyboards
from lexicon import lexicon_ru
from services.services import pages
from database.database import Database
from FSMS.FSMS import RegistrationFSM, MenuPagesFSM


router = Router()
kb = Keyboards()
db = Database()


@router.message(Command('help'))
async def cmd_start(message: Message):
    await message.answer(
        text='zxc'
    )


@router.message(CommandStart())
async def cmd_start_registration(message: Message, state: FSMContext, bot: Bot):
    check_user = db.check_user_in_base(message.from_user.id)
    if not check_user:
        await state.set_state(RegistrationFSM.name)
        await message.answer(
            text=lexicon_ru.registration['name']
        )
    else:
        await bot.delete_message(
            message_id=message.message_id,
            chat_id=message.chat.id
        )
        await message.answer(
            text=lexicon_ru.registration['error_registration']
        )


@router.message(Command('menu'))
async def cmd_menu_main(message: Message, state: FSMContext):
    await state.set_state(MenuPagesFSM.menu)
    await message.answer(
        text=lexicon_ru.menu_text['main'],
        reply_markup=kb.menu_keyboard()
    )


@router.callback_query(F.data == 'back')
async def cmd_back(callback: CallbackQuery, state: FSMContext):
    prev_page = pages.get_prev_page()
    await callback.message.edit_text(
        text=prev_page['text'],
        reply_markup=prev_page['reply_markup']
    )
    await state.set_state(prev_page['state'])


@router.callback_query(F.data == 'back_to_menu')
async def cmd_back(callback: CallbackQuery, state: FSMContext):
    menu_page = pages.get_menu_page()
    await callback.message.edit_text(
        text=menu_page['text'],
        reply_markup=menu_page['reply_markup']
    )
    await state.set_state(menu_page['state'])
