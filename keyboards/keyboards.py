from lexicon import lexicon_ru
from database.models import ShoppingCartModel
from aiogram.types import (BotCommand, InlineKeyboardMarkup, 
                           InlineKeyboardButton, ContentType)
from aiogram.filters.callback_data import CallbackData


def set_commands() -> list[BotCommand]:
    commands = [
        BotCommand(command=key, description=value)
        for key, value in lexicon_ru.bot_menu.items()
    ]
    return commands


class CartItemsFactory(CallbackData, prefix='cart_item'):
    cart_id: int
    good_id: int


class Keyboards:
    def __init__(self) -> None:
        self.back_buttons = [
            [InlineKeyboardButton(text=value, callback_data=key)]
            for key, value in lexicon_ru.back_buttons.items()
        ]

    @staticmethod
    def menu_keyboard() -> InlineKeyboardMarkup:
        buttons = [
            [InlineKeyboardButton(text=value, callback_data=key)]
            for key, value in lexicon_ru.menu_buttons.items()
        ]
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard

    @staticmethod
    def base_keyboard(lexicon: dict) -> InlineKeyboardMarkup:
        buttons = [
            [InlineKeyboardButton(text=value, callback_data=key)]
            for key, value in lexicon.items()
        ]
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard

    def goods_keyboard(
        self,
        categories: list = None,
        goods_titles: list = None,
        goods_info: bool = None
    ) -> InlineKeyboardMarkup:
        if categories is not None:
            buttons = [
                [InlineKeyboardButton(text=category, callback_data=category)]
                for category in categories
            ]
            buttons.append(self.back_buttons[-1])
            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        elif goods_titles is not None:
            buttons = [
                [InlineKeyboardButton(text=title, callback_data=str(good_id))]
                for title, good_id in goods_titles
            ]
            buttons.extend(self.back_buttons)
            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        elif goods_info is not None:
            btn = lexicon_ru.market_buy_or_put_buttons['buy']
            buttons = [
                [InlineKeyboardButton(text=btn, callback_data='buy')]
            ]
            buttons.extend(self.back_buttons)
            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        else:
            keyboard = InlineKeyboardMarkup(inline_keyboard=self.back_buttons)
        return keyboard

    def buy_put_keyboard(
        self, 
        buy_put_value: int, 
        goods_value: int
    ) -> InlineKeyboardMarkup:
        buy_put_buttons = [
            InlineKeyboardButton(text=value, callback_data=key)
            for key, value in lexicon_ru.market_buy_or_put_buttons.items()
        ]
        if 1 < buy_put_value < goods_value:
            buttons = [
                [
                    InlineKeyboardButton(text='-', callback_data='-'),
                    InlineKeyboardButton(text=str(buy_put_value), 
                                         callback_data='buy_put_value'),
                    InlineKeyboardButton(text='+', callback_data='+')
                ],
            ]
        elif goods_value == 1:
            buttons = [
                [
                    InlineKeyboardButton(text=str(buy_put_value), 
                                         callback_data='buy_put_value')
                ]
            ]
        elif goods_value == buy_put_value:
            buttons = [
                [
                    InlineKeyboardButton(text='-', callback_data='-'),
                    InlineKeyboardButton(text=str(buy_put_value), 
                                         callback_data='buy_put_value')
                ]
            ]
        else:
            buttons = [
                [
                    InlineKeyboardButton(text=str(buy_put_value), 
                                         callback_data='buy_put_value'),
                    InlineKeyboardButton(text='+', callback_data='+')
                ]
            ]
        buttons.append(buy_put_buttons)
        buttons.extend(self.back_buttons)
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard
    
    def cart_items_keyboard(
        self,
        items: list[ShoppingCartModel], 
        choose_plural
    ) -> InlineKeyboardMarkup:
        lexicon = lexicon_ru.put_choose_plural['cart_good_value']
        buttons = [
            [
                InlineKeyboardButton(
                    text=f"{item.good_title}, {choose_plural(item.good_value, lexicon)}", 
                    callback_data=CartItemsFactory(
                        cart_id=item.cart_id,
                        good_id=item.good_id
                    ).pack()
                )
            ]
            for item in items
        ]
        buttons1 = [
            InlineKeyboardButton(text=value, callback_data=key)
            for key, value in lexicon_ru.check_cart_buttons.items()
        ]
        buttons.append(buttons1)
        buttons.append(self.back_buttons[-1])
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard
    
    def cart_item_info_keyboard(self) -> InlineKeyboardMarkup:
        buttons = [
            [InlineKeyboardButton(text=value, callback_data=key)]
            for key, value in lexicon_ru.cart_check_item_buttons.items()
        ]
        buttons.extend(self.back_buttons)
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard
    