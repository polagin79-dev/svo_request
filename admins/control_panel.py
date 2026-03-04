from aiogram import Bot
from aiogram.types import Message
from aiogram.enums.chat_member_status import ChatMemberStatus

from settings import Settings
from tools.save import save_users
from tools.safe_message import bot_message_safe

async def is_admin(message: Message, bot: Bot):
    member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    bot = await bot.get_chat_member(message.chat.id, bot.id)
    if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR] or bot.status != ChatMemberStatus.ADMINISTRATOR:
        return False
    return True


#admins=[]
#admins.append("5221532379")


def notification_error_admin(func):
    async def wrap(*args, **kwargs):
        #print('notification_error_admin: start')
        #bot=args[0]
        bot = Settings.bot
        Settings.users_block = []
        res=await func(*args, **kwargs)
        #print('notification_error_admin: res=', res)
        users_block_copy = Settings.users_block[:]
        Settings.users_block = []
        msg_u = 'пользователь заблокирован'
        msg_a = 'администратор заблокирован'
        while len(users_block_copy)>0:
            for id_block in users_block_copy:
                for id_admin in Settings.admin_id:
                    if int(id_block) != int(id_admin):
                        info=get_info(id_block)
                        if int(id_block) in Settings.admin_id:
                            await bot_message_safe(bot, id_admin, msg_a+info+', id='+str(id_block))
                        else:
                            await bot_message_safe(bot, id_admin, msg_u+info+', id='+str(id_block))
            users_block_copy = Settings.users_block[:]
        #Settings.users_block = []
        users_notchat_copy = Settings.users_notchat[:]
        Settings.users_notchat = []
        msg_u = 'не найден чат с пользователем'
        msg_a = 'не найден чат с администратором'
        while len(users_notchat_copy)>0:
            for id_notchat in users_notchat_copy:
                for id_admin in Settings.admin_id:
                    if int(id_notchat) != int(id_admin):
                        info=get_info(id_notchat)
                        if int(id_notchat) in Settings.admin_id:
                            await bot_message_safe(bot, id_admin, msg_a+info+', id='+str(id_notchat))
                        else:
                            await bot_message_safe(bot, id_admin, msg_u+info+', id='+str(id_notchat))
            users_notchat_copy = Settings.users_notchat[:]
        #print('notification_error_admin: res=', res)
        return res
    return wrap


async def send_admins(bot: Bot, text: str):    
    for id in Settings.admin_id:
        #await bot.send_message(id, text)
        #print(id)
        await bot_message_safe(bot, id, text)
        #await bot.send_message(id, text, reply_markup=get_reg_kb())


def add_new_user(id_a:str, full_name_a:str, msg_date)->str:
    if Settings.users.get(id_a, 1) != 1:
        return "BUSY"
    #Settings.users[str(id_a)] = dict(full_name = full_name_a, fio = fio_a)
    #Settings.users[str(id_a)] = dict(zip(list(full_name_a), list(fio_a)))
    Settings.users[str(id_a)] = {"full_name":str(full_name_a), "date_reg":str(msg_date), "signal":'UNKNOWN'}
    save_users(Settings.users)
    return "OK"    


def get_info(id):
    #print(id)
    #print(Settings.users)
    #print(id in Settings.users)
    if id in Settings.users:
        fio=Settings.users[str(id)]['fio']
        return '('+fio+') '
    else:
        return ''
    #text = Settings.users.get(id,'')


@notification_error_admin
async def send_message_all(bot: Bot, text: str,
                           parse_mode=None,
                           reply_markup2=None,
                           disable_web_page_preview=None,
                           disable_notification=False,
                           reply_to_message_id=None,
                           timeout=None):
    for id in Settings.users.keys():
        #await bot.send_message(id, text, reply_markup=get_users_kb())
        await bot_message_safe(bot, id, text, reply_markup=reply_markup2)



