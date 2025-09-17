from db.db import get_pool_func

async def create_chat(chat_id, chat_name):
    pool = await get_pool_func()
    async with pool.acquire() as connection:
        await connection.execute(
            'INSERT INTO chats (chat_id, chat_name) VALUES ($1, $2)', chat_id, chat_name)