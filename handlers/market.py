from aiogram import Router, F, Bot
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from lexicon import lexicon_ru
from services.services import pages
from database.database import Database
from keyboards.keyboards import Keyboards
from FSMS.FSMS import MenuPagesFSM, MarketFSM


router = Router()
kb = Keyboards()
db = Database()


@router.callback_query(MenuPagesFSM.menu, F.data == 'market')
async def cmd_market_choose_category(callback: CallbackQuery, state: FSMContext):
    categories = db.get_goods_categories()
    pages.update_states(
        callback.message.text,
        callback.message.reply_markup,
        await state.get_state()
    )
    await callback.message.edit_text(
        text=lexicon_ru.market_texts['choose_category'],
        reply_markup=kb.goods_keyboard(categories=categories)
    )
    await state.set_state(MarketFSM.choose_category)


@router.callback_query(MarketFSM.choose_category)
async def cmd_market_choose_goods(callback: CallbackQuery, state: FSMContext):
    category = callback.data
    goods_titles = db.get_goods_titles(category)
    pages.update_states(
        callback.message.text,
        callback.message.reply_markup,
        await state.get_state()
    )
    await callback.message.edit_text(
        text=lexicon_ru.market_texts['choose_goods'].format(category.lower()),
        reply_markup=kb.goods_keyboard(goods_titles=goods_titles)
    )
    await state.set_state(MarketFSM.choose_goods)


@router.callback_query(MarketFSM.choose_goods)
async def cmd_market_check_goods(callback: CallbackQuery, state: FSMContext):
    goods_id = int(callback.data)
    goods_info = db.get_good_info(goods_id)
    pages.update_states(
        callback.message.text,
        callback.message.reply_markup,
        await state.get_state()
    )
    await callback.message.edit_text(
        text=lexicon_ru.market_texts['check_goods'].format(*goods_info),
        reply_markup=kb.goods_keyboard(goods_info=True),
        parse_mode=ParseMode.HTML
    )
    await state.update_data(
        goods_id=goods_id,
        goods_title=goods_info[0],
        goods_author=goods_info[1],
        goods_category=goods_info[2],
        goods_decription=goods_info[3],
        goods_price=goods_info[4],
        goods_value=goods_info[-1]
    )
    await state.set_state(MarketFSM.check_goods)


@router.callback_query(F.data == 'buy', MarketFSM.check_goods)
async def cmd_market_buy(callback: CallbackQuery, state: FSMContext):
    goods_value = (await state.get_data())['goods_value']
    await state.update_data(buy_put_value=1)
    pages.update_states(
        callback.message.text,
        callback.message.reply_markup,
        await state.get_state()
    )
    await callback.message.edit_text(
        text=lexicon_ru.market_texts['buy_value'],
        reply_markup=kb.buy_put_keyboard(1, goods_value),
    )
    await state.set_state(MarketFSM.buy_put)


@router.callback_query(MarketFSM.buy_put, F.data == '+')
async def cmd_market_buy_value(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    goods_value = data['goods_value']
    buy_put_value = data['buy_put_value'] + 1
    await state.update_data(buy_put_value=buy_put_value)
    await callback.message.edit_text(
        text=callback.message.text,
        reply_markup=kb.buy_put_keyboard(buy_put_value, goods_value)
    )
        

@router.callback_query(MarketFSM.buy_put, F.data == '-')
async def cmd_market_buy_value(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    goods_value = data['goods_value']
    buy_put_value = data['buy_put_value'] - 1
    await state.update_data(buy_put_value=buy_put_value)
    await callback.message.edit_text(
        text=callback.message.text,
        reply_markup=kb.buy_put_keyboard(buy_put_value, goods_value)
    )


@router.callback_query(MarketFSM.buy_put, F.data == 'buy_put_value')
async def cmd_market_buy_value_press(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.answer()


@router.callback_query(MarketFSM.buy_put, F.data == 'buy')
async def cmd_market_accept_or_not_buy(callback: CallbackQuery, state: FSMContext):
    pages.update_states(
        callback.message.text,
        callback.message.reply_markup,
        await state.get_state()
    )
    await callback.message.edit_text(
        text=lexicon_ru.market_texts['accept_buy'],
        reply_markup=kb.base_keyboard(lexicon_ru.accept_buttons)
    )
    await state.set_state(MarketFSM.accept_buy)


@router.callback_query(MarketFSM.accept_buy, F.data == 'yes')
async def cmd_market_accept_buy(callback: CallbackQuery, state: FSMContext):
    pass


@router.callback_query(MarketFSM.buy_put, F.data == 'put')
async def cmd_market_put_cart(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    db.update_user_cart(
        callback.from_user.id, 
        data['goods_id'], 
        data['buy_put_value'],
        data['goods_title'],
        data['buy_put_value'] * data['goods_price']
    )
    await callback.message.edit_text(
        text=lexicon_ru.market_texts['put_cart_succesfull'].format(
            data['goods_title'], data['buy_put_value']
        ),
        reply_markup=kb.base_keyboard(lexicon_ru.back_buttons)
    )