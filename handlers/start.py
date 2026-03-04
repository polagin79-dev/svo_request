from aiogram import Router
from aiogram import Bot
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
#from aiogram import html
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

from tools.save import save_start
from settings import Settings
from tools.safe_message import message_answer_safe
from admins.control_panel import add_new_user, send_admins


router = Router()
    
@router.message(Command("start"))  
async def cmd_start(message: Message, bot: Bot, state: FSMContext):
    save_start(str(message.from_user.id)+" "+message.from_user.full_name+" "+str(message.date))
    if not str(message.from_user.id) in Settings.users.keys():
        add_new_user(message.from_user.id, message.from_user.full_name, message.date)
        text_admin = "новый пользователь\nid:" + str(message.from_user.id)+\
                     '\nfull_name:'+str(message.from_user.full_name)+\
                     '\nдата входа:'+str(message.date)
        await send_admins(bot, text_admin)
        msg = await message_answer_safe(
            message,
            #f"Привет, {html.bold(html.quote(message.from_user.full_name))}",
            f"Привет\nознакомься с документом",
            parse_mode=ParseMode.HTML,
            reply_markup=ReplyKeyboardRemove()
            )
    else:
        full_name = Settings.users[str(message.from_user.id)]['full_name']
        msg = await message_answer_safe(
            message,
            #f"Привет, {html.bold(html.quote(full_name))}\n",
            f"Привет",
            parse_mode=ParseMode.HTML,
            reply_markup=ReplyKeyboardRemove()
            )
    await state.clear()
