from aiogram import Router, Bot, types
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters import Command, StateFilter, CommandObject
from aiogram.types import Message,FSInputFile
from tgbot.config import load_config
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import F

import time
from datetime import datetime
import requests
import asyncio
from aiogram.exceptions import TelegramBadRequest

from tgbot.services.del_message import delete_message

from tgbot.filters.admin import ModerationFilter
from db.db_select import chat_exists
from db.db_update import create_chat

user_router = Router()
config = load_config(".env")
bot = Bot(token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode='HTML'))

@user_router.message(Command("init_moder"))
async def user_start(message: Message, command: CommandObject):
    chat_id = message.chat.id  
    
    flag = await chat_exists(chat_id)
    if not flag:
        if command.args:
            name = command.args
            await create_chat(chat_id, name)
            msg_text = f"Чат - {name} - инициализирован"
            await bot.send_message(chat_id=chat_id, text=msg_text)
        else:
            msg_text = "Укажите имя чата после команды. Например: /init чат1"
            await bot.send_message(chat_id=chat_id, text=msg_text)
            return
    else:
        msg_text = "Чат уже инициализирован"
        await bot.send_message(chat_id=chat_id, text=msg_text)
        return
    
@user_router.message(ModerationFilter())
async def delete_forbidden_content(message: types.Message):
    await message.delete()