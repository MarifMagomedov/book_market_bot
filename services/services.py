from aiogram.types import InlineKeyboardMarkup
from lexicon.lexicon_ru import menu_text
from keyboards.keyboards import Keyboards
from FSMS.FSMS import MenuPagesFSM


kb = Keyboards()


def choose_plural(amount: int, variants: list) -> str:
    variant = 2
    if amount % 10 == 1 and amount % 100 != 11:
        variant = 0
    elif amount % 10 >= 2 and amount % 10 <= 4 and (amount % 100 < 10 or amount % 100 >= 20):
        variant = 1
    return '{} {}'.format(amount, variants[variant])


class Pages:
    def __init__(self):
        self.states = []
        self.menu_page = {
            'text': menu_text['main'],
            'reply_markup': kb.menu_keyboard(),
            'state': MenuPagesFSM.menu
        }

    def update_states(self, text: str, reply_markup: InlineKeyboardMarkup, state: str) -> None:
        self.states.append(
            {
                'text': text,
                'reply_markup': reply_markup,
                'state': state
            }
        )

    def get_prev_page(self) -> dict:
        return self.states.pop(-1)

    def get_menu_page(self) -> dict:
        self.states = []
        return self.menu_page

    def get_profile_page(self) -> dict:
        profile_page = self.states.pop(0)
        self.states = []
        return profile_page


pages = Pages()

