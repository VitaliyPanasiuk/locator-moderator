from db.db import get_pool_func
import aiofiles
import os

async def chat_exists(chat_id):
    pool = await get_pool_func()
    async with pool.acquire() as connection:
        chats = await connection.fetchrow("SELECT * from chats WHERE chat_id = $1", chat_id)
        
    return True if chats else False

async def user_exists_create(user_id, user_name):
    pool = await get_pool_func()
    async with pool.acquire() as connection:
        user = await connection.fetchrow("SELECT * from users WHERE user_id = $1", user_id)
        
        if not user:
            await connection.execute(
                'INSERT INTO users (user_id, user_name) VALUES ($1, $2)', user_id, user_name)
            
            user = await connection.fetchrow("SELECT * from users WHERE user_id = $1", user_id)
        
    return user
    
async def get_chat_settings(chat_id):
    pool = await get_pool_func()
    async with pool.acquire() as connection:
        chat = await connection.fetchrow(
            "SELECT * FROM chats WHERE chat_id = $1", 
            chat_id
        )
        return chat

async def get_stop_words(chat_settings):
    if chat_settings and chat_settings['stop_word_file']:
        

        current_script_path = os.path.abspath(__file__)
        project_root = os.path.dirname(os.path.dirname(current_script_path))
        MEDIA_ROOT = os.path.join(project_root, 'bot_project', 'media')
        
        file_path = os.path.join(MEDIA_ROOT, chat_settings['stop_word_file'])
        
        try:
            async with aiofiles.open(file_path, mode='r', encoding='utf-8') as f:
                content = await f.read()
                return {line.strip().lower() for line in content.splitlines() if line.strip()}
        except FileNotFoundError:
            print(f"Ошибка: Файл стоп-слов не найден по пути {file_path}")
            return set()
            
    return set()