#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, certifi

if not os.path.isdir('dbs'):
    os.mkdir('dbs')

from pyrogram import Client,errors
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton as btn
from telebot.types import InlineKeyboardMarkup as mk
from telebot.types import KeyboardButton as kb
from telebot.types import ReplyKeyboardMarkup as rep
import threading
from telebot import types
import asyncio
from Plugins.apis import *
from Plugins.SessionConverter import *
from kvsqlite.sync import Client as uu
import zipfile
import time
import re
from telethon import TelegramClient
from telethon.sessions import StringSession
from telebot import TeleBot, types
from pyrogram import Client
from pyrogram import Client, errors
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import config                     

if not os.path.isdir('dbs'):
    os.mkdir('dbs')

db_path = 'dbs/abuhamza.v2'
db_folder = 'dbs/'
db = uu('dbs/abuhamza.v2', 'bot')

if not db.exists("accounts"):
    db.set("accounts", [])
App = app()

sudo = 7598650992

api_id = '22256614'
api_hash = '4f9f53e287de541cf0ed81e12a68fa3b'

TELEGRAM_TOKEN = "000000" 

back = rep(row_width=2, resize_keyboard=True)

bot = telebot.TeleBot(TELEGRAM_TOKEN, threaded=False, num_threads=55, skip_pending=True, parse_mode="html", disable_web_page_preview=True)
print(bot)

@bot.message_handler(commands=['start'])
def Admin(message):
    if message.chat.id != sudo:
        return
    
    markup = InlineKeyboardMarkup(row_width=2)
    
    accs = db.get("accounts")
    
    btn0 = InlineKeyboardButton("حذف حساب", callback_data="show")
    btn1 = InlineKeyboardButton("اضف حساب", callback_data="number")
    btn3 = InlineKeyboardButton("مغادرة من الكل", callback_data="confirm_logout")
    btn4 = InlineKeyboardButton("رفع نسخه", callback_data="upload_backup")
    btn5 = InlineKeyboardButton("نسخه احتياطيه", callback_data="fetch_backup")
    btn2 = InlineKeyboardButton(f"عدد حساباتك : {len(accs)}", callback_data="account_count")
    btn6 = InlineKeyboardButton("تنظيف الحسابات", callback_data="clean_accounts")
    telmber = InlineKeyboardButton("تحويل تلمبر", callback_data="telmber")
    getgift = InlineKeyboardButton("جلب مميز", callback_data="get_gift")
    btn7 = InlineKeyboardButton("نقل مخفي", callback_data="move_hidden")
    btn8 = InlineKeyboardButton("نقل ظاهر", callback_data="move_visible")
    stop = InlineKeyboardButton("ايقاف النقل", callback_data="stop_transfer")
    accget = InlineKeyboardButton("سحب حساب", callback_data="accget")
    
    
    markup.add(btn2)
    markup.add(btn0, btn1)
    markup.add(accget)
    markup.add(telmber, getgift)
    markup.add(btn8, btn7)
    markup.add(btn3, btn6)
    markup.add(stop)
    markup.add(btn5)
    
    bot.send_message(message.chat.id, """مرحبا بك عزيزي المستخدم في بوت نقل اعضاء المطور \n\n• تحكم من الازرار الموجودة بالاسفل""", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("accountdr_"))
def handle_account_selection(call):
    account_index = int(call.data.split('_')[1])
    load_ = db.get('accounts')
    account = load_[account_index]
    
    keyboard = [
        [InlineKeyboardButton(text="حذف الحساب", callback_data=f"delete_{account_index}")],
        [InlineKeyboardButton(text="رجــوع 🔙", callback_data="show")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=(
            f"📞 **حساب :** {account['phone_number']}\n\n"
            "اختر من الخيارات أدناه لإجراء العملية المطلوبة."
        ),
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("show"))
def show_accounts(call):   
    load_ = db.get('accounts')
    if len(load_) == 0:
        bot.send_message(call.message.chat.id, "⚠️ لا توجد حسابات مسجلة.")
        return
    
    keyboard = []
    for i in range(0, len(load_), 2):
        row = []
        row.append(
            InlineKeyboardButton(
                text=f"{load_[i]['phone_number']}",
                callback_data=f"accountdr_{i}"
            ))
        if i + 1 < len(load_):
            row.append(
                InlineKeyboardButton(
                    text=f"{load_[i + 1]['phone_number']}",
                    callback_data=f"accountdr_{i + 1}"
                ))
        keyboard.append(row)
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="📑 هذه قائمة بالحسابات المسجلة في البوت \n\n- اضغط على زر الحساب لإدارة جلسته.",
        reply_markup=reply_markup
    )    

