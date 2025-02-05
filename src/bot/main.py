import logging
import asyncio
import argparse
from pathlib import Path
from aiogram import Bot, Dispatcher
from aiogram.filters import Command

from .config import API_TOKEN, SECTIONS, QUESTIONS_FILE
from .handlers import handle_start, handle_section_choice, handle_show_sections, load_all_questions
from .parser import load_questions_from_json, save_questions_to_json

def parse_args() -> argparse.Namespace:
    """
    Parse command line arguments.
    
    Returns:
        argparse.Namespace: Parsed command line arguments.
    """
    parser = argparse.ArgumentParser(description='Telegram bot for one-to-one meeting questions')
    parser.add_argument('--load_questions', action='store_true',
                       help='Load fresh questions from web and update JSON file')
    return parser.parse_args()

async def main() -> None:
    """Initialize and start the bot."""
    # Parse command line arguments
    args = parse_args()
    
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

    # Load questions
    if args.load_questions:
        # Delete existing JSON file if it exists
        if QUESTIONS_FILE.exists():
            QUESTIONS_FILE.unlink()
            logging.info(f"Deleted existing questions file: {QUESTIONS_FILE}")
        
        # Load fresh questions from web
        logging.info("Loading fresh questions from web...")
        await load_all_questions()
        
        # Save to JSON
        save_questions_to_json(SECTIONS)
    else:
        # Try to load from JSON first
        if not load_questions_from_json():
            # If JSON loading fails, load from web
            logging.info("Loading questions from web...")
            await load_all_questions()
            # Save for future use
            save_questions_to_json(SECTIONS)
    
    logging.info("Starting bot...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main()) 