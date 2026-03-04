from aiogram import Router, F
from aiogram import Bot
from aiogram.filters import Command, CommandObject, StateFilter, BaseFilter
from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile
from aiogram.enums.chat_member_status import ChatMemberStatus
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.exceptions import TelegramBadRequest

from settings import Settings
from tools.safe_message import message_answer_safe, bot_send_photo_safe, bot_send_video_safe
from mydb.db_work import appendRequest
from tools.upload import get_new_name_photo
from var import text_zaiavka

router = Router()

def prepareText(message:str):
    return message.replace('заявка','').strip()

def checkZaiavka(msg:str):
    res=False
    for zvka in text_zaiavka:
        if zvka in msg:
            return True
    return res

class ZaiavkaFilter(BaseFilter):
    def __init__(self, text_zaiavka_a: list): 
        self.text_zaiavka = text_zaiavka_a

    async def __call__(self, message: Message) -> bool:
        if message.caption:
            return checkZaiavka(message.caption)
        if message.text:
            return checkZaiavka(message.text)
        return False

@router.message(F.photo, ZaiavkaFilter(text_zaiavka))
async def cmd_photo_zaiavka(message: Message, bot: Bot, state: FSMContext):
    msg=message.caption
    name_file=get_new_name_photo()
    await bot.download(
        message.photo[-1],
        destination=name_file
        )
    appendRequest({'full_name':message.from_user.full_name, 'user_id':message.from_user.id,\
                   'dt_msg':message.date, 'msg':msg, 'photo':name_file})

@router.message(ZaiavkaFilter(text_zaiavka))
async def cmd_zaiavka(message: Message, bot: Bot, state: FSMContext):
    msg=message.text
    appendRequest({'full_name':message.from_user.full_name, 'user_id':message.from_user.id,\
                   'dt_msg':message.date, 'msg':msg, 'photo':None})
    await message_answer_safe(
        message,
        "заявка доставлена"
        )

#F.text == «Привет» — текст сообщения равен «Привет»;
#F.text != «Пока!» — текст сообщения не равен «Пока!»;
#F.text.contains («Привет») — текст сообщения содержит слово «Привет»;
#F.text.lower().contains («привет») — текст сообщения в малом регистре содержит слово «привет»;
#F.text.startswith («Привет») — текст сообщения начинается со слова «Привет»;
#F.text.endswith («дружище») — текст сообщения заканчивается словом «дружище».

if __name__ == "__main__":
    pass
    #main()
