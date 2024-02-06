from aiogram.fsm.state import State, StatesGroup


class RegistrationFSM(StatesGroup):
    name = State()
    surname = State()
    email = State()


class MenuPagesFSM(StatesGroup):
    menu = State()


class ProfileEditFSM(StatesGroup):
    start = State()
    edit_param = State()
    edit_email = State()
    edit_name_surname = State()
    edit_accept = State()


class MarketFSM(StatesGroup):
    choose_category = State()
    choose_goods = State()
    check_goods = State()
    buy_put = State()
    accept_buy = State()


class CartFSM(StatesGroup):
    check_items = State()
    check_item = State()
    choose_items = State()
    buy_item = State()
    accept_buy = State()
    delete_item = State()
    