from aiogram import Router, F, Bot
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from lexicon import lexicon_ru
from database.database import Database
from FSMS.FSMS import MenuPagesFSM, CartFSM
from services.services import pages, choose_plural
from keyboards.keyboards import Keyboards, CartItemsFactory


router = Router()
kb = Keyboards()
db = Database()


@router.callback_query(MenuPagesFSM.menu, F.data == 'cart')
async def cmd_check_cart_items(callback: CallbackQuery, state: FSMContext):
    pages.update_states(
        callback.message.text,
        callback.message.reply_markup,
        await state.get_state()
    )
    user_cart =  db.get_user_cart(callback.from_user.id)
    await callback.message.edit_text(
        text=lexicon_ru.cart['check_cart'].format(
            choose_plural(
                len(user_cart), 
                lexicon_ru.put_choose_plural['orders_value']
            ),
            choose_plural(
                sum(i.total_sum for i in user_cart), 
                lexicon_ru.put_choose_plural['orders_sum']
            )
        ),
        reply_markup=kb.cart_items_keyboard(user_cart, choose_plural)
    )
    await state.update_data(user_cart=user_cart)
    await state.set_state(CartFSM.check_items)


@router.callback_query(CartFSM.check_items, F.data == 'choose')
async def cmd_choose_cart_items(callback: CallbackQuery, state: FSMContext):
    
    await callback.message.edit_text(
        text=lexicon_ru.cart['choose_items'],
        reply_markup=callback.message.reply_markup
    )



@router.callback_query(CartFSM.check_items, CartItemsFactory.filter())
async def cmd_cart_check_item_info(
    callback: CallbackQuery, 
    callback_data: CartItemsFactory, 
    state: FSMContext
):
    pages.update_states(
        callback.message.text,
        callback.message.reply_markup,
        await state.get_state()
    )
    item_info = db.get_good_info(callback_data.good_id)
    await callback.message.edit_text(
        text=lexicon_ru.cart['check_item'].format(*item_info),
        reply_markup=kb.cart_item_info_keyboard(),
        parse_mode=ParseMode.HTML
    )
    await state.update_data(
        good_id=callback_data.good_id, 
        cart_id=callback_data.cart_id
    )
    await state.set_state(CartFSM.check_item)


@router.callback_query(CartFSM.check_item, F.data == 'delete')
async def cmd_delete_cart_item(callback: CallbackQuery, state: FSMContext):
    pages.update_states(
        callback.message.text,
        callback.message.reply_markup,
        await state.get_state()
    )
    await callback.message.edit_text(
        text=lexicon_ru.cart['delete_item'],
        reply_markup=kb.base_keyboard(lexicon_ru.accept_buttons)
    )
    await state.set_state(CartFSM.delete_item)


@router.callback_query(CartFSM.delete_item, F.data == 'yes')
async def cmd_accept_delete_cart_item(callback: CallbackQuery, state: FSMContext):
    cart_id = (await state.get_data())['cart_id']
    db.delete_user_cart_item(cart_id)
    user_cart = db.get_user_cart(callback.from_user.id)
    await callback.message.edit_text(
        text=lexicon_ru.cart['check_cart'].format(
            choose_plural(
                len(user_cart), 
                lexicon_ru.put_choose_plural['orders_value']
            ),
            choose_plural(
                sum(i.total_sum for i in user_cart), 
                lexicon_ru.put_choose_plural['orders_sum']
            )
        ),
        reply_markup=kb.cart_items_keyboard(user_cart, choose_plural)
    )
    await state.clear()
    await state.set_state(CartFSM.check_items)