@bot.callback_query_handler(func=lambda call: call.data.startswith("accget"))
def show_accounts(call):
    accounts = db.get("accounts") or []
    
    if not accounts:
        bot.send_message(call.message.chat.id, "⚠️ لا يوجد حسابات مضافة بعد")
        return
    
    markup = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(acc["phone_number"], callback_data=f"accountsfd_{i}")
        for i, acc in enumerate(accounts)
    ]
    markup.add(*buttons)
    
    bot.send_message(call.message.chat.id, "🗃] قائمة بحساباتك المضافة في البوت\n\n- اضغط على زر الحساب الذي تريد سحبه من البوت:", reply_markup=markup)

from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client
from pyrogram.raw.functions.account import GetAuthorizations, ResetAuthorization
import re
import asyncio

@bot.callback_query_handler(func=lambda call: call.data.startswith("sdsds_zxscs_"))
def show_sessions(call):
    index = int(call.data.split("_")[2])
    accounts = db.get("accounts") or []
    
    if index >= len(accounts):
        bot.answer_callback_query(call.id, "❌ الحساب غير موجود!")
        return
    
    acc = accounts[index]
    session = Client("temp_session", api_id=api_id, api_hash=api_hash, session_string=acc["session"])
    session.connect()
    
    try:
        active_sessions = session.invoke(GetAuthorizations())
        
        if not active_sessions.authorizations:
            bot.answer_callback_query(call.id, "⚠️ لا توجد جلسات نشطة لهذا الحساب.")
            return
        
        markup = InlineKeyboardMarkup(row_width=1)
        for i, session_info in enumerate(active_sessions.authorizations):
            session_name = f"{session_info.device_model} - {session_info.ip}"
            markup.add(InlineKeyboardButton(session_name, callback_data=f"dcaads_salak_{index}_{i}"))
        
        markup.add(InlineKeyboardButton("خروج جلسة البوت", callback_data=f"ggttt_ggff_ddaa_{index}"))
        
        markup.add(InlineKeyboardButton("رجوع", callback_data=f"accountsfd_{index}"))
        
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="🗂] الجلسات النشطة لهذا الحساب\n\n- اختر جلسة لتسجيل الخروج منها",
            reply_markup=markup
        )
    
    finally:
        session.disconnect()

@bot.callback_query_handler(func=lambda call: call.data.startswith("ggttt_ggff_ddaa_"))
def logout_bot_session(call):
    index = int(call.data.split("_")[3])
    accounts = db.get("accounts") or []
    
    if index >= len(accounts):
        bot.answer_callback_query(call.id, "❌ الحساب غير موجود!")
        return
    
    acc = accounts[index]
    
    try:
        # إنشاء كائن Client جديد
        session = Client("temp_session", api_id=api_id, api_hash=api_hash, session_string=acc["session"])
        session.connect()
        
        # تسجيل خروج جلسة البوت
        session.log_out()
        
        # إرسال رسالة تأكيد
        bot.answer_callback_query(call.id, "✅ تم تسجيل خروج جلسة البوت بنجاح.")
        
        # تحديث الرسالة الحالية
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="🗂] تم تسجيل خروج جلسة البوت بنجاح.",
            reply_markup=None  # إزالة لوحة المفاتيح
        )
    
    except Exception as e:
        bot.answer_callback_query(call.id, f"❌ فشل في تسجيل الخروج: {str(e)}")
    
    finally:
        # إغلاق الكائن Client بعد الانتهاء
        if 'session' in locals() and session.is_connected:
            session.disconnect()

@bot.callback_query_handler(func=lambda call: call.data.startswith("dcaads_salak_"))
def logout_session(call):
    data = call.data.split("_")
    account_index = int(data[2])
    session_index = int(data[3]) 
    
    accounts = db.get("accounts") or []
    
    if account_index >= len(accounts):
        bot.answer_callback_query(call.id, "❌ الحساب غير موجود!")
        return
    
    acc = accounts[account_index]
    session = Client("temp_session", api_id=api_id, api_hash=api_hash, session_string=acc["session"])
    session.connect()
    
    try:
        active_sessions = session.invoke(GetAuthorizations())
        
        if session_index >= len(active_sessions.authorizations):
            bot.answer_callback_query(call.id, "❌ الجلسة غير موجودة!")
            return
        
        session_hash = active_sessions.authorizations[session_index].hash
        session.invoke(ResetAuthorization(hash=session_hash))
        bot.answer_callback_query(call.id, "✅ تم تسجيل الخروج من الجلسة بنجاح.")
        
        show_sessions(call)
    
    finally:
        session.disconnect()

@bot.callback_query_handler(func=lambda call: call.data.startswith("accountsfd_"))
def account_details(call):
    index = int(call.data.split("_")[1])
    accounts = db.get("accounts") or []
    
    if index >= len(accounts):
        bot.answer_callback_query(call.id, "❌ الحساب غير موجود!")
        return
    
    acc = accounts[index]
    
    if acc["two-step"] != "None":
        two_step_status = f"`{acc['two-step']}`"
    else:
        two_step_status = "غير مفعل ❌"
    
    markup = InlineKeyboardMarkup()
    get_code_btn = InlineKeyboardButton("📩 جلب الكود", callback_data=f"getcode_{index}")
    show_sessions_btn = InlineKeyboardButton("🗂 عرض الجلسات", callback_data=f"sdsds_zxscs_{index}")
    roh = InlineKeyboardButton("رجوع", callback_data=f"accget")
    markup.add(get_code_btn, show_sessions_btn)
    markup.add(roh)
    
    msg = f"📱 **الرقم :** `{acc['phone_number']}`\n🔐 **التحقق بخطوتين :** {two_step_status}\n\n❗ حاول تسجيل دخول بالرقم على تطبيق تليجرام ثم اضغط على زر **جلب الكود**"
    bot.send_message(call.message.chat.id, msg, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("getcode_"))
def get_support_code(call):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
    index = int(call.data.split("_")[1])
    accounts = db.get("accounts") or []

    if index < 0 or index >= len(accounts):
        bot.answer_callback_query(call.id, "❌ الحساب غير موجود!")
        return

    acc = accounts[index]

    session = Client("temp_session", api_id=api_id, api_hash=api_hash, session_string=acc["session"])
    session.connect()

    try:
        messages = session.get_chat_history(777000, limit=1)

        for msg in messages:
            if msg.text:
                match = re.search(r'\b\d{4,5}\b', msg.text)
                if match:
                    keyboard = InlineKeyboardMarkup()
                    keyboard.add(InlineKeyboardButton("سحب حساب اخر", callback_data="accget"))
                    keyboard.add(InlineKeyboardButton("خروج جلسة البوت", callback_data="ggttt_ggff_ddaa_{index}"))

                    bot.send_message(
                        call.message.chat.id,
                        f"**تم جلب الكود بنجاح** ✅\n\n- الكود : `{match.group()}`",
                        parse_mode="Markdown",
                        reply_markup=keyboard
                    )
                else:
                    bot.send_message(call.message.chat.id, "⚠️ لم يتم العثور على كود تحقق صحيح.")
                return

        bot.send_message(call.message.chat.id, "⚠️ لم يتم العثور على كود تحقق من تيليجرام.")

    finally:
        session.disconnect()

@bot.callback_query_handler(func=lambda call: call.data.startswith("delete_"))
def delete_account(call):
    account_index = int(call.data.split('_')[1])
    load_ = db.get('accounts')
    account = load_[account_index]
    
    load_.remove(account)
    db.set("accounts", load_)
    
    bot.send_message(call.message.chat.id, "🗑 تم حذف الحساب بنجاح.")

