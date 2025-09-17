from aiogram.filters import BaseFilter
from aiogram.types import Message

from tgbot.config import Config

import string
from aiogram.exceptions import TelegramBadRequest
from db.db_select import chat_exists, user_exists_create, get_stop_words, get_chat_settings

class AdminFilter(BaseFilter):
    is_admin: bool = True

    async def __call__(self, obj: Message, config: Config) -> bool:
        return (obj.from_user.id in config.tg_bot.admin_ids) == self.is_admin


class ModerationFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        print('handled')
        permissions = await user_exists_create(message.from_user.id, message.from_user.username)
        chat_settings = await get_chat_settings(message.chat.id)

        if message.text and chat_settings:
            stop_words = await get_stop_words(chat_settings)
            if stop_words:
                clean_text = message.text.lower().translate(str.maketrans('', '', string.punctuation))
                message_words = set(clean_text.split())
                if not stop_words.isdisjoint(message_words):
                    return True 

        if message.forward_origin and not permissions['can_forward']:
            if message.forward_origin.type == 'hidden_user':
                return True 

            if message.forward_from:
                try:
                    fwd_member = await message.bot.get_chat_member(message.chat.id, message.forward_from.id)
                    if fwd_member.status in ["left", "kicked"]:
                        return True 
                except TelegramBadRequest:
                    return True 

        has_links = message.entities and any(e.type in ["url", "text_link"] for e in message.entities)
        if has_links and not permissions['can_send_links']:
            return True 

        if (message.photo and not permissions['can_send_photos']) or \
            (message.document and not permissions['can_send_files']) or \
            (message.video and not permissions['can_send_videos']) or \
            (message.sticker and not permissions['can_send_gifs_stickers']):
            return True 

        if (message.voice or message.video_note) and not permissions['can_send_voice']:
            return True

        return False
