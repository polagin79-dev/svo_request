import os
import json
import pickle


# читает файл в список
def read2list(file):
    if not os.path.exists(file):
        return []
    # открываем файл в режиме чтения utf-8
    file = open(file, 'r', encoding='utf-8')

    # читаем все строки и удаляем переводы строк
    lines = file.readlines()
    lines = [line.rstrip('\n') for line in lines]

    file.close()

    return lines

def read_json2dict(file:str)->dict:
    data = {}
    if not os.path.exists(file):
        return data
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def read_pkl2map(file:str)->dict:
    data = {}
    if not os.path.exists(file):
        return data
    with open(file, 'rb', encoding='utf-8') as f:
        data = pickle.load(f)
    return data

def read_users()->dict:
    return read_json2dict('users.json')

def read_token()->dict:
    lists=read2list("token.txt")
    return lists[0]

def read_send_media()->list:
    path=os.path.abspath('lof_media.txt')
    if not os.path.exists(path):
        return []
    rows=read2list(path)
    send_media=[]
    for row in rows:
        d=json.loads(row)
        send_media.append(d)
    return send_media
