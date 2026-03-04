import json
import pickle

from datetime import datetime

from settings import Settings


def save(message: str, file:str):
        f=open(file, 'w', encoding='utf-8')
        f.write(message+"\n")
        f.close()
    

def save_append(message: str, file:str):
        with open(file, 'a', encoding='utf-8') as f:
                f.write(message+"\n")


#def save_map2json(obj:dict, file:str):
#        with open(file, 'w', encoding='utf-8') as f:
#                json.dump(obj, f, ensure_ascii=False)


def save_map2pkl(obj:dict, file:str):
        with open(file, 'wb', encoding='utf-8') as f:
                pickle.dump(obj, f)


#def save_users(users:dict):
#        return save_map2json(dict, 'users.json')


def save_dict2json(obj:dict, file:str):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False)    

def save_users(obj:dict):
    save_dict2json(obj, 'users.json')

#def save_blocks(id:int):
#        if int(id) in Settings.admin_id:
#                f=open("blocks_admin.txt", 'a', encoding='utf-8')
#                f.write(str(id)+"\n")
#                f.close()
#        elif str(id) in Settings.users.keys():
#                f=open("blocks_user.txt", 'a', encoding='utf-8')
#                f.write(str(id)+"\n")
#                f.close()
#        else:
#                f=open("blocks_user2.txt", 'a', encoding='utf-8')
#                f.write(str(id)+"\n")
#                f.close()


def save_blocks_admin(id:int):
        with open("blocks_admin.txt", 'a', encoding='utf-8') as f:
                f.write(str(id)+"\n")


def save_blocks_user(id:int):
        with open("blocks_user.txt", 'a', encoding='utf-8') as f:
                f.write(str(id)+"\n")


def save_blocks_unknown(id:int):
        with open("blocks_unknown.txt", 'a', encoding='utf-8') as f:
                f.write(str(id)+"\n")


def save_notchat_admin(id:int):
        with open("blocks_notchat_admin.txt", 'a', encoding='utf-8') as f:
                f.write(str(id)+"\n")


def save_notchat_user(id:int):
        with open("blocks_notchat_user.txt", 'a', encoding='utf-8') as f:
                f.write(str(id)+"\n")


def save_notchat_unknown(id:int):
        with open("blocks_notchat_unknown.txt", 'a', encoding='utf-8') as f:
                f.write(str(id)+"\n")


def save_error(text:str):
        save_append(text, 'errors.txt')


def save_start(text:str):
        save(text, 'users_start.txt')

def save_message_media(id_user, path_media, id_message = None):
        if str(id_user in Settings.users.keys()):
                fio = Settings.users[str(id_user)]["fio"]
        else:
                fio = 'Неизвестный'
        dt = datetime.now().strftime("%Y-%b-%d %H:%M")
        Settings.send_media.append({
                'fio':fio,
                'id_msg':id_message,
                'id_user':int(id_user),
                'time': dt,
                'path': path_media
                })
        if (len(Settings.send_media) > 100):
                Settings.send_media = Settings.send_media[-50:]
        text='{"fio":"' + str(fio) + '","id_msg":' + str(id_message) + ', "id_user":'+str(id_user)+', "time":"'+str(dt)+'", "path":"'+path_media+'"}'
        save_append(text, 'lof_media.txt')

