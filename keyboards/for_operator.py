from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def zaiavki_period_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="ПРЕКРАТИТЬ")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)
