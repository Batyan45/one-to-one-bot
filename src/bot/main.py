import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command

from .config import API_TOKEN, SECTIONS
from .handlers import handle_start, handle_section_choice, handle_show_sections, load_all_questions

async def main() -> None:
    """Initialize and start the bot."""
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Initialize bot and dispatcher
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()

    # Register handlers
    dp.message.register(handle_start, Command("start"))
    # Register section choice handler only for valid section keys
    dp.callback_query.register(handle_section_choice, lambda c: c.data in SECTIONS)
    # Register show sections handler
    dp.callback_query.register(handle_show_sections, lambda c: c.data == "show_sections")

    # Load questions and start polling
    logging.info("Loading questions...")
    await load_all_questions()
    
    logging.info("Starting bot...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main()) 