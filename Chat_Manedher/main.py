from create_bot import bot, storage, dp
from user.Midllvary import rate_limit, ThrottlingMiddleware

from user.user_chat.owner import register_handlers_owner
#from user.user_chat.moderator import register_handlers_moderator
from user.user_chat.user import register_handlers_user
from user.user_chat.shop import register_handlers_shop

import asyncio
from aiogram import Bot, Dispatcher, types, executor

import datetime

'''*******************************************start*****************************************************************'''

register_handlers_owner(dp)

register_handlers_user(dp)

register_handlers_shop(dp)

#register_handlers_moderator(dp)

'''*******************************************init*****************************************************************'''

if __name__ == '__main__':
	# Setup middleware
	dp.middleware.setup(ThrottlingMiddleware())

	# Start long-polling
	executor.start_polling(dp, skip_updates=True)