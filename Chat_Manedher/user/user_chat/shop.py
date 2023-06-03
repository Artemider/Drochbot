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

'''*******************************************shop*****************************************************************'''

async def balance_coin(coin, user_id):

	lvl = cur.execute('SELECT lvl FROM size_table_dickup WHERE user_id == ?', (user_id,)).fetchone()
	lvl = lvl[0]

	a = int(lvl) * 10
	random_du = random.randint(0,a)
	coin_up = int(coin) + random_du

	coin_list = [coin_up, random_du]

	return coin_list

async def items(random_items, user_id):

	if random_items >= 80:
		comment = 'Ви отримали: "💪".'

		frihand = cur.execute('SELECT frihand FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
		frihand = frihand[0]
		frihand = int(frihand) + 1

		cur.execute('UPDATE inventory SET frihand == ? WHERE user_id == ?', (frihand, user_id))
		base.commit()

	elif random_items <= 80 and random_items >= 70:
		comment = 'Ви отримали: "⛽".'

		pump = cur.execute('SELECT pump FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
		pump = pump[0]
		pump = int(pump) + 1

		cur.execute('UPDATE inventory SET pump == ? WHERE user_id == ?', (pump, user_id))
		base.commit()

	elif random_items <= 80 and random_items >= 75:
		comment = 'Ви отримали: "🧴".'

		grease = cur.execute('SELECT grease FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
		grease = grease[0]
		grease = int(grease) + 1
		cur.execute('UPDATE inventory SET grease == ? WHERE user_id == ?', (grease, user_id))
		base.commit()

	elif random_items == 1:
		comment = 'Ви отримали: "🧴".'

		coin = cur.execute('SELECT coin FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
		coin = coin[0]
		coin = int(coin) + 100
		cur.execute('UPDATE inventory SET coin == ? WHERE user_id == ?', (coin, user_id))
		base.commit()

	else:
		random_items = int(random.randint(5,20))
		comment = f'<i>Ви отримали:</i> <b>{random_items}💶</b>.'

		coin = cur.execute('SELECT coin FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
		coin = coin[0]
		coin = int(coin) + random_items
		cur.execute('UPDATE inventory SET coin == ? WHERE user_id == ?', (coin, user_id))
		base.commit()

	return comment

'''*******************************************shop*****************************************************************'''

#shop
@rate_limit(2, 'shop')
async def shop(message: types.Message):

	user_id = str(message.from_user.id)
	username = message.from_user.username
	first_name = str(message.from_user.first_name)
	chat_id = str(message.chat.id)
	chat_name = message.chat.title

	if str(user_id) in ignore:
		return

	try:
		coin = cur.execute('SELECT coin FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
		coin = coin[0]
	
		title = f'\
		Coin: <b>{coin}💶</b>\n\
		--------------------------------------\n\
		<i>Frihand 💪</i> $✓`•~ <b>15💶</b>\n\
		<i>Pump ⛽</i> $✓`•~ <b>50💶</b>\n\
		<i>Grease 🧼</i> $✓`•~ <b>100💶</b>\n\
		<i>Rabot 🐰</i> $✓`•~ <b>200💶</b>\n\
		--------------------------------------\n\
		====<b>/buy n item</b>====\n\
		--------------------------------------\n\
		  <i>/case</i> $✓`•~ <b>35💶</b>\n\
		--------------------------------------\n\
		'
	except:
		await message.answer(f"Спробуйте: '/dickup'",  parse_mode='html')
		return

	await message.answer(f'{title}',  parse_mode='html')

#market
@rate_limit(2, 'market')
async def market(message: types.Message):

	user_id = str(message.from_user.id)
	username = message.from_user.username
	first_name = str(message.from_user.first_name)
	chat_id = str(message.chat.id)
	chat_name = message.chat.title

	if str(user_id) in ignore:
		return

	try:
		sell_list = cur.execute('SELECT * FROM market').fetchall()
	except: pass

	awalist = []
	n = 0

	if sell_list == []:
		await message.answer(f"<b>None</b>\n",  parse_mode='html')
		return

	for x in sell_list:
		n += 1
		lc1 = x[1]#item_id
		lc2 = x[2]#price
		lc3 = x[3]#numb
		lc4 = x[4]#item
		lc5 = x[5]#dt

		if lc1 != None:
			awalist.append((f"<b>{n}){lc3}{lc4} $✓ {lc2}💶 [id == <i>{lc1}</i>]</b>"))

	awatitle = ';\n'.join(map(''.join,awalist))
	await message.answer(f"<b>Auction:</b>\n" + awatitle,  parse_mode='html')

#sell
@rate_limit(2, 'sell')
async def sell(message: types.Message):

	user_id = str(message.from_user.id)
	args = message.get_args()
	username = message.from_user.username
	first_name = str(message.from_user.first_name)
	chat_id = str(message.chat.id)
	chat_name = message.chat.title

	if str(user_id) in ignore:
		return

	if not args:
		await message.reply("Команда не має бути пуста!")
		return

	try:	
	
		try:
			givint = int(message.text.split()[1])
			givtype = message.text.split()[2]
			givprice = int(message.text.split()[3])

			if givint > 20 or givprice > 1000:
				await message.reply('Завелике число, малий шанс покупкки!\nМакс число == 20;\nМакс ціна == 1000;')
				return

			try:
				sid = cur.execute('SELECT user_id FROM market WHERE user_id == ?', (user_id,)).fetchone()
				sid = str(sid[0])
	
				if sid == user_id:
					await message.reply('Ви уже продаєте товари!')
					return
			except:pass

		except:
			await message.reply('Неправильно написано!\nПриклад:\n/sell 1 🥚 150')
			return
	
		if givtype == "💪" or givtype == "💪🏻":
			frihand = cur.execute('SELECT frihand FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
			
			if int(frihand[0]) < givint:
				await message.answer(f"У вас замало <b>{givtype}</b>.",  parse_mode='html')
				return
	
			frihand = int(frihand[0]) - givint
			givtype = "💪"
	
			cur.execute('UPDATE inventory SET frihand == ? WHERE user_id == ?', (frihand, user_id))
			base.commit()
	
		if givtype == "⛽" or givtype == "⛽️":
			pump = cur.execute('SELECT pump FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
			
			if int(pump[0]) < givint:
				await message.answer(f"У вас замало <b>{givtype}</b>.",  parse_mode='html')
				return
	
			pump = int(pump[0]) - givint
			givtype = "⛽"
	
			cur.execute('UPDATE inventory SET pump == ? WHERE user_id == ?', (pump, user_id))
			base.commit()
	
		if givtype == "🐰" or givtype == "🐰":
			rabot = cur.execute('SELECT rabot FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
			
			if int(rabot[0]) < givint:
				await message.answer(f"У вас замало <b>{givtype}</b>.",  parse_mode='html')
				return
	
			rabot = int(rabot[0]) - givint
			givtype = "🐰"
	
			cur.execute('UPDATE inventory SET rabot == ? WHERE user_id == ?', (rabot, user_id))
			base.commit()
	
		if givtype == "🧼" or givtype == "🧼":
			grease = cur.execute('SELECT grease FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
	
			if int(grease[0]) < givint:
				await message.answer(f"У вас замало <b>{givtype}</b>.",  parse_mode='html')
				return
	
			grease = int(grease[0]) - givint
			givtype = "🧼"
	
			cur.execute('UPDATE inventory SET grease == ? WHERE user_id == ?', (grease, user_id))
			base.commit()

		if givtype == "💶" or givtype == "ххх":
			coin = cur.execute('SELECT coin FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
	
			if int(coin[0]) < givint:
				await message.answer(f"У вас замало <b>{givtype}</b>.",  parse_mode='html')
				return
	
			coin = int(coin[0]) - givint
			givtype = "💶"
	
			cur.execute('UPDATE inventory SET coin == ? WHERE user_id == ?', (coin, user_id))
			base.commit()

		if args == True: #"⛽" and args == "⛽️" and args == "💪" and args == "💪🏻"
			await message.answer(f"<b>Цього знаку, немає у Базі Даних!</b>",  parse_mode='html')
			return

		comment = f'Ви <b>успішно</b> подали <b>{givint}{givtype}</b>, за {givprice}💶.'

		awalisty = []
		chat_list = cur.execute('SELECT * FROM chatlist').fetchmany(10000)

		for x in chat_list:
			chat_id_bd = x[1]
			awalisty.append(chat_id_bd)

		itmlist = []

		for x in awalisty:
			item_id = random.randint(1111,2000)

			if item_id != x:
				itmlist.append(item_id)

		item_id = itmlist[0]

		try:
			cur.execute('INSERT INTO market VALUES(?, ?, ?, ?, ?, ?)', (user_id, item_id, givprice, givint, givtype, 1))
			base.commit()
		except:
			await message.answer(f"<b>Error!</b>",  parse_mode='html')
			return

		await message.answer(f"{comment}",  parse_mode='html')

	except:
		await message.answer(f"<b>Вас немає цього предмета!</b>\nСпробуйте: '/dickup'",  parse_mode='html')

#kauf
@rate_limit(2, 'kauf')
async def kauf(message: types.Message):

	user_id = str(message.from_user.id)
	args = message.get_args()
	username = message.from_user.username
	first_name = str(message.from_user.first_name)
	chat_id = str(message.chat.id)
	chat_name = message.chat.title

	if str(user_id) in ignore:
		return

	if not args:
		await message.reply("Команда не має бути пуста!")
		return

	try:
		args = int(args)
	except:
		await message.answer(f"<i>Вкажіть, будь ласка, </i><b>id товару!</b>",  parse_mode='html')
		return

	try:
		sell_list = cur.execute('SELECT * FROM market WHERE item_id == ?', (args,)).fetchone()
		if sell_list == None:
			await message.answer(f"<i>Лота з таким</i> <b>id - немає!</b>",  parse_mode='html')
			return
		
		lc1 = sell_list[0]#user_id
		lc2 = int(sell_list[2])#price
		lc3 = int(sell_list[3])#numb
		lc4 = sell_list[4]#item
		
		prcoin = cur.execute('SELECT coin FROM inventory WHERE user_id == ?', (lc1,)).fetchone()
		prcoin = int(prcoin[0])
		
		coin = cur.execute('SELECT coin FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
		coin = int(coin[0])
		
		if coin < (lc2):
			await message.answer(f"У вас замало <b>💶</b>, потрібно <b>{lc2}</b>.",  parse_mode='html')
			return
		coin_def = coin

		coin = coin - lc2
		prcoin = prcoin + lc2

		if user_id == lc1:
			coin = coin_def
			prcoin = coin_def
		
		cur.execute('UPDATE inventory SET coin == ? WHERE user_id == ?', (coin, user_id))
		base.commit()
		cur.execute('UPDATE inventory SET coin == ? WHERE user_id == ?', (prcoin, lc1))
		base.commit()
		
		if lc4 == "💪":
			item_nm1 = cur.execute('SELECT frihand FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
			item_nm1 = int(item_nm1[0])
		
			itemsum = item_nm1 +lc3
		
			cur.execute('UPDATE inventory SET frihand == ? WHERE user_id == ?', (itemsum, user_id))
			base.commit()
		
		if lc4 == "⛽":
			item_nm1 = cur.execute('SELECT pump FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
			item_nm1 = int(item_nm1[0])
		
			itemsum = item_nm1 +lc3
		
			cur.execute('UPDATE inventory SET pump == ? WHERE user_id == ?', (itemsum, user_id))
			base.commit()
		
		if lc4 == "🧼":
			item_nm1 = cur.execute('SELECT grease FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
			item_nm1 = int(item_nm1[0])
		
			itemsum = item_nm1 +lc3
		
			cur.execute('UPDATE inventory SET grease == ? WHERE user_id == ?', (itemsum, user_id))
			base.commit()
		
		if lc4 == "🐰":
			item_nm1 = cur.execute('SELECT rabot FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
			item_nm1 = int(item_nm1[0])
		
			itemsum = item_nm1 +lc3
		
			cur.execute('UPDATE inventory SET rabot == ? WHERE user_id == ?', (itemsum, user_id))
			base.commit()
		
		if lc4 == "💶":
			item_nm1 = cur.execute('SELECT coin FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
			item_nm1 = int(item_nm1[0])
		
			itemsum = item_nm1 +lc3
		
			cur.execute('UPDATE inventory SET coin == ? WHERE user_id == ?', (itemsum, user_id))
			base.commit()
		
		cur.execute('DELETE FROM market WHERE item_id  == ?', (args,))
		base.commit()
	
		comment = f'Ви <b>успішно</b> купили <b>{lc3}{lc4}</b>.'
		
		await message.answer(f"{comment}",  parse_mode='html')
	except:
		await message.answer("Спробуйте: '/dickup'",  parse_mode='html')

#buy
@rate_limit(2, 'buy')
async def buy(message: types.Message):

	user_id = str(message.from_user.id)
	args = message.get_args()
	username = message.from_user.username
	first_name = str(message.from_user.first_name)
	chat_id = str(message.chat.id)
	chat_name = message.chat.title

	if str(user_id) in ignore:
		return

	if not args:
		await message.reply("Команда не має бути пуста!")
		return

	try:
	
		try:
			givint = int(message.text.split()[1])
			givtype = message.text.split()[2]
		except:
			await message.reply('Неправильно написано!\nПриклад:\n/buy 1 🥚')
			return
	
		if givtype == "💪" or givtype == "💪🏻":
			coin = cur.execute('SELECT coin FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
			frihand = cur.execute('SELECT frihand FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
			coin = int(coin[0])
	
			if coin < (givint*15):
				givint15 = givint*15
				await message.answer(f"У вас замало <b>💶</b>, потрібно <b>{givint15}</b>.",  parse_mode='html')
				return
	
			frihand = int(frihand[0]) + givint
			coin = coin - givint*15
	
			cur.execute('UPDATE inventory SET frihand == ? WHERE user_id == ?', (frihand, user_id))
			base.commit()
			cur.execute('UPDATE inventory SET coin == ? WHERE user_id == ?', (coin, user_id))
			base.commit()
	
		if givtype == "⛽" or givtype == "⛽️":
			coin = cur.execute('SELECT coin FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
			pump = cur.execute('SELECT pump FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
			coin = int(coin[0])
	
			if coin < (givint*50):
				givint15 = givint*50
				await message.answer(f"У вас замало <b>💶</b>, потрібно <b>{givint15}</b>.",  parse_mode='html')
				return
	
			pump = int(pump[0]) + givint
			coin = coin - givint*50
	
			cur.execute('UPDATE inventory SET pump == ? WHERE user_id == ?', (pump, user_id))
			base.commit()
			cur.execute('UPDATE inventory SET coin == ? WHERE user_id == ?', (coin, user_id))
			base.commit()

		if givtype == "🧼" or givtype == "🧼":
			coin = cur.execute('SELECT coin FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
			grease = cur.execute('SELECT grease FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
			coin = int(coin[0])

			if coin < (givint*100):
				givint15 = givint*100
				await message.answer(f"У вас замало <b>💶({coin})</b>, потрібно <b>{givint15}</b>.",  parse_mode='html')
				return
	
			grease = int(grease[0]) + givint
			coin = coin - givint*100
	
			cur.execute('UPDATE inventory SET grease == ? WHERE user_id == ?', (grease, user_id))
			base.commit()
			cur.execute('UPDATE inventory SET coin == ? WHERE user_id == ?', (coin, user_id))
			base.commit()

		if givtype == "🐰" or givtype == "🐰":
			coin = cur.execute('SELECT coin FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
			rabot = cur.execute('SELECT rabot FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
			coin = int(coin[0])

			if coin < (givint*200):
				givint15 = givint*200
				await message.answer(f"У вас замало <b>💶({coin})</b>, потрібно <b>{givint15}</b>.",  parse_mode='html')
				return
	
			rabot = int(rabot[0]) + givint
			coin = coin - givint*200
	
			cur.execute('UPDATE inventory SET rabot == ? WHERE user_id == ?', (rabot, user_id))
			base.commit()
			cur.execute('UPDATE inventory SET coin == ? WHERE user_id == ?', (coin, user_id))
			base.commit()
	


		if args == True: 
			await message.answer(f"<b>Цього знаку, немає у Базі Даних!</b>",  parse_mode='html')
			return

		comment = f'Ви <b>успішно</b> купили <b>{givint}{givtype}</b>.'

		await message.answer(f"{comment}",  parse_mode='html')
	except:
		await message.answer("Спробуйте: '/dickup'",  parse_mode='html')

#mine
@rate_limit(2, 'mine')
async def mine(message: types.Message):

	user_id = str(message.from_user.id)
	username = message.from_user.username
	first_name = str(message.from_user.first_name)
	chat_id = str(message.chat.id)
	chat_name = message.chat.title

	time_coin_bd = int(time.time()) + int(7200)

	lucky = 1
	print_lk = " "

	if str(user_id) in ignore:
		return

	try:
		coin = cur.execute('SELECT coin FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
		coin = coin[0]
	
		try:
			time_coin = cur.execute('SELECT time_coin FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
			time_coin = time_coin[0]
		
			if int(time_coin) > int(time.time()):
				raise SyntaxError(x)
	
		except:
			abc_time = int(time_coin) - int(time.time())
			h = floor(int(abc_time)/3600) 
			m = floor((int(abc_time) - int(h*3600))/60)
			s = int(abc_time) - int(h*3600 + m*60)
	
			if len(str(h)) < 2:
				h = str(0) + str(h)
		
			if len(str(m)) < 2:
				m = str(0) + str(m)
		
			if len(str(s)) < 2:
				s = str(0) + str(s)
		
			await message.reply(f'Ви уже <b>отримали <i>coin</i></b>,\nнаступний раз буде\nчерез: <b>{h}:{m}:{s}</b>.',  parse_mode='html')
			return
		
		coin_list = await balance_coin(coin, user_id)
		coin = coin_list[0]
		random_du = coin_list[1]
		
		cur.execute('UPDATE inventory SET coin == ? WHERE user_id == ?', (coin, user_id))
		base.commit()
		cur.execute('UPDATE inventory SET time_coin == ? WHERE user_id == ?', (time_coin_bd, user_id))
		base.commit()
	
		text = f"<i><b>{first_name}</b></i>, ви збільшили свій рахунок на <b>{random_du}</b> 💶.\nВаш новий рахунок: <b>{coin}</b> 💶."
	
		try:
			await message.reply(f'{text}',  parse_mode='html')
		except:
			first_name = username
			if first_name == None:
				first_name = "Fredd"
			await message.reply(f'{text}',  parse_mode='html')
	except:
		await message.answer("Спробуйте: '/dickup'",  parse_mode='html')

#case
@rate_limit(1, 'case')
async def case(message: types.Message):

	user_id = str(message.from_user.id)
	username = message.from_user.username
	first_name = str(message.from_user.first_name)
	chat_id = str(message.chat.id)
	chat_name = message.chat.title

	random_items = random.randint(0,100)

	if str(user_id) in ignore:
		return

	try:
		coin = cur.execute('SELECT coin FROM inventory WHERE user_id == ?', (user_id,)).fetchone()
		coin = int(coin[0])
		
		if coin < 35:
			await message.answer(f"У вас замало <b>💶</b>, потрібно <b>35</b>.",  parse_mode='html')
			return
		
		coin = coin - 35
		
		cur.execute('UPDATE inventory SET coin == ? WHERE user_id == ?', (coin, user_id))
		base.commit()

		comment = await items(random_items, user_id)
	except:
		await message.answer("Спробуйте: '/dickup'",  parse_mode='html')
		return

	await message.answer(f"{comment}",  parse_mode='html')


'''*******************************************start*****************************************************************'''

def register_handlers_shop(dp : Dispatcher):

	#shop
	dp.register_message_handler(shop, commands=["shop"])
	dp.register_message_handler(buy, commands=["buy"])
	dp.register_message_handler(mine, commands=["mine"])

	#market
	dp.register_message_handler(market, commands=["market"])
	dp.register_message_handler(sell, commands=["sell"])
	dp.register_message_handler(kauf, commands=["kauf"])

	#case
	dp.register_message_handler(case, commands=["case"])