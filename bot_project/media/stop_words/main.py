import discord
from discord.ext import commands
from config.config import load_config
import logging
import asyncio
from logging.handlers import TimedRotatingFileHandler
import os
import sys
from db.db_update import create_tables


config = load_config(".env")

logger = logging.getLogger(__name__)

def setup_logging():
    """Настраивает логирование с ротацией по дням и вывод в консоль."""
    if not os.path.exists('logs'):
        os.makedirs('logs')

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter('%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s'))
    
    file_handler = TimedRotatingFileHandler(
        filename='logs/bot.log',
        when='midnight',
        interval=1,
        encoding='utf-8'
    )
    
    file_handler.setFormatter(logging.Formatter('%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s'))
    
    logging.getLogger().addHandler(console_handler)
    logging.getLogger().addHandler(file_handler)
    logging.getLogger().setLevel(logging.INFO)

async def main():

    setup_logging()
    logger.info("Запускаю бота...")

    await create_tables()
    logger.info("DB created")
    
    intents = discord.Intents.all()
    intents.messages = True
    intents.message_content = True
    intents.guilds = True

    bot = commands.Bot(command_prefix='/', intents=intents)

    @bot.event
    async def on_ready():
        await bot.load_extension("cogs.basic_commands")
        logger.info("Все модули команд успешно загружены.")
        
        await bot.tree.sync()
        logger.info("Слэш-команды успешно синхронизированы!")
    
    try:
        await bot.start(config.ds_bot.token)
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот остановлен.")