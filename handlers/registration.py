from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from FSMS.FSMS import RegistrationFSM
from lexicon import lexicon_ru
from filters.filters import ValidEmail, ValidNameSurname
from database.database import Database


router = Router()
db = Database()


@router.message(RegistrationFSM.name, ValidNameSurname())
async def cmd_set_name(message: Message, state: FSMContext):
    await state.update_data(user_id=message.from_user.id, name=message.text)
    await state.set_state(RegistrationFSM.surname)
    await message.answer(
        text=lexicon_ru.registration['surname']
    )


@router.message(RegistrationFSM.name)
async def cmd_set_name(message: Message):
    await message.answer(
        text=lexicon_ru.registration['error_data']
    )


@router.message(RegistrationFSM.surname, ValidNameSurname())
async def cmd_set_surname(message: Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await state.set_state(RegistrationFSM.email)
    await message.answer(
        text=lexicon_ru.registration['email']
    )


@router.message(RegistrationFSM.surname)
async def cmd_set_surname_error(message: Message, state: FSMContext):
    await message.answer(
        text=lexicon_ru.registration['error_data']
    )


@router.message(RegistrationFSM.email, ValidEmail())
async def cmd_set_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    data = await state.get_data()
    await state.clear()
    db.create_profile(*data.values())
    await message.answer(
        text=lexicon_ru.registration['end']
    )


@router.message(RegistrationFSM.email)
async def cmd_set_email(message: Message, state: FSMContext):
    await message.answer(
        text=lexicon_ru.registration['error_data']
    )