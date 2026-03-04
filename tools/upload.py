import os

idx = 0

def get_new_name_photo()->str:
    global idx
    idx = idx + 1
    name = 'PHOTO/' + str(idx) + '.jpg'
    while (os.path.exists(name)):
        idx = idx + 1
        name = 'PHOTO/' + str(idx) + '.jpg'
    return name
