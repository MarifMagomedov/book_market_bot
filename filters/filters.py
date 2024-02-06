import re
from aiogram.filters import BaseFilter
from aiogram.types import Message


class ValidNameSurname(BaseFilter):
    @staticmethod
    def check_name_or_surname(text):
        return text and any(elem.isalpha() for elem in text)

    async def __call__(self, message: Message):
        return self.check_name_or_surname(message.text)


class ValidEmail(BaseFilter):
    @staticmethod
    def check_email(email):
        return bool(re.findall(r'[a-zA-Z1-9]+@[a-zA-Z]+\.[a-zA-Z]+', email))

    async def __call__(self, message: Message):
        return self.check_email(message.text)