@bot.callback_query_handler(func=lambda call: call.data == "stop_transfer")
def stop_transfer(call):
    if not config.transfer_active:
        bot.answer_callback_query(call.id, text="⚠️ عملية النقل متوقفة بالفعل")
    else:
        config.transfer_active = False 
        bot.answer_callback_query(call.id, text="✅ تم إيقاف عملية النقل")
        
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="❌ **تم إلغاء عملية النقل بنجاح**",
            parse_mode="Markdown"
        )
    
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    message = call.message
    
    if message.chat.id != sudo:
        return 
    bot.clear_step_handler(message)
    cid, data, = message.from_user.id, message.text
    if call.data == 'fetch_backup':
        temp_zip_path = "AbuHamza.zip"
        db_folder = "dbs" 
    
        with zipfile.ZipFile(temp_zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for filename in os.listdir(db_folder):
                file_path = os.path.join(db_folder, filename)
                if os.path.isfile(file_path):
                    zipf.write(file_path, arcname=filename)  
    
        with open(temp_zip_path, "rb") as zip_file:
            bot.send_document(call.message.chat.id, zip_file, caption="📂] نسخه احتياطيه لحساباتك في البوت")
    
        os.remove(temp_zip_path)
    
    if call.data == 'clean_accounts':
        true, false = 0, 0
        cx = bot.send_message(call.message.chat.id, f"<strong>جاري تنظيف الحسابات 🔍</strong>\n\n✅] حسابات تعمل : {true}\n⚠️] حسابات لا تعمل : {false}")
        load_ = db.get('accounts')
        count = 0
        for i in load_:
            x = asyncio.run(check(i['session']))
            if x is True:
                true += 1
            else:
                false += 1
                load_.remove(i)
                db.set("accounts", load_)
            count += 1
            if count % 30 == 0:
                bot.edit_message_text(chat_id=call.message.chat.id, text=f"<strong>- جاري تنظيف الحسابات 🔍</strong>\n\n✅] حسابات تعمل : {true}\n⚠️] حسابات لا تعمل : {false}", message_id=cx.message_id)
        bot.edit_message_text(chat_id=call.message.chat.id, text=f"<strong>تم تنظيف الحسابات ✅</strong>\n\n✅] حسابات تعمل : {true}\n⚠️] حسابات لا تعمل : {false}", message_id=cx.message_id) 
   
    if call.data == 'confirm_logout':
        msg = bot.send_message(call.message.chat.id, '• تم بدء مغادرة كل المجموعات بنجاح ✅')
        acc = db.get('accounts')
        true = 0
        for amount in acc:
            try:
                o = asyncio.run(leave_chats(amount["session"]))
                true += 1
            except Exception as e:
                continue
            bot.edit_message_text(chat_id=call.message.chat.id, text=f'• تم بنجاح الخروج من كل المجموعات \n• تم الخروج من <code>{true}</code> حساب بنجاح ✅', message_id=msg.message_id)
            
    if call.data == "number":
        x = bot.reply_to(message, "📞] ارسل الرقم مع الترميز الدولي +", reply_markup=back)
        bot.register_next_step_handler(x, AddAccounts)
        
    if call.data == "ssessions":
        keyboard = InlineKeyboardMarkup(row_width=2)
        url_button = InlineKeyboardButton(text="استخراج كود الجلسة", url="https://telegram.tools/session-string-generator#pyrogram,user")
        keyboard.add(url_button)
        x = bot.reply_to(message, "⚡] ارسل كود جلسة الحساب \n\n📛] يجب استخراجه من الزر الموجود بالاسفل", reply_markup=keyboard)
        bot.register_next_step_handler(x, AddAccount)
        
    if call.data == "add_account":
        keyboard = InlineKeyboardMarkup(row_width=2)
        number = InlineKeyboardButton(text="رقم هاتف", callback_data="number")
        sessions = InlineKeyboardButton(text="جلسة", callback_data="ssessions")
        keyboard.add(number, sessions)
        x = bot.reply_to(message, "⚡] اختر نوع التسجيل الذي تريده \n\n- اذا كان الحساب جديد اضغط على زر جلسة \n\n- اذا كان الحساب منذ 3 اشهر اضغط رقم هاتف", reply_markup=keyboard)
        
    if call.data == "move_visible":
        x = bot.reply_to(message, "➖] ارسل رابط الجروب المراد النقل منه", reply_markup=back)
        bot.register_next_step_handler(x, FromGroupDef)
     
    if call.data == "move_hidden":
        x = bot.reply_to(message, "➖] ارسل رابط الجروب المراد النقل منه", reply_markup=back)
        bot.register_next_step_handler(x, FromHiddenGroupDef)
        
    if call.data == "telmber":
        x = bot.reply_to(message, "🌆] ارسل رابط الجروب المراد تحويل الحسابات منه", reply_markup=back)
        bot.register_next_step_handler(x, tumbler)
        
    if data == "get_gift":
        x = bot.reply_to(message, '- تم بدا جلب روابط المميز من الحسابات برجاء انتظار اشعار', reply_markup=back)
        acc = db.get("accounts")
        count = 0
        for i in acc:
            Convert_sess = MangSession.PYROGRAM_TO_TELETHON(i["session"])
            x = asyncio.run(get_gift(Convert_sess))
            mkk = isinstance(x, list)
            if x != False and mkk is True:
                gifts = db.get("gifts") if db.exists("gifts") else []
                for ii in x:
                    if ii not in gifts:
                        text = f"<strong>• رابط تليجرام مميز جديد 🥳</strong>\n\n- الرابط : https://t.me/giftcode/{ii}\n- رقم الهاتف : {i['phone']}"
                        count += 1
                        bot.send_message(chat_id=cid, text=text, parse_mode="html")
                        gifts.append(ii)
                        db.set("gifts", gifts)
        bot.send_message(chat_id=sudo, text=f"- تم الانتهاء من فحص الحسابات تم ايجاد {count} روابط")
        
def FromHiddenGroupDef(message):
    if message.text == "/start" or message.text == "رجوع":
        return messages(message)
    x = bot.send_message(chat_id=message.chat.id,text="➕] ارسل رابط الجروب المراد النقل اليه .", reply_markup=back)
    bot.register_next_step_handler(x, MaxHiddenDef, message.text)

def MaxHiddenDef(message, FromGroup):
    if message.text == "/start" or message.text == "رجوع":
        return messages(message)
    x = bot.send_message(chat_id=message.chat.id,text="👥] ارسل عدد الاعضاء التي تريد نقلهم", reply_markup=back)
    bot.register_next_step_handler(x, TimeToAdd, FromGroup, message.text)

def TimeToAdd(message, FromGroup, ToGroup):
    if message.text == "/start" or message.text == "رجوع":
        return messages(message)
    MaxCount = message.text
    x = bot.send_message(chat_id=message.chat.id,text=f"⏱️] ارسل الفاصل الزمني بين كل عملية نقل\n\n- اذا تريده فوري ارسل 0", reply_markup=back)
    bot.register_next_step_handler(x, ToHiddenGroupDef, FromGroup, ToGroup, MaxCount)

def ToHiddenGroupDef(message, FromGroup, ToGroup, MaxCount):
    if message.text == "/start" or message.text == "رجوع":
        return messages(message)
    
    try:
        if int(message.text) == 0:
            timeToAdd = 0
        else:
            fir = int(message.text) * 60
            timeToAdd = int(MaxCount) / int(fir)
            print(timeToAdd)
    except:
        return bot.reply_to(message, "⚠️] ارسل الوقت بأرقام فقط")
    
    accs = len(db.get('accounts'))
    msg = bot.reply_to(message, "⏳] جاري فحص الحسابات المحظورة قبل بدء عملية النقل")
    
    result = asyncio.run(check_spam())
    if result is False:
        bot.edit_message_text(text="❌ حدث خطأ أثناء عملية فحص الحسابات. تم إيقاف عملية النقل", 
                              chat_id=message.from_user.id, message_id=msg.message_id)
        return
    else:
        accounts = len(result)
        if accounts == 0:
            bot.edit_message_text(text="⚠️] للأسف، تم إلغاء عملية النقل لأن كل الحسابات محظورة عام", 
                                  chat_id=message.from_user.id, message_id=msg.message_id)
            return
        else:
            bot.edit_message_text(text=f"<strong>- تم انتهاء عملية الفحص بنجاح ✅</strong>\n\n"
                                       f"- عدد الحسابات السليمة : {accounts}\n"
                                       f"- عدد الحسابات المحظورة : {accs - accounts}", 
                                  chat_id=message.from_user.id, message_id=msg.message_id)
    
    config.transfer_active = True
    msg = bot.send_message(chat_id=message.chat.id, text="جارٍ التجهيز لعملية النقل ⏳")
    
    list = asyncio.run(app.GETuserHide(FromGroup, ToGroup, MaxCount))
    numUser = len(list)
    true, false = 0, 0
    
    keyboard = InlineKeyboardMarkup()
    stop_button = InlineKeyboardButton("إيقاف النقل", callback_data="stop_transfer")
    keyboard.add(stop_button)

    x = bot.edit_message_text(
        chat_id=message.from_user.id, 
        text=f"<strong>- تم تخزين الأعضاء بنجاح ✅</strong>\n\n"
             f"👥] تم تخزين : {MaxCount}\n"
             f"✅] متعرف عليهم : {numUser}\n\n"
             f"- من مجموعة : {FromGroup}\n"
             f"➕] المجموعة المستضيفة : {ToGroup}\n\n"
             f"<strong>⏳] جارٍ متابعة نقل الأعضاء</strong>\n\n"
             f"✅] تم إضافة : {true}\n"
             f"❌] فشل إضافة : {false}", 
        message_id=msg.message_id,
        reply_markup=keyboard
    )
    
    if config.transfer_active:
        threading.Thread(target=lambda: asyncio.run(app.AddUsers(result, list, ToGroup, message.chat.id, bot, x.message_id, MaxCount, timeToAdd))).start()
    else:
        bot.send_message(chat_id=message.chat.id, text="❌ تم إلغاء عملية النقل.")
    
def FromGroupDef(message):
    if message.text == "/start" or message.text == "رجوع":
        return messages(message)
    x = bot.send_message(chat_id=message.chat.id,text="➕] ارسل رابط الجروب المراد النقل اليه .", reply_markup=back)
    bot.register_next_step_handler(x, MaxDef, message.text)

def MaxDef(message, FromGroup):
    if message.text == "/start" or message.text == "رجوع":
        return messages(message)
    x = bot.send_message(chat_id=message.chat.id,text="👥] ارسل عدد الاعضاء التي تريد نقلها", reply_markup=back)
    bot.register_next_step_handler(x, TimeToAdd2, FromGroup, message.text)

def TimeToAdd2(message, FromGroup, ToGroup):
    if message.text == "/start" or message.text == "رجوع":
        return messages(message)
    MaxCount = message.text
    x = bot.send_message(chat_id=message.chat.id,text=f"⏱️] ارسل الفاصل الزمني بين كل عملية نقل\n- ارسل عدد الوقت بالدقائق ، اذا تريده فوري ارسل 0", reply_markup=back)
    bot.register_next_step_handler(x, ToGroupDef, FromGroup, ToGroup, MaxCount)

def ToGroupDef(message, FromGroup, ToGroup, MaxCount):
    if message.text == "/start" or message.text == "رجوع":
        return messages(message)
    
    try:
        if int(message.text) == 0:
            timeToAdd = 0
        else:
            fir = int(message.text) * 60
            timeToAdd = int(MaxCount) / int(fir)
            print(timeToAdd)
    except:
        return bot.reply_to(message, "⚠️] ارسل الوقت بارقام فقط")
    
    msg = bot.reply_to(message, "⏳] جاري فحص الحسابات المحظورة قبل اتمام عملية النقل")
    accs = len(db.get('accounts'))
    result = asyncio.run(check_spam())
    
    if result is False:
        bot.edit_message_text(text="❌ حدث خطأ أثناء عملية فحص الحسابات. تم إيقاف عملية النقل", 
                              chat_id=message.from_user.id, message_id=msg.message_id)
        return
    else:
        accounts = len(result)
        if accounts == 0:
            bot.edit_message_text(text="⚠️] للأسف، تم إلغاء عملية النقل لأن كل الحسابات محظورة عام", 
                                  chat_id=message.from_user.id, message_id=msg.message_id)
            return
        else:
            bot.edit_message_text(text=f"<strong>تم انتهاء عملية الفحص بنجاح ✅</strong>\n\n"
                                       f"✅] حسابات سليمة : {accounts}\n"
                                       f"❌] حسابات محظورة : {accs - accounts}", 
                                  chat_id=message.from_user.id, message_id=msg.message_id)
    
    config.transfer_active = True
    msg = bot.reply_to(message, "🚀] جارٍ التجهيز لعملية النقل")
    
    list = asyncio.run(app.GETuserUnHide(FromGroup, ToGroup, MaxCount))
    numUser = len(list)
    true, false = 0, 0

    keyboard = InlineKeyboardMarkup()
    stop_button = InlineKeyboardButton("إيقاف النقل", callback_data="stop_transfer")
    keyboard.add(stop_button)
    
    x = bot.edit_message_text(
        chat_id=message.from_user.id, 
        text=f"<strong>تم بدء عملية النقل</strong>\n\n"
             f"👥] العدد المطلوب : {MaxCount}\n"
             f"🗃] تم تخزين : {numUser}\n\n"
             f"➖] من : {FromGroup}\n"
             f"➕] إلي : {ToGroup}\n\n"
             f"<strong>⏳] جارٍ إضافة الأعضاء</strong>\n\n"
             f"✅] تم إضافة : {true}\n"
             f"❌] فشل إضافة : {false}", 
        message_id=msg.message_id,
        reply_markup=keyboard
    )

    if config.transfer_active:
        threading.Thread(target=lambda: asyncio.run(app.AddUsers(result, list, ToGroup, message.chat.id, bot, x.message_id, MaxCount, timeToAdd))).start()
    else:
        bot.send_message(chat_id=message.chat.id, text="❌ تم إلغاء عملية النقل.")
    
def AddAccount(message):
    if message.text == "/start" or message.text == "رجوع":
        return messages(message)
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        if "1" in message.text or ":" in message.text: 
            session_string = message.text.strip() 
            _client = Client(
                "::memory::", 
                api_id=api_id,
                api_hash=api_hash,
                session_string=session_string,
                device_model="Dev Salah : @PTS27",
                system_version="Dev Salah : @PTS27",
                app_version="11.4.2",
                lang_code="en"
            )
            try:
                _client.connect() 
                
                if _client.is_connected:
                    bot.send_message(
                        message.chat.id,
                        "✅ تم تسجيل الدخول بنجاح باستخدام كود الجلسة!")
                    _client.disconnect() 
                else:
                    bot.send_message(
                        message.chat.id,
                        "❌ فشل تسجيل الدخول! يرجى التحقق من كود الجلسة.",
                        reply_markup=back
                    )
            except Exception as e:
                bot.send_message(
                    message.chat.id,
                    f"⚠️ حدث خطأ أثناء تسجيل الدخول: {str(e)}",
                    reply_markup=back
                )
        else:
            bot.send_message(
                message.chat.id,
                "⚠️ صيغة كود الجلسة غير صحيحة. يرجى إرسال كود الجلسة الصحيح.",
                reply_markup=back
            )
    except Exception as e:
        bot.send_message(message.chat.id, "ERORR : " + str(e))


def AddAccounts(message):
    if message.text == "/start" or message.text == "رجوع":
        return messages(message)
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        if "+" in message.text:
            session_name = f"session_{message.chat.id}_{int(time.time())}"
            _client = Client(
                session_name, 
                api_id=api_id,
                api_hash=api_hash,
                device_model="Salah Hemdan",
                system_version="User : @PTS27",
                app_version="11.4.2",
                lang_code="en"
            )
            _client.connect()
            SendCode = _client.send_code(message.text)
            Mas = bot.send_message(
                message.chat.id,
                "💬] تم ارسال رمز تحقق للحساب ... ارسله لي",
                reply_markup=back
            )
            bot.register_next_step_handler(
                Mas, sigin_up, _client, message.text, SendCode.phone_code_hash, message.text
            )
        else:
            Mas = bot.send_message(
                message.chat.id,
                "⚠️] صيغة الرقم غير صحيحه .. ارسله بهذا الشكل \n+20121100000",
                reply_markup=back
            )
    except Exception as e:
        bot.send_message(message.chat.id, "ERORR : " + str(e)) 

def sigin_up(message, _client, phone, hash, name):
    if message.text == "/start" or message.text == "رجوع":
        return messages(message)
    try:
        bot.send_message(message.chat.id, "⏳] جاري الفحص")
        _client.sign_in(phone, hash, message.text)
        
        markup = InlineKeyboardMarkup(row_width=2)
        salahh = InlineKeyboardButton("اضف حساب اخر", callback_data="number")
        markup.add(salahh)
        
        bot.send_message(message.chat.id, "✅] تم تسجيل الحساب بنجاح", reply_markup=markup)
        
        ses = _client.export_session_string()
        data = {"phone_number": name, "two-step": "None", "session": ses}
        accounts = db.get("accounts")
        accounts.append(data)
        db.set("accounts", accounts)
    except errors.SessionPasswordNeeded:
        Mas = bot.send_message(message.chat.id, "🔐] هذا الحساب محمي بالتحقق بخطوتين .. ارسل كلمة سر التحقق بخطوتين")
        bot.register_next_step_handler(Mas, AddPassword, _client, name)
    except Exception as e:
        print(f"Error during sign-in: {e}")
        bot.send_message(message.chat.id, f"ERORR : {e}")

def AddPassword(message, _client, name):
    if message.text == "/start" or message.text == "رجوع":
        return messages(message)
    try:
        _client.check_password(message.text)
        
        markup = InlineKeyboardMarkup(row_width=2)
        btn00 = InlineKeyboardButton("اضف حساب اخر", callback_data="number")
        markup.add(btn00)
        
        bot.send_message(message.chat.id, "✅] تم تسجيل الحساب بنجاح", reply_markup=markup)
        
        ses = _client.export_session_string()
        data = {"phone_number": name, "two-step": message.text, "session": ses}
        accounts = db.get("accounts")
        accounts.append(data)
        db.set("accounts", accounts)
    except Exception as e:
        print(f"Error during password addition: {e}")
        bot.send_message(message.chat.id, f"❌] التحقق بخطوتين غلط ")
    
def tumbler(message):
    if message.text == "/start" or message.text == "رجوع":
        return messages(message)
    load_ = db.get('accounts')
    cid = message.from_user.id
    msg = bot.send_message(chat_id=cid, text=f"- جارً سحب بيانات المستخدمين من الجروب بعدد {len(load_)} مستخدم.")
    list = asyncio.run(app.GETuserTumbler(message.text, len(load_)))
    bot.edit_message_text(chat_id=cid ,message_id=msg.message_id, text=f"• تم اكتمال سحب بيانات {len(list)}")
    true, false = 0, 0
    xx = bot.send_message(chat_id=cid, text=f"• تم بدء تحويل الحسابات تمبلر 🚀\n\n✅] تم تحويل : {true}\n❌] فشل تحويل : {false}")
    load_ = db.get('accounts')
    for i in load_:
        user = random.choice(list)
        x = asyncio.run(fake_num(i["session"], user))
        list.remove(user)
        if x is True:
            true += 1
            bot.edit_message_text(chat_id=cid ,message_id=xx.message_id, text=f"• تم بدء تحويل الحسابات تمبلر 🚀\n\n✅] تم تحويل : {true}\n❌] فشل تحويل : {false}")
        else:
            false += 1
            bot.edit_message_text(chat_id=cid ,message_id=xx.message_id, text=f"• تم بدء تحويل الحسابات تمبلر 🚀\n\n✅] تم تحويل : {true}\n❌] فشل تحويل : {false}")
    x = bot.send_message(chat_id=cid, text=f"• تم الانتهاء من تحويل الحسابات بالكامل")

def logout_all_sessions_except_bot(phone_number, session_string):
    try:
        client = TelegramClient(StringSession(session_string), api_id, api_hash)
        client.connect()

        if not client.is_user_authorized():
            return False

        client.log_out(except_self=True)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        client.disconnect()
    
bot.infinity_polling(none_stop=True,timeout=15, long_polling_timeout =15)