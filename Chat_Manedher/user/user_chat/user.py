from user.Midllvary import rate_limit, ThrottlingMiddleware 
from create_bot import bot, dp
from config import ignore
from database.start import base, cur

from aiogram import types, executor, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from math import floor
import time
import asyncio
import datetime
import random

'''*******************************************Func*****************************************************************'''

#async def balance(size):
#
#	lvl = floor(int(size)/100) + 1
#	a = int(lvl) * -10
#	random_du = random.randint(a,20)
#	size_up = int(size) + random_du
#
#	if size_up <= 0:
#		random_du = random.randint(1,20)
#		size_up = int(size) + random_du
#
#	balance = [lvl, size_up, random_du]
#
#	return balance
#
#async def items(random_items, user_id, lucky):
#	if random_items <= 90 and random_items >= 80:
#		comment = '\nВи отримали: "💪".'
#
#		frihand = cur.execute('SELECT frihand FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
#		frihand = frihand[0]
#		frihand = int(frihand) + (1 * int(lucky))
#
#		cur.execute('UPDATE inventory SET frihand == ? WHERE user_id == ?', (frihand, user_id))
#		base.commit()
#
#	elif random_items <= 80 and random_items >= 75:
#		comment = '\nВи отримали: "⛽".'
#
#		pump = cur.execute('SELECT pump FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
#		pump = pump[0]
#		pump = int(pump) + (1 * int(lucky))
#
#		cur.execute('UPDATE inventory SET pump == ? WHERE user_id == ?', (pump, user_id))
#		base.commit()
#
#	elif random_items == 74:
#		comment = '\nВи отримали: "🧴".'
#
#		grease = cur.execute('SELECT grease FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
#		grease = grease[0]
#		grease = int(grease) + (1 * int(lucky))
#
#		cur.execute('UPDATE inventory SET grease == ? WHERE user_id == ?', (grease, user_id))
#		base.commit()
#
#	elif random_items == 70:
#		comment = '\nВи отримали: "🐰".'
#
#		rabot = cur.execute('SELECT rabot FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
#		rabot = rabot[0]
#		rabot = int(rabot) + 1
#
#		cur.execute('UPDATE inventory SET rabot == ? WHERE user_id == ?', (rabot, user_id))
#		base.commit()
#
#	else:
#		comment = " "
#
#	return comment


'''*******************************************Code*****************************************************************'''

# Commands "Start"
@rate_limit(5, 'start')
async def comand_start(message: types.Message):

	user_id = str(message.from_user.id)
	username = message.from_user.username
	first_name = message.from_user.first_name
	chat_id = str(message.chat.id)
	chat_name = message.chat.title

	dt = datetime.datetime.now()
	data = datetime.date.today()

	if str(user_id) in ignore:
		return

	try:
		a = await message.reply(f'Дякую за запуск <i><b><a href="tg://user?id={user_id}">{first_name}</a></b></i>. Я готовий!',  parse_mode='html')
	except:
		first_name = username
		if first_name == None:
			first_name = "Fredd"

		a = await message.reply(f'Дякую за запуск <i><b><a href="tg://user?id={user_id}">{first_name}</a></b></i>. Я готовий!',  parse_mode='html')

	print(a.to_python)
	if message.chat.type == "private": pass
	if message.chat.type == "group" or message.chat.type == "supergroup" or message.chat.type == "channel":

		#try:
		#	num = cur.execute('SELECT * FROM chatlist ORDER BY number_chat DESC').fetchmany(1)
		#	num = num[0]
		#	num = num[0]
		#	number_chat = int(num) + 1

		#except:
		#	number_chat = 1

		num = cur.execute('SELECT MAX(number_chat) FROM chatlist').fetchone()
		number_chat = num[0] + 1 if num[0] else 1

		if chat_name != None: chat_name = chat_name
		if chat_name == None: chat_id = NoneName
		try:
			#awalist = []
			#chat_list = cur.execute('SELECT * FROM chatlist').fetchmany(10000)

			#for x in chat_list:
			#	chat_id_bd = x[2]
			#	awalist.append(chat_id_bd)
			siz = cur.execute('SELECT chat_id FROM chatlist WHERE chat_id == ?', (chat_id,)).fetchone()
			siz = str(siz[0])

			if chat_id != siz:#not in awalist:
				cur.execute('INSERT INTO chatlist VALUES(?, ?, ?, ?)', (number_chat, chat_name, chat_id, data))
				base.commit()
				await bot.send_message(chat_id = 1101984099, text = f'<b>Nick</b>: <i><b><a href="tg://user?id={user_id}">{message.from_user.first_name}</a></b></i>.\n<b>Name</b>: {chat_name}.\n<b>Id</b>: {chat_id}.\n<b>Data</b>: {data}.',  parse_mode='html')
		except: pass

# Commands "Help"
@rate_limit(5, 'help')
async def help(message: types.Message):

	user_id = str(message.from_user.id)
	username = message.from_user.username
	first_name = message.from_user.first_name
	chat_id = str(message.chat.id)
	chat_name = message.chat.title

	markup = InlineKeyboardMarkup()
	button = InlineKeyboardButton(text="Про бота:", callback_data='btn1')
	button1 = InlineKeyboardButton(text="Команди:", callback_data='btn2')
	button2 = InlineKeyboardButton(text="Допомога автору:", callback_data='btn3')
	button3 = InlineKeyboardButton(text="Документація:", url='https://telegra.ph/Dokumentacіya-10-03')
	markup.add(button, button1).add(button2).add(button3)

	await message.reply("Ось ця інформація, має бути корисна для вас", reply_markup=markup)

#Button1
@dp.callback_query_handler(text = 'btn1')
@rate_limit(3, 'btn1')
async def but1(callback_query: types.CallbackQuery):
	await callback_query.message.answer('<i>Бот створений, щоб привнести хаус у ваш чат.</i>',  parse_mode='html')
	await callback_query.message.delete_reply_markup()

#Button2
@dp.callback_query_handler(text = 'btn2')
@rate_limit(3, 'btn2')
async def but2(callback_query: types.CallbackQuery):
	await callback_query.message.answer('<b>start</b> - <i>запуск бота</i>.\
	\n<b>help</b> - <i>допомога</i>.\
	\n<b>dickup</b> - <i>збільшити пипірку</i>.\
	\n<b>topdick</b> - <i>топ</i>.\
	\n<b>profile</b> - <i>профіль</i>.\
	\n<b>use</b> - <i>(предмет) використати предмет</i>.\
	\n<b>give</b> - <i>(кількість) (предмет) передати предмет</i>.\
	\n<b>buy</b> - <i>(кількість) (предмет) купити предмет</i>.\
	\n<b>mine</b> - <i>отримати <b>coin</b></i>.\
	\n<b>shop</b> - <i>каталог предметів</i>.\
	\n<b>sell</b> - <i>(число) (предмет) (ціна) продати на аукціон</i>.\
	\n<b>kauf</b> - <i>(id товару) покупка на аукціоні</i>.\
	\n<b>market</b> - <i>подивитись аукціон</i>.\
	\n<b>case</b> - <i>відкрити скриню</i>.\
	',  parse_mode='html')
	await callback_query.message.delete_reply_markup()

#Button3
@dp.callback_query_handler(text = 'btn3')
@rate_limit(3, 'btn3')
async def but3(callback_query: types.CallbackQuery):
	await callback_query.message.answer('<b><i>Якщо хочеш підтримати автора:</i></b>\
		<b>5168 7520 2402 4112</b>',  parse_mode='html')
	await callback_query.message.delete_reply_markup()

'''*******************************************dickup*****************************************************************'''

## Commands "DickUp"
#@rate_limit(2, 'dickup')
#async def dickup(message: types.Message):
#
#	user_id = str(message.from_user.id)
#	username = message.from_user.username
#	first_name = str(message.from_user.first_name)
#	chat_id = str(message.chat.id)
#	chat_name = message.chat.title
#	random_items = random.randint(0,100)
#
#	time_dickup_bd = int(time.time()) + int(1200)
#
#	lucky = 1
#	print_lk = " "
#
#
#	if str(user_id) in ignore:
#		return
#
#	#---rabot---
#	try:
#		rabot = cur.execute('SELECT rabot FROM effect WHERE user_id == ?', (user_id,)).fetchone()
#		rabot = int(rabot[0])
#
#		if random_items <= 90 and random_items >= 73 and rabot >= 0:
#
#			lucky = random.randint(2,4)
#
#			print_lk = f"\n<b>Удача</b>, ваші предмети збільшились у <b>{lucky}</b> раза."
#			rabot = rabot - 1
#
#			cur.execute('UPDATE effect SET rabot == ? WHERE user_id == ?', (rabot, user_id,))
#			base.commit()
#	except: pass
#
#	try:
#		size = cur.execute('SELECT size FROM size_table_dickup WHERE user_id == ?', (user_id,)).fetchone()
#		size = size[0]
#
#		try:
#			time_dickup = cur.execute('SELECT time_dickup FROM size_table_dickup WHERE user_id == ?', (user_id,)).fetchone()
#			time_dickup = time_dickup[0]
#	
#			if int(time_dickup) > int(time.time()):
#				raise SyntaxError(x)
#		except:
#
#			abc_time = int(time_dickup) - int(time.time())
#			m = floor(int(abc_time)/60) 
#			s = int(abc_time) - int(m*60) 
#	
#			if len(str(m)) < 2:
#				m = str(0) + str(m)
#	
#			if len(str(s)) < 2:
#				s = str(0) + str(s)
#	
#			await message.reply(f'Ви уже <b>збільшували пипірку</b>, наступний раз буде через <b>{m}:{s}</b>.',  parse_mode='html')
#			return
#
#	except:
#		size = 0
#	
#	#---grease---
#	try:
#		grease = cur.execute('SELECT grease FROM effect WHERE user_id == ?', (user_id,)).fetchone()
#		grease = int(grease[0])
#	
#		if grease >=1:
#			time_dickup_bd = int(time.time()) + int(300)
#			
#			grease = grease - 1
#
#			cur.execute('UPDATE effect SET grease == ? WHERE user_id == ?', (grease, user_id,))
#			base.commit()
#	except: pass
#
#	#func
#	balanc = await balance(size)
#	lvl = balanc[0]
#	size_up = balanc[1]
#	random_du = balanc[2]
#
#	#awalist = []
#	#size_list = cur.execute('SELECT * FROM size_table_dickup').fetchmany(10000)
#	#
#	#for x in size_list:
#	#	number_size = x[1]
#	#	awalist.append(number_size)
#
#	siz = cur.execute('SELECT user_id FROM size_table_dickup WHERE user_id == ?', (user_id,)).fetchone()
#	siz = siz[0]
#
#	if user_id != siz:#not in awalist:
#		cur.execute('INSERT INTO inventory VALUES(?, ?, ?, ?, ?, ?, ?)', (user_id, 200, 1, 1, 1, 0, 0))
#		base.commit()
#		cur.execute('INSERT INTO effect VALUES(?, ?, ?)', (user_id, 0, 0))
#		base.commit()
#		
#		try:
#			await message.reply(f'<i><b><a href="tg://user?id={user_id}">{first_name}</a></b></i> ви збільшили свою пипірку на <b>{random_du}</b> см.\nВаш новий рахунок: <b>{random_du}</b> см.',  parse_mode='html')
#			cur.execute('INSERT INTO size_table_dickup VALUES(?, ?, ?, ?, ?, ?)', (first_name, user_id, lvl, size_up, chat_id, time_dickup_bd,))
#			base.commit()
#			return
#		except:
#			first_name = username
#			if first_name == None:
#				first_name = "Fredd"
#
#			await message.reply(f'<i><b><a href="tg://user?id={user_id}">{first_name}</a></b></i> ви збільшили свою пипірку на <b>{random_du}</b> см.\nВаш новий рахунок: <b>{random_du}</b> см.',  parse_mode='html')
#			cur.execute('INSERT INTO size_table_dickup VALUES(?, ?, ?, ?, ?, ?)', (first_name, user_id, lvl, size_up, chat_id, time_dickup_bd,))
#			base.commit()
#			return
#		
#	cur.execute('UPDATE size_table_dickup SET size == ? WHERE user_id == ?', (size_up, user_id))
#	base.commit()
#	cur.execute('UPDATE size_table_dickup SET time_dickup == ? WHERE user_id == ?', (time_dickup_bd, user_id))
#	base.commit()
#
#	cur.execute('UPDATE size_table_dickup SET lvl == ? WHERE user_id == ?', (lvl, user_id))
#	base.commit()
#
#	#func
#	comment = await items(random_items, user_id, lucky)
#
#	text = f"<i><b>{first_name}</b></i>, ви збільшили свою пипірку на <b>{random_du}</b> см.\nВаш новий рахунок: <b>{size_up}</b> см.{comment}{print_lk}"
#
#	try:
#		await message.reply(f'{text}',  parse_mode='html')
#	except:
#		first_name = username
#		if first_name == None:
#			first_name = "Fredd"
#		await message.reply(f'{text}',  parse_mode='html')

'''*******************************************dickup2.0*****************************************************************'''

@rate_limit(2, 'dickup')
async def dickup(message: types.Message):
    user_id = str(message.from_user.id)
    username = message.from_user.username
    first_name = str(message.from_user.first_name)
    chat_id = str(message.chat.id)
    chat_name = message.chat.title
    random_items = random.randint(0, 100)

    time_dickup_bd = int(time.time()) + 1200

    lucky = 1
    print_lk = ""

    if user_id in ignore:
        return

    try:
        rabot = cur.execute('SELECT rabot FROM effect WHERE user_id == ?', (user_id,)).fetchone()
        rabot = int(rabot[0])

        if 73 <= random_items <= 90 and rabot >= 0:
            lucky = random.randint(2, 4)
            print_lk = f"\n<b>Удача</b>, ваші предмети збільшились у <b>{lucky}</b> раза."
            rabot -= 1
            cur.execute('UPDATE effect SET rabot == ? WHERE user_id == ?', (rabot, user_id,))
            base.commit()
    except:
        pass

    try:
        size, time_dickup = cur.execute('SELECT size, time_dickup FROM size_table_dickup WHERE user_id == ?',
                                        (user_id,)).fetchone()

        if int(time_dickup) > int(time.time()):
            abc_time = int(time_dickup) - int(time.time())
            m = str(abc_time // 60).zfill(2)
            s = str(abc_time % 60).zfill(2)
            await message.reply(f'Ви уже <b>збільшували пипірку</b>, наступний раз буде через <b>{m}:{s}</b>.',
                                parse_mode='html')
            return
    except:
        size = 0

    try:
        grease = cur.execute('SELECT grease FROM effect WHERE user_id == ?', (user_id,)).fetchone()
        grease = int(grease[0])

        if grease >= 1:
            time_dickup_bd = int(time.time()) + 300
            grease -= 1
            cur.execute('UPDATE effect SET grease == ? WHERE user_id == ?', (grease, user_id,))
            base.commit()
    except:
        pass

    lvl = (int(size) // 100) + 1
    a = int(lvl) * -10
    random_du = random.randint(a, 20)
    size_up = int(size) + random_du

    if size_up <= 0:
        random_du = random.randint(1, 20)
        size_up = int(size) + random_du

    siz = cur.execute('SELECT user_id FROM size_table_dickup WHERE user_id == ?', (user_id,)).fetchone()
    siz = siz[0]

    if user_id != siz:
        cur.execute('INSERT INTO inventory VALUES(?, ?, ?, ?, ?, ?, ?)', (user_id, 200, 1, 1, 1, 0, 0))
        base.commit()
        cur.execute('INSERT INTO effect VALUES(?, ?, ?)', (user_id, 0, 0))
        base.commit()

        try:
            await message.reply(
                f'<i><b><a href="tg://user?id={user_id}">{first_name}</a></b></i> ви збільшили свою пипірку на <b>{random_du}</b> см.\nВаш новий рахунок: <b>{random_du}</b> см.',
                parse_mode='html')
        except:
            pass
        return

    cur.execute('UPDATE size_table_dickup SET size == ?, time_dickup == ? WHERE user_id == ?',
                (size_up, time_dickup_bd, user_id,))
    base.commit()

    comment = await items(random_items, user_id, lucky)

    await message.reply(f'<i><b><a href="tg://user?id={user_id}">{first_name}</a></b></i> ви збільшили свою пипірку на <b>{size_up}</b>.{print_lk}{comment}',
                        parse_mode='html')


async def items(random_items, user_id, lucky):
    items_dict = {
        80: ("💪", "frihand"),
        75: ("⛽", "pump"),
        74: ("🧴", "grease"),
        70: ("🐰", "rabot")
    }

    if random_items in items_dict:
        comment, item_key = items_dict[random_items]
        item_value = cur.execute(f'SELECT {item_key} FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
        item_value = item_value[0]
        item_value = int(item_value) + (1 * int(lucky))
        cur.execute(f'UPDATE inventory SET {item_key} == ? WHERE user_id == ?', (item_value, user_id))
        base.commit()
    else:
        comment = ""

    return comment

# Commands "topdick"
@rate_limit(2, 'topdick')
async def topdick(message: types.Message):

	#first_name, user_id, size integer, chat_id, time_dickup integer

	user_id = str(message.from_user.id)
	username = message.from_user.username
	chat_id = str(message.chat.id)
	chat_name = message.chat.title

	if str(user_id) in ignore:
		return

	topdick = cur.execute('SELECT * FROM size_table_dickup ORDER BY size DESC').fetchmany(10)

	a = 0

	awalist = []
	for x in topdick:
		a += 1
		lc1 = x[0]
		lc2 = x[1]
		lc3 = x[3]

		awalist.append((f'<b>{a})</b><b>{lc1}</b> === <b>{lc3}</b> см;'))
	awatitle = '\n'.join(map(''.join,awalist))
	await message.answer(awatitle,  parse_mode='html')

'''*******************************************profile/use*****************************************************************'''

# Commands "profile"
@rate_limit(2, 'profile')
async def profile(message: types.Message):

	user_id = str(message.from_user.id)
	username = message.from_user.username
	first_name = message.from_user.first_name
	chat_id = str(message.chat.id)
	chat_name = message.chat.title

	#<b>{a})</b><b>{lc1}</b> === <b>{lc3}</b> см;
	#inventory(user_id, frihand, lvl)

	if str(user_id) in ignore:
		return
	try:
		size = cur.execute('SELECT size FROM size_table_dickup WHERE user_id == ?', (user_id,)).fetchone()
		lc3 = cur.execute('SELECT lvl FROM size_table_dickup WHERE user_id == ?', (user_id,)).fetchone()
		inventory = cur.execute('SELECT * FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
		effect = cur.execute('SELECT * FROM effect WHERE user_id == ?', (user_id,)).fetchone()

		size = size[0]
		lc3 = lc3[0]

		x = inventory
		e = effect

		lc1 = x[0]
		lc2 = x[1]
		lc4 = x[2]
		lc5 = x[3]
		lc6 = x[4]
		lc7 = x[5]

		ef1 = e[1]
		ef2 = e[2]

		if username == None:
			username = "Fredd"

		title = f'<b>Ваш Профіль</b>\n\
			Nick: <i><b><a href="tg://user?id={user_id}">{username}</a></b></i>\n\
			Lvl: <b>{lc3}</b>\n\
			Coin: <b>{lc2}</b>\n\
			Size: <b>{size}</b>\n\
			------------------------------\n\
			<i>Frihand 💪</i> == <b>{lc4}</b>\n\
			<i>Pump ⛽</i> == <b>{lc5}</b>\n\
			<i>Grease 🧼</i> == <b>{lc6}</b>\n\
			<i>Rabot 🐰</i> == <b>{lc7}</b>\n\
			------------------------------\n\
			<i>grease</i> °= <b>{ef1}</b>\n\
			<i>rabot</i> °= <b>{ef2}</b>\n\
			------------------------------\n\
			'

		await message.answer(f'{title}',  parse_mode='html')
	except:
		lc2 = 10
		lc3 = 1
		lc4 = 1
		lc5 = 1
		lc6 = 0
		lc7 = 0
		size = 0
		
		title = f'<b>Ваш Профіль</b>\n\
			Nick: <i><b><a href="tg://user?id={user_id}">{username}</a></b></i>\n\
			Lvl: <b>{lc3}</b>\n\
			Coin: <b>{lc2}</b>\n\
			Size: <b>{size}</b>\n\
			------------------------------\n\
			<i>Frihand 💪</i> == <b>{lc4}</b>\n\
			<i>Pump ⛽</i> == <b>{lc5}</b>\n\
			<i>Grease 🧼</i> == <b>{lc6}</b>\n\
			<i>Rabot 🐰</i> == <b>{lc7}</b>\n\
			------------------------------\n\
			<i>grease</i> °= <b>0</b>\n\
			<i>rabot</i> °= <b>0</b>\n\
			------------------------------\n\
			'

		if username == None:
			username = "Fredd"
		await message.answer(f'{title}',  parse_mode='html')
		cur.execute('INSERT INTO inventory VALUES(?, ?, ?, ?, ?, ?, ?)', (user_id, 200, 1, 1, 1, 0, 0))
		base.commit()
		cur.execute('INSERT INTO size_table_dickup VALUES(?, ?, ?, ?, ?, ?)', (first_name, user_id, 1, 1, chat_id, 1))
		base.commit()
		cur.execute('INSERT INTO effect VALUES(?, ?, ?)', (user_id, 0, 0))
		base.commit()
#
#	except:
#		first_name = username
#		if first_name == None:
#			first_name = "Fredd"
#		await message.answer(f'{title}',  parse_mode='html')
#
#	except:
#		lc2 = 1
#		lc3 = 1
#		lc4 = 1
#		size = 0
#		
#		await message.answer(f'{title}',  parse_mode='html')
#		cur.execute('INSERT INTO inventory VALUES(?, ?, ?, ?)', (user_id, 1, 1, 1))
#		base.commit()
#
#	except:
#		first_name = username
#		if first_name == None:
#			first_name = "Fredd"
#		await message.answer(f'{title}',  parse_mode='html')
#		cur.execute('INSERT INTO inventory VALUES(?, ?, ?, ?)', (user_id, 1, 1, 1))
#		base.commit()

# Commands "use"
@rate_limit(2, 'use')
async def use(message: types.Message):

	user_id = str(message.from_user.id)
	username = message.from_user.username
	first_name = message.from_user.first_name
	chat_id = str(message.chat.id)
	chat_name = message.chat.title
	args = message.get_args()

	if str(user_id) in ignore:
		return

	if not args:
		await message.reply('Неправильно написано!\nПриклад:\n/use 🥚')
		return


	try:
		if args == "💪" or args == "💪🏻":
			frihand = cur.execute('SELECT frihand FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
	
			if int(frihand[0]) <= 0:
				await message.answer(f"У вас немає <b>{args}</b>, попросіть у когось.",  parse_mode='html')
				return
	
			time_dickup = cur.execute('SELECT time_dickup FROM size_table_dickup WHERE user_id == ?', (user_id,)).fetchone()
			time_dickup = time_dickup[0]
	
			if int(time.time()) >= int(time_dickup):
				await message.answer(f"Ви <b>не використaли {args}</b> - у вас уже закінчився кулдаун.",  parse_mode='html')
				return
			frihand = int(frihand[0]) - 1
	
			cur.execute('UPDATE size_table_dickup SET time_dickup == ? WHERE user_id == ?', (int(time.time()), user_id))
			base.commit()
	
			cur.execute('UPDATE inventory SET frihand == ? WHERE user_id == ?', (frihand, user_id))
			base.commit()
	
			comment = "\nКулдаун знятий, можете збільшувати пипірку."
			await message.answer(f"Ви <b>успішно</b> використали <b>{args}</b>.{comment}",  parse_mode='html')
			return
	

		if args == "⛽" or args == "⛽️":
			pump = cur.execute('SELECT pump FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
	
			if int(pump[0]) <= 0:
				await message.answer(f"У вас немає <b>{args}</b>, попросіть у когось.",  parse_mode='html')
				return
	
			size = cur.execute('SELECT size FROM size_table_dickup WHERE user_id == ?', (user_id,)).fetchone()
			size = int(size[0]) + 50
	
			pump = int(pump[0]) - 1
			
			lvl = floor(int(size)/100) + 1

			cur.execute('UPDATE size_table_dickup SET size == ? WHERE user_id == ?', (size, user_id))
			base.commit()
	
			cur.execute('UPDATE inventory SET pump == ? WHERE user_id == ?', (pump, user_id))
			base.commit()

			cur.execute('UPDATE size_table_dickup SET lvl == ? WHERE user_id == ?', (lvl, user_id))
			base.commit()

			comment = "\nПипірка збільшилась на <b>50 см</b>"
			await message.answer(f"Ви <b>успішно</b> використали <b>{args}</b>.{comment}",  parse_mode='html')
			return
		

		if args == "🧼" or args == "🧼":
			numb_grease = cur.execute('SELECT grease FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
	
			if int(numb_grease[0]) <= 0:
				await message.answer(f"У вас немає <b>{args}</b>, попросіть у когось.",  parse_mode='html')
				return
	
			grease = cur.execute('SELECT grease FROM effect WHERE user_id == ?', (user_id,)).fetchone()

			grease = int(grease[0])
			grease = grease + 5

			numb_grease = int(numb_grease[0]) - 1

			cur.execute('UPDATE effect SET grease == ? WHERE user_id == ?', (grease, user_id))
			base.commit()
	
			cur.execute('UPDATE inventory SET grease == ? WHERE user_id == ?', (numb_grease, user_id))
			base.commit()

			comment = "\n<b>Змазка</b> допоможе вам на <b>5</b> наступних /dickup!"
			await message.answer(f"Ви <b>успішно</b> використали <b>{args}</b>.{comment}",  parse_mode='html')
			return

		if args == "🐰" or args == "🐰":
			numb_rabot = cur.execute('SELECT rabot FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
	
			if int(numb_rabot[0]) <= 0:
				await message.answer(f"У вас немає <b>{args}</b>, попросіть у когось.",  parse_mode='html')
				return
	
			rabot = cur.execute('SELECT rabot FROM effect WHERE user_id == ?', (user_id,)).fetchone()

			rabot = int(rabot[0])
			rabot = rabot + 5

			numb_rabot = int(numb_rabot[0]) - 1

			cur.execute('UPDATE effect SET rabot == ? WHERE user_id == ?', (rabot, user_id))
			base.commit()
	
			cur.execute('UPDATE inventory SET rabot == ? WHERE user_id == ?', (numb_rabot, user_id))
			base.commit()

			comment = "\n<b>Удача</b> вам усміхнеться <b>5</b> раз!"
			await message.answer(f"Ви <b>успішно</b> використали <b>{args}</b>.{comment}",  parse_mode='html')
			return

		items_list = ["⛽", "⛽️", "💪", "💪🏻", "🧼", "🧼", "🐰", "🐰"]

		if args not in items_list:
			await message.answer(f"<b>Цього знаку, немає у Базі Даних!</b>",  parse_mode='html')
			return

	except:
		await message.answer(f"<b>Вас немає цього предмета!</b>\nСпробуйте: '/dickup'",  parse_mode='html')
	

# Commands "give"
@rate_limit(2, 'give')
async def give(message: types.Message):

	user_id = str(message.from_user.id)
	args = message.get_args()
	username = message.from_user.username
	first_name = message.from_user.first_name
	chat_id = str(message.chat.id)
	chat_name = message.chat.title

	if str(user_id) in ignore:
		return

	if not message.reply_to_message:
		await message.reply("Команда має бути відповідю!")
		return


	reply_user_id = str(message.reply_to_message.from_user.id)
	reply_username = message.reply_to_message.from_user.username
	reply_first_name = message.reply_to_message.from_user.first_name

	if not args:
		await message.reply("Команда не має бути пуста!")
		return

	try:
		if reply_user_id == user_id:
			await message.reply("Передавайте іншим користувачам!")
			return	
	
		try:
			givint = int(message.text.split()[1])
			givtype = message.text.split()[2]
		except:
			await message.reply('Неправильно написано!\nПриклад:\n/give 1 🥚')
			return
	
		if givtype == "💪" or givtype == "💪🏻":
			frihand = cur.execute('SELECT frihand FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
	
			if int(frihand[0]) < givint:
				await message.answer(f"У вас замало <b>{args}</b>, попросіть у когось.",  parse_mode='html')
				return
	
			frihand = int(frihand[0]) - givint
	
			cur.execute('UPDATE inventory SET frihand == ? WHERE user_id == ?', (frihand, user_id))
			base.commit()
	
			try:
				reply_frihand = cur.execute('SELECT frihand FROM inventory WHERE user_id == ?', (reply_user_id,)).fetchone()
				reply_frihand = int(reply_frihand[0]) + givint
				cur.execute('UPDATE inventory SET frihand == ? WHERE user_id == ?', (reply_frihand, reply_user_id))
				base.commit()
			except:
				await message.answer(f"<b>Цього користувача, немає у Базі Даних!</b>",  parse_mode='html')
				return
	
		if givtype == "⛽" or givtype == "⛽️":
			pump = cur.execute('SELECT pump FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
	
			if int(pump[0]) < givint:
				await message.answer(f"У вас замало <b>{args}</b>, попросіть у когось.",  parse_mode='html')
				return
	
			pump = int(pump[0]) - givint
	
			cur.execute('UPDATE inventory SET pump == ? WHERE user_id == ?', (pump, user_id))
			base.commit()
	
			try:
				reply_frihand = cur.execute('SELECT pump FROM inventory WHERE user_id == ?', (reply_user_id,)).fetchone()
				reply_frihand = int(reply_frihand[0]) + givint
				cur.execute('UPDATE inventory SET pump == ? WHERE user_id == ?', (reply_frihand, reply_user_id))
				base.commit()
			except:
				await message.answer(f"<b>Цього користувача, немає у Базі Даних!</b>",  parse_mode='html')
				return
	
		if givtype == "🐰" or givtype == "🐰":
			rabot = cur.execute('SELECT rabot FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
	
			if int(rabot[0]) < givint:
				await message.answer(f"У вас замало <b>{args}</b>, попросіть у когось.",  parse_mode='html')
				return
	
			rabot = int(rabot[0]) - givint
	
			cur.execute('UPDATE inventory SET rabot == ? WHERE user_id == ?', (rabot, user_id))
			base.commit()
	
			try:
				reply_rabot = cur.execute('SELECT rabot FROM inventory WHERE user_id == ?', (reply_user_id,)).fetchone()
				reply_rabot = int(reply_rabot[0]) + givint
				cur.execute('UPDATE inventory SET rabot == ? WHERE user_id == ?', (reply_rabot, reply_user_id))
				base.commit()
			except:
				await message.answer(f"<b>Цього користувача, немає у Базі Даних!</b>",  parse_mode='html')
				return
	
		if givtype == "🧼" or givtype == "🧼":
			grease = cur.execute('SELECT grease FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
	
			if int(grease[0]) < givint:
				await message.answer(f"У вас замало <b>{args}</b>, попросіть у когось.",  parse_mode='html')
				return
	
			grease = int(grease[0]) - givint
	
			cur.execute('UPDATE inventory SET grease == ? WHERE user_id == ?', (grease, user_id))
			base.commit()
	
			try:
				reply_grease = cur.execute('SELECT grease FROM inventory WHERE user_id == ?', (reply_user_id,)).fetchone()
				reply_grease = int(reply_grease[0]) + givint
				cur.execute('UPDATE inventory SET grease == ? WHERE user_id == ?', (reply_grease, reply_user_id))
				base.commit()
			except:
				await message.answer(f"<b>Цього користувача, немає у Базі Даних!</b>",  parse_mode='html')
				return

		if givtype == "💶" or givtype == "ххх":
			coin = cur.execute('SELECT coin FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
	
			if int(coin[0]) < givint:
				await message.answer(f"У вас замало <b>{args}</b>, попросіть у когось.",  parse_mode='html')
				return
	
			coin = int(coin[0]) - givint
	
			cur.execute('UPDATE inventory SET coin == ? WHERE user_id == ?', (coin, user_id))
			base.commit()
	
			try:
				reply_grease = cur.execute('SELECT coin FROM inventory WHERE user_id == ?', (reply_user_id,)).fetchone()
				reply_grease = int(reply_grease[0]) + givint
				cur.execute('UPDATE inventory SET coin == ? WHERE user_id == ?', (reply_grease, reply_user_id))
				base.commit()
			except:
				await message.answer(f"<b>Цього користувача, немає у Базі Даних!</b>",  parse_mode='html')
				return

		if args == True: #"⛽" and args == "⛽️" and args == "💪" and args == "💪🏻"
			await message.answer(f"<b>Цього знаку, немає у Базі Даних!</b>",  parse_mode='html')
			return

		comment = f'Ви <b>успішно</b> передали <b>{givint}{givtype}</b>'

		try:

			await message.answer(f"{comment} користувачу <b>{reply_first_name}</b>.",  parse_mode='html')
		except:

			if reply_username == None:
				reply_username = "Fredd"
			await message.answer(f"{comment} користувачу <b>{reply_username}</b>.",  parse_mode='html')

	except:
		await message.answer(f"<b>Вас немає цього предмета!</b>\nСпробуйте: '/dickup'",  parse_mode='html')

'''*******************************************start*****************************************************************'''

def register_handlers_user(dp : Dispatcher):

	#Code
	dp.register_message_handler(comand_start, commands=["start"])
	dp.register_message_handler(help, commands=["help"])

	#dickup
	dp.register_message_handler(dickup, commands=["dickup"])
	#dp.register_message_handler(topdickchat, commands=["topdickchat"])
	dp.register_message_handler(topdick, commands=["topdick"])

	#profile/use
	dp.register_message_handler(profile, commands=["profile"])
	dp.register_message_handler(use, commands=["use"])
	dp.register_message_handler(give, commands=["give"])