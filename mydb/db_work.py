import os
import sqlite3
from datetime import date
from settings import Settings

name_db = Settings.db_path #'messages.db3'

def CreateDB():
    if os.path.exists(name_db):
        return
    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()
    cursor.execute('''
CREATE TABLE IF NOT EXISTS requests (
id INTEGER PRIMARY KEY,
user_id TEXT NOT NULL,
full_name TEXT NOT NULL,
dt_msg INTEGER NOT NULL,
doc_msg TEXT DEFAULT NULL,
msg TEXT DEFAULT NULL,
photo TEXT DEFAULT NULL,
status TEXT NOT NULL,
operator_id TEXT DEFAULT '',
operator_full_name TEXT DEFAULT '')
''')
    conn.commit()
    conn.close()

def getUnprocessedRequestText():
    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()
    query = 'SELECT user_id, full_name, dt_msg, doc_msg, msg, id FROM requests WHERE (status == "DELIVERED" and photo is NULL)'
    cursor.execute(query)
    rows = cursor.fetchall()
    rows_d=[]
    for row in rows:
        rows_d.append({'user_id':row[0], 'full_name':row[1], 'dt_msg':row[2],\
                       'doc_msg':row[3], 'msg':row[4], 'id':row[5]})
    conn.commit()
    conn.close()
    return rows_d

def getUnprocessedRequestPhoto():
    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()
    query = 'SELECT user_id, full_name, dt_msg, doc_msg, msg, photo, id FROM requests WHERE ((status == "DELIVERED") and (NOT photo is NULL))'
    cursor.execute(query)
    rows = cursor.fetchall()
    rows_d=[]
    for row in rows:
        rows_d.append({'user_id':row[0], 'full_name':row[1], 'dt_msg':row[2],\
                       'doc_msg':row[3], 'msg':row[4], 'photo':row[5], 'id':row[6]})
    conn.commit()
    conn.close()
    return rows_d

def getPeriodText(d):
    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()
    query = 'SELECT user_id, full_name, dt_msg, doc_msg, msg, id FROM requests WHERE (dt_msg >= "' + str(d) + '" and photo is NULL)'
    cursor.execute(query)
    rows = cursor.fetchall()
    rows_d=[]
    for row in rows:
        rows_d.append({'user_id':row[0], 'full_name':row[1], 'dt_msg':row[2],\
                       'doc_msg':row[3], 'msg':row[4], 'id':row[5]})
    conn.commit()
    conn.close()
    return rows_d

def getPeriodPhoto(d):
    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()
    query = 'SELECT user_id, full_name, dt_msg, doc_msg, msg, photo, id FROM requests WHERE ((dt_msg >= "' + str(d) + '") and (NOT photo is NULL))'
    cursor.execute(query)
    rows = cursor.fetchall()
    rows_d=[]
    for row in rows:
        rows_d.append({'user_id':row[0], 'full_name':row[1], 'dt_msg':row[2],\
                       'doc_msg':row[3], 'msg':row[4], 'photo':row[5], 'id':row[6]})
    conn.commit()
    conn.close()
    return rows_d

def markProcessing(rows:list, operator_id:str, operator_full_name:str):
    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()
    for row in rows:
        query = 'UPDATE requests SET status="PROCESSING", ' + \
                'operator_id="' + str(operator_id) + '", ' + \
                'operator_full_name="' + str(operator_full_name) + '"' + \
                'WHERE id=' + str(row['id'])
        cursor.execute(query)
    conn.commit()
    conn.close()

def appendRequest(request:dict):
    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()
    if request['photo'] == None:
        cursor.execute('INSERT INTO requests(user_id, full_name, dt_msg, status) VALUES (?, ?, ?, ?)', \
                       (request['user_id'], request['full_name'], request['dt_msg'], 'DELIVERED'))
    else:
        cursor.execute('INSERT INTO requests(user_id, full_name, dt_msg, photo, status) VALUES (?, ?, ?, ?, ?)', \
                       (request['user_id'], request['full_name'], request['dt_msg'], request['photo'], 'DELIVERED'))
    last_id=cursor.lastrowid
    if request['msg'] != None:
        cursor.execute('UPDATE requests SET msg="' + request['msg'] +\
                       '"WHERE id=' + str(last_id))
    if request['photo'] != None:
        cursor.execute('UPDATE requests SET doc_msg="' + request['photo'] +\
                       '"WHERE id=' + str(last_id))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    testMain()
