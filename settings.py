from aiogram import Bot

from tools.read import read2list, read_users, read_send_media, read_token

class Settings:
    token: str = ''
    users = {}
    #users_block = []
    #users_notchat = []
    #send_media = []
    #received = []
    #admins_block = []
    #queue_send_video = deque()
    #send_video = []
    db_path = "./messages.db3"
    bot:object

def fillSettings():
    Settings.users = read_users()
    Settings.token = read_token()


fillSettings()

Settings.bot = Bot(Settings.token)

