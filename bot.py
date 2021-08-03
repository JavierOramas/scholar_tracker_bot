#! /root/anaconda3/bin/python
import os
from pyrogram import Client, filters
from read_config import read_config
import json

def read_data(id):
    id = str(id)

    try:
        with open('db/'+id+'.json', 'r') as f:
            return json.loads(f.readline())
    except:
        return {}
    
def write_data(id,db):
    id = str(id)
    with open('db/'+id+'.json', 'w') as f:
        f.write(json.dumps(db))

config_data = read_config('./config/config_bot.json')
app = Client(config_data['bot_user_name'], config_data['api_id'], config_data['api_hash'])

@app.on_message(filters.command('add'))
def see_fee(client, message):
    users = message.text.split()
    scholar_id = str(app.get_users([users[-1]])[0]['id'])
    owner_id = str(app.get_users([users[-2]])[0]['id'])
    
    db = read_data(message.chat.id)
 
    # print(owner_id in db.keys())
    if not owner_id in db.keys():
        db[owner_id] = []
    if not scholar_id in db[owner_id]:
        db[owner_id].append(scholar_id)
        write_data(message.chat.id,db)

    pass

@app.on_message(filters.command('get'))
def see_fee(client, message):
    users = message.text.split()
    owner_id = str(app.get_users([users[-1]])[0]['id'])
    
    db = read_data(message.chat.id)

    if owner_id in db.keys():
        scholars = app.get_users(db[owner_id])
        msg = ''
        
        for i in scholars:
            msg += '@'+str(i['username'])+'\n'
        message.reply_text('scholars de '+users[-1]+':\n'+msg)    
    else:
        message.reply_text(users[-1]+' no tiene scholars :(')
    pass

@app.on_message(filters.command('getall'))
def see_fee(client, message):
    users = message.text.split()
    # owner_id = str(app.get_users([users[-1]])[0]['id'])
    
    db = read_data(message.chat.id)

    for owner_id in db.keys():
        username = '@'+app.get_users(owner_id)['username']
        scholars = app.get_users(db[owner_id])
        msg = ''
        
        for i in scholars:
            msg += '@'+str(i['username'])+'\n'
        message.reply_text('scholars de '+username+':\n'+msg)    
    pass

@app.on_message(filters.command('owner'))
def see_fee(client, message):
    users = message.text.split()
    scholar_id = str(app.get_users([users[-1]])[0]['id'])
    
    db = read_data(message.chat.id)

    for i in db.keys():
        
        scholars = db[i]
        
        if scholar_id in scholars:
            username = app.get_users(i)['username']
            msg = '@'+username+' es su dueño'
            message.reply_text(msg)    
            return
    
    message.reply_text(users[-1]+' es libre como el viento :)')
    pass

@app.on_message(filters.command('free'))
def see_fee(client, message):
    users = message.text.split()
    scholar_id = str(app.get_users([users[-1]])[0]['id'])
    
    db = read_data(message.chat.id)

    for i in db.keys():
        
        scholars = db[i]
        
        if scholar_id in scholars:
            db[i].remove(scholar_id)
            msg = users[-1]+' ha roto las cadenas de la esclavitud, Felicidades!!!'
            message.reply_text(msg)    
            return
    
    pass

@app.on_message(filters.command('help'))
@app.on_message(filters.command('start'))
def help(client, message):
    
    message.reply_text("""Puedes contribuir con el desarrollo aqui: https://github.com/JavierOramas/\no puedes donar para contribuir al desarrollo: 0x64eF391bb5Feae6023440AD12a9870062dd2B342
""")
    pass

app.run()