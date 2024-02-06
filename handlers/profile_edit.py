from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from keyboards.keyboards import Keyboards
from lexicon import lexicon_ru
from FSMS.FSMS import ProfileEditFSM, MenuPagesFSM
from database.database import Database
from services.services import pages
from filters.filters import ValidNameSurname, ValidEmail


router = Router()
kb = Keyboards()
db = Database()


@router.callback_query(F.data == 'profile', MenuPagesFSM.menu)
async def cmd_menu_profile(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ProfileEditFSM.start)
    user = db.select_user(callback.from_user.id)
    await callback.message.edit_text(
        text=lexicon_ru.profile_texts['main'].format(*user),
        reply_markup=kb.base_keyboard(lexicon_ru.profile_main_buttons)
    )


@router.callback_query(F.data == 'back_to_profile')
async def cmd_back(callback: CallbackQuery, state: FSMContext):
    profile_page = pages.get_profile_page()
    await callback.message.edit_text(
        text=profile_page['text'],
        reply_markup=profile_page['reply_markup']
    )
    await state.set_state(profile_page['state'])


@router.callback_query(F.data == 'edit_profile', ProfileEditFSM.start)
async def cmd_start_edit_profile(callback: CallbackQuery, state: FSMContext):
    pages.update_states(callback)
    await callback.message.edit_text(
        text=lexicon_ru.profile_edit_texts['edit_param'],
        reply_markup=kb.base_keyboard(lexicon_ru.profile_edit_buttons)
    )
    await state.set_state(ProfileEditFSM.edit_param)


@router.callback_query(ProfileEditFSM.edit_param)
async def cmd_profile_edit_param(callback: CallbackQuery, state: FSMContext):
    await state.update_data(
        edit_param=callback.data,
        prev_msg_id=callback.message.message_id
    )
    pages.update_states(callback)
    if callback.data == 'name' or callback.data == 'surname':
        await state.set_state(ProfileEditFSM.edit_name_surname)
    else:
        await state.set_state(ProfileEditFSM.edit_email)
    await callback.message.edit_text(
        text=lexicon_ru.profile_edit_texts['edit_value']
    )


@router.message(ProfileEditFSM.edit_name_surname, ValidNameSurname())
async def cmd_profile_edit_value(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(edit_value=message.text)
    await state.set_state(ProfileEditFSM.edit_accept)
    prev_msg_id = (await state.get_data())['prev_msg_id']
    await bot.delete_message(
        message_id=message.message_id,
        chat_id=message.chat.id
    )
    await bot.edit_message_text(
        text=lexicon_ru.profile_edit_texts['accept'],
        message_id=prev_msg_id,
        chat_id=message.chat.id,
        reply_markup=kb.base_keyboard(lexicon_ru.profile_accept_buttons)
    )


@router.message(ProfileEditFSM.edit_email, ValidEmail())
async def cmd_profile_edit_value(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(edit_value=message.text)
    await state.set_state(ProfileEditFSM.edit_accept)
    prev_msg_id = (await state.get_data())['prev_msg_id']
    await bot.delete_message(
        message_id=message.message_id,
        chat_id=message.chat.id
    )
    await bot.edit_message_text(
        text=lexicon_ru.profile_edit_texts['accept'],
        message_id=prev_msg_id,
        chat_id=message.chat.id,
        reply_markup=kb.base_keyboard(lexicon_ru.profile_accept_buttons)
    )


@router.message(ProfileEditFSM.edit_email)
@router.message(ProfileEditFSM.edit_name_surname)
async def cmd_profile_edit_value(message: Message, state: FSMContext, bot: Bot):
    prev_msg_id = (await state.get_data())['prev_msg_id']
    await bot.delete_message(
        message_id=message.message_id,
        chat_id=message.chat.id
    )
    await bot.edit_message_text(
        text=lexicon_ru.profile_edit_texts['edit_value_error'],
        message_id=prev_msg_id,
        chat_id=message.chat.id,
    )


@router.callback_query(ProfileEditFSM.edit_accept, F.data == 'yes')
async def cmd_profile_edit_accept(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    db.update_user_profile(
        callback.from_user.id,
        data['edit_param'],
        data['edit_value']
    )
    await callback.message.edit_text(
        text=lexicon_ru.profile_edit_texts['end'],
        reply_markup=kb.base_keyboard(lexicon_ru.profile_end)
    )
    await state.clear()
