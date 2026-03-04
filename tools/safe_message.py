from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError
from aiogram.exceptions import TelegramBadRequest
from aiogram.exceptions import TelegramNetworkError

from tools.save import save_blocks_unknown, save_blocks_user, save_blocks_admin, save_error, save_notchat_unknown, save_notchat_user, save_notchat_admin
from settings import Settings

def answer_safe(func):
    async def wrap(*args, **kwargs):
        message=args[0]
        res=None
        try:
            res=await func(*args, **kwargs)
        except TelegramForbiddenError as e:
            msg = str(e)
            if msg.find('bot was blocked by the user')>0:
                save_blocks(message.from_user.id)
                Settings.users_block.append(message.from_user.id)
            else:
                save_error("TelegramForbiddenError ошибка в safe_message.py->bot_message_safe\n"+str(e))
        except TelegramBadRequest as e:
            msg = str(e)
            if msg.find('chat not found')>0:
                save_notchat(message.from_user.id)
                Settings.users_notchat.append(message.from_user.id)
            else:
                save_error("TelegramBadRequest ошибка в safe_message.py->bot_message_safe\n"+str(e))
        except TelegramNetworkError as e:
            msg = str(e)
            save_error("TelegramNetworkError ошибка в safe_message.py->answer_safe\n"+msg)
        except Exception as e:
            #pass
            save_error("неизвестная ошибка в safe_message.py->bot_message_safe\n"+str(e))
        return res
    return wrap


@answer_safe
async def message_answer_safe(
    message, text,
    parse_mode=None,
    reply_markup=None,
    disable_web_page_preview=None,
    disable_notification=False,
    reply_to_message_id=None,
    timeout=None):
    return await message.answer(text, parse_mode=parse_mode, reply_markup=reply_markup)


def save_blocks(id):
    if int(id) in Settings.admin_id:
        save_blocks_admin(id)
    elif str(id) in Settings.users.keys():
        save_blocks_user(id)
    else:
        save_blocks_unknown(id)


def save_notchat(id):
    if int(id) in Settings.admin_id:
        save_notchat_admin(id)
    elif str(id) in Settings.users.keys():
        save_notchat_user(id)
    else:
        save_notchat_unknown(id)
    

def bot_safe(func):
    async def wrap(*args, **kwargs):
        id=args[1]
        res=None
        try:
            message_res=await func(*args, **kwargs)            
            res = [message_res, 0]            
        except TelegramForbiddenError as e:
            msg = str(e)
            if msg.find('bot was blocked by the user')>0:
                save_blocks(id)
                Settings.users_block.append(id)
                res = [None, 1]
            else:
                save_error("TelegramForbiddenError ошибка в safe_message.py->bot_safe\n"+msg)
                res = [None, 2]
        except TelegramBadRequest as e:
            msg = str(e)
            if msg.find('chat not found')>0:
                save_notchat(id)
                Settings.users_notchat.append(id)
                res = [None, 3]
            elif msg.find('wrong remote file identifier specified')>0:
                res = [None, 4]
            elif msg.find('PHOTO_INVALID_DIMENSIONS')>0:
                res = [None, 5]
            else:
                save_error("TelegramBadRequest ошибка в safe_message.py->bot_safe\n"+msg)
                res = [None, 6]
        except TelegramNetworkError as e:
            msg = str(e)
            save_error("TelegramNetworkError ошибка в safe_message.py->bot_safe\n"+msg)
            res = [None, 7]
        except Exception as e:
            msg = str(e)            
            save_error("неизвестная ошибка в safe_message.py->bot_safe\n"+msg)
            res = [None, 8]
        return res
    return wrap

@bot_safe
async def bot_message_safe(bot, id, text,
                           parse_mode=None,
                           reply_markup=None,
                           disable_web_page_preview=None,
                           disable_notification=False,
                           reply_to_message_id=None,
                           timeout=None,
                           reply_markup2=None):
    await bot.send_message(id, text, parse_mode, reply_markup=reply_markup2)#get_users_kb())


@bot_safe
async def bot_send_photo_safe(bot, id, image,
                              parse_mode2=None,
                              caption2=None,
                              reply_markup2=None):
    return await bot.send_photo(id, image, caption=caption2, parse_mode=parse_mode2, reply_markup=reply_markup2)


@bot_safe
async def bot_send_video_safe(bot, id, image,
                              parse_mode2=None,
                              caption2=None,
                              reply_markup2=None):
    return await bot.send_video(id, image, caption=caption2, parse_mode=parse_mode2, reply_markup=reply_markup2)

    
@bot_safe
async def bot_send_doc_safe(bot, id, doc,
                              parse_mode2=None,
                              caption2=None,
                              reply_markup2=None):
    return await bot.send_document(id, doc, caption=caption2, parse_mode=parse_mode2, reply_markup=reply_markup2)
