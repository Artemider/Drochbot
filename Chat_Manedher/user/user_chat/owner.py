from user.Midllvary import rate_limit, ThrottlingMiddleware 
from create_bot import bot, dp
from config import owner
from database.start import base, cur

from aiogram import types, executor, Dispatcher
import asyncio

'''*******************************************Code*****************************************************************'''

# Commands "ownermenu"
@rate_limit(5, 'ownermenu')
async def ownermenu(message: types.Message):
	user_id = message.from_user.id
	username = message.from_user.username
	chat_id = str(message.chat.id)
	chat_name = message.chat.title

	if str(user_id) not in owner:
		await message.reply('У вас не достатньо прав.')
		return
	await message.answer('/ownermenu - меню каманд администратора.\
		\n/chatlist - список чатів.\
		\n/userlist - список користувачів.\
		\n/advertising - Повідомлення.\
		')

# Commands "chatlist"
@rate_limit(5, 'chatlist')
async def chatlist(message: types.Message):

	user_id = message.from_user.id
	username = message.from_user.username
	chat_id = str(message.chat.id)
	chat_name = message.chat.title

	if str(user_id) not in owner:
		await message.reply('У вас не достатньо прав.')
		return

	chatlist = cur.execute('SELECT * FROM chatlist').fetchall()

	awalist = []
	for x in chatlist:
		lc1 = x[0]
		lc2 = x[1]
		lc3 = x[2]
		lc4 = x[3]
		awalist.append((f"<b>{lc1})|</b> <i>{lc2}</i> <b>|</b> {lc3} <b>|</b> <b>{lc4}</b> <b>|</b>"))
	awatitle = ';\n'.join(map(''.join,awalist))
	await message.answer(f"<b>Список чатів:</b>\n" + awatitle,  parse_mode='html')

# Commands "userlist"
@rate_limit(5, 'userlist')
async def userlist(message: types.Message):

	user_id = message.from_user.id
	username = message.from_user.username
	chat_id = str(message.chat.id)
	chat_name = message.chat.title

	if str(user_id) not in owner:
		await message.reply('У вас не достатньо прав.')
		return

	chatlist = cur.execute('SELECT * FROM size_table_dickup').fetchall()

	awalist = []

	n = 0

	for x in chatlist:
		n += 1
		lc1 = x[0]
		lc2 = x[1]
		lc3 = x[2]
		lc4 = x[3]
		awalist.append((f"<b>{n})|</b> <i>{lc1}</i> <b>| {lc2} | {lc3} |</b>"))
	awatitle = ';\n'.join(map(''.join,awalist))
	await message.answer(f"<b>Список користувачів:</b>\n" + awatitle,  parse_mode='html')

# Commands "advertising"
@rate_limit(5, 'advertising')
async def advertising(message: types.Message):

	user_id = message.from_user.id
	args = message.get_args()
	username = message.from_user.username

	if str(user_id) not in owner:
		await message.reply('У вас не достатньо прав.')
		return

	chatlist = cur.execute('SELECT chat_id FROM chatlist').fetchall()
	#chatlist2 = map('.'.join,chatlist)
	#print(chatlist2)
	if not args:
		await message.answer('Команда немає бути пуста!')
	else:
		for message_ide in chatlist:
			try:
				message_ide = message_ide[0]
				await bot.send_message(chat_id = int(message_ide), text = f"<b>Повідомлення від автора:</b>\n     <i>{args}</i>",  parse_mode='html')
			except:
				await message.answer(f'Помилка!({message_ide})')			



'''*******************************************start*****************************************************************'''

def register_handlers_owner(dp : Dispatcher):
	dp.register_message_handler(ownermenu, commands=["ownermenu"])
	dp.register_message_handler(userlist, commands=["userlist"])
	dp.register_message_handler(chatlist, commands=["chatlist"])
	dp.register_message_handler(advertising, commands=["advertising"])