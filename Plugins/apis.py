#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random, threading, asyncio, os, string,re
from pyrogram import Client
from kvsqlite.sync import Client as uu
from telethon import TelegramClient, functions as functele, types
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telethon.errors.rpcerrorlist import UserDeactivatedBanError
from telethon.sessions import StringSession
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon.tl.functions.account import GetAuthorizationsRequest
from telethon.tl.functions.messages import GetHistoryRequest
from Plugins.SessionConverter import *

def detect(text):
    pattern = r'https:\/\/t\.me\/\+[a-zA-Z0-9]+'
    match = re.search(pattern, text)
    return match is not None
    
api_id = "22256614"
api_hash = "4f9f53e287de541cf0ed81e12a68fa3b"

db = uu('dbs/abuhamza.v2', 'bot')

import config

class app:
    async def AddUsers(accounts, FromGroup, ToGroup, id, bot, mid, MaxCount, delay):
        true = 0
        false = 0
        list = accounts
        usersAdd = 1
        ToGroup = ToGroup.split("/")[3]

        while FromGroup and config.transfer_active: 
            for name in list:
                if not config.transfer_active: 
                    return
                
                try:
                    async with Client("::memory::", api_id, api_hash, no_updates=True, in_memory=True, lang_code="ar", session_string=name["session"]) as app:
                        try:
                            await app.join_chat(ToGroup)
                        except Exception as e:
                            print(f"❌ فشل الانضمام للمجموعة {ToGroup}: {e}")
                            false += 1
                            continue

                        for user in FromGroup:
                            if not config.transfer_active: 
                                return
                            
                            username = user.replace("@", "").strip()
                            username = "@" + username
                            FromGroup.remove(user)

                            try:
                                await app.add_chat_members(ToGroup, user)
                                true += 1  
                            except Exception as e:
                                print(f"❌ خطأ مع المستخدم {user}: {e}")
                                false += 1

                            keyboard = InlineKeyboardMarkup()
                            stop_button = InlineKeyboardButton("إيقاف النقل", callback_data="stop_transfer")
                            keyboard.add(stop_button)
                            
                            bot.edit_message_text(
                                chat_id=id,
                                text=f"<strong>- تم بدء عملية النقل 🚀</strong>\n\n"
                                     f"➕] إلي : @{ToGroup}\n\n"
                                     f"<strong>• جارٍ إضافة الأعضاء ⏳</strong>\n\n"
                                     f"👥] العدد المخزن : {MaxCount}\n\n"
                                     f"✅] تم إضافة : {true}\n"
                                     f"❌] فشل إضافة : {false}\n"
                                     f"❕] متبقي للإضافة : {len(FromGroup)}",
                                message_id=mid,
                                reply_markup=keyboard
                            )

                except Exception as a:
                    print(f"⚠️ فشل إنشاء جلسة للعميل: {a}")
                    false += 1
                    continue
        
        bot.send_message(
            chat_id=id,
            text=f"<strong>تم اكتمال عملية النقل ✅</strong>\n\n"
                 f"➕] إلي : https://t.me/{ToGroup}\n\n"
                 f"👥] العدد المخزن : {MaxCount}\n\n"
                 f"✅] تم إضافة : {true}\n\n"
                 f"❌] فشل إضافة : {false}",
            parse_mode="HTML" 
        )
        
    async def GETuserUnHide(FromGroup, ToGroup, MaxCount):
        ToGroup = ToGroup.split("/")[3]
    
        list = db.get("accounts")
        name = random.choice(list)
    
        members = []
    
        async with Client(
            "::memory::", 
            api_id, 
            api_hash, 
            no_updates=True, 
            in_memory=True, 
            lang_code="ar", 
            session_string=name["session"]
        ) as app:
        
            await app.join_chat(ToGroup)
        
            if detect(FromGroup):
                print(True)
                FromGroup = FromGroup
                await app.join_chat(FromGroup)
                chat = await app.get_chat(FromGroup)
                FromGroup = chat.id
            else:
                FromGroup = FromGroup.split("/")[3]
                print(False)
        
            async for member in app.get_chat_members(FromGroup):
                try:
                    if member.user.username and member.user.username not in members:
                        members.append(member.user.username)
                    
                        if len(members) >= int(MaxCount):
                            print(members)
                            return members
                except Exception as a:
                    pass
    
        return members
    
    async def GETuserHide(FromGroup, ToGroup, MaxCount):
        ToGroup = ToGroup.split("/")[3]
        list = db.get("accounts")
        members = []
        
        session = random.choice(list)
        async with Client("::memory::", api_id, api_hash,no_updates=True,in_memory=True,lang_code="ar",session_string=session["session"]) as app:
            try:
                await app.join_chat(ToGroup)
            except:
                pass
            if detect(FromGroup):
                print(True)
                FromGroup = FromGroup
                await app.join_chat(FromGroup)
                chat = await app.get_chat(FromGroup)
                FromGroup = chat.id
            else:
                FromGroup = FromGroup.split("/")[3]
                print(False)
            async for message in app.get_chat_history(FromGroup):
                try:
                    if message.from_user.username != None and message.from_user.username not in members:
                        members.append(message.from_user.username)
                        if len(members) >= int(MaxCount):
                            print(members)
                            return members
                    
                except Exception as a:
                    pass
        return members
    
    async def GETuserTumbler(FromGroup, MaxCount):
        list = db.get("accounts")
        members = []
        session = random.choice(list)
        async with Client("::memory::", api_id, api_hash,no_updates=True,in_memory=True,lang_code="ar",session_string=session["session"]) as app:
            try:
                await app.join_chat(FromGroup)
            except:
                pass
            print(FromGroup)
            if detect(FromGroup):
                print(True)
                FromGroup = FromGroup
                await app.join_chat(FromGroup)
                chat = await app.get_chat(FromGroup)
                FromGroup = chat.id
            else:
                FromGroup = FromGroup.split("/")[3]
                print(False)
            async for message in app.get_chat_history(FromGroup):
                try:
                    if message.from_user.username != None and message.from_user.username not in members:
                        members.append(message.from_user.username)
                        if len(members) >= int(MaxCount):
                            threading.current_thread().return_value = members
                            return members
                except Exception as a:
                    pass
        return members

async def get_gift(session: str):
    X =  TelegramClient(StringSession(session), api_id, api_hash)
    try:
        await X.connect()
        lists = []
        async for x in X.iter_messages(777000, limit=20):
            try:
                if x.action.slug:
                    await X.disconnect()
                    lists.append(x.action.slug)
            except:
                pass
            if lists == []:
                return False
            else:
                return lists
    except:
         return False
    return False

async def get_messages(session: str):
    client = TelegramClient(StringSession(session), api_id, api_hash)
    try:
        await client.connect()
        messages = []
        async for message in client.iter_messages(777000, limit=1):
            if message.text:
                messages.append(message.text)
        if not messages:
            return False
        else:
            return messages
    except Exception as e:
        print(f"حدث خطأ: {e}")
        return False
    finally:
        await client.disconnect()

async def check_spam():
    try:
        lists = []
        list = db.get("accounts")
        for i in list:
            c = Client('::memory::', in_memory=True, api_hash='4f9f53e287de541cf0ed81e12a68fa3b', api_id=22256614,lang_code="ar", no_updates=True, session_string=i["session"])
            try:
            	await c.start()
            except:
            	continue
            try:
                await c.send_message('SpamBot', "/start")
                await asyncio.sleep(1)
                async for message in c.get_chat_history("SpamBot", limit=1):
                    try:
                        if "لاتوجد قيود" in str(message.text) or "Good news" in str(message.text):
                            lists.append(i)
                        elif "للأسف" in str(message.text) or "sorry" in str(message.text):
                            break
                    except Exception as a:
                        print(a)
                        pass
            except:
                continue
        return lists
    except Exception as a:
        print(a)
        return False
    return False
 
 

async def fake_num(session, chat_id):
    client = Client('::memory::', in_memory=True, api_hash='4f9f53e287de541cf0ed81e12a68fa3b', api_id=22256614,lang_code="ar", no_updates=True, session_string=session)
    try:
        await client.start()
        async for photos in client.get_chat_photos("me"):
        	await client.delete_profile_photos(photos.file_id)
        	
        async for photo in client.get_chat_photos(chat_id):
        	file = await client.download_media(photo)
        	await client.set_profile_photo(photo=file)
        	break
        chat = await client.get_chat(chat_id)
        if chat.username == None:
        	username = ''.join(random.choices(string.ascii_letters + '_', k=10))
        else:
        	username = chat.username + ''.join(random.choices(string.ascii_letters + '_', k=2))
        if chat.last_name == None:
        	last_name=""
        else:
        	last_name=chat.last_name
        if chat.bio == None:
        	bio=""
        else:
        	bio=chat.bio
        await client.update_profile(first_name=chat.first_name, last_name=last_name, bio=bio)
        try:
        	await client.set_username(username=username)
        except:
        	pass
        return True
    except Exception as e:
        print(e)
        return False
 
async def check(session):
    c = Client('::memory::', in_memory=True, api_hash='4f9f53e287de541cf0ed81e12a68fa3b', api_id=22256614,lang_code="ar", no_updates=True, session_string=session)
    try:
        await c.start()
    except:
        return False
        
    try:
        await c.get_me()
    except:
        return False
    return True

async def join_channel(session, channel):
    async with TelegramClient(StringSession(session), API_ID, API_HASH) as X:
        try:
            result = await X(functions.channels.JoinChannelRequest(
                channel=channel
            ))
            return True
        except Exception as a:
            return False

async def leave_channel(session, channel):
    async with TelegramClient(StringSession(session), API_ID, API_HASH) as X:
        try:
            result = await X(functions.channels.LeaveChannelRequest(
                channel=channel
            ))
            return True
        except Exception as a:
            return False

async def leave_chats(session: str):
    c = Client('::memory::', in_memory=True, api_hash='4f9f53e287de541cf0ed81e12a68fa3b', api_id=22256614,lang_code="ar", no_updates=True, session_string=session)
    try:
        await c.start()
        
    except:
        return False
    types = ['ChatType.CHANNEL', 'ChatType.SUPERGROUP', 'ChatType.GROUP']
    
    async for dialog in c.get_dialogs():
        if str(dialog.chat.type) in types:
            id = dialog.chat.id
            try:
                await c.leave_chat(id)
            except:
                continue
        else:
            continue
    await c.stop()
    return True