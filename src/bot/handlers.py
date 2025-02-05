from typing import Any
import random
import logging
import asyncio
from aiogram import Bot, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .config import SECTIONS
from .parser import parse_questions

async def load_all_questions() -> None:
    """Load questions for all sections."""
    loop = asyncio.get_running_loop()
    for key, section in SECTIONS.items():
        questions = await loop.run_in_executor(None, parse_questions, section['url'])
        section['questions'] = questions
        logging.info(f"Loaded {len(questions)} questions for section '{section['title']}'")

async def handle_start(message: types.Message) -> None:
    """
    Handle /start command.
    
    Args:
        message: Incoming message object.
    """
    buttons = []
    for key, section in SECTIONS.items():
        button = InlineKeyboardButton(text=section['title'], callback_data=key)
        buttons.append([button])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer("Выберите раздел вопросов:", reply_markup=keyboard)

async def handle_section_choice(callback: types.CallbackQuery) -> None:
    """
    Handle section choice callback.
    
    Args:
        callback: Callback query object.
    """
    section_key = callback.data
    section = SECTIONS.get(section_key)
    if not section or not section['questions']:
        await callback.answer("В этом разделе нет вопросов.")
        return

    question_tuple = random.choice(section['questions'])
    rating, question_text = question_tuple

    # Format message with bold section title
    message_text = f"**{section['title']}**\n\n{question_text}"

    # Create keyboard with sections list button and rating/next buttons
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="К списку тем", callback_data="show_sections")],
            [
                InlineKeyboardButton(text=str(rating), url=section['url']),
                InlineKeyboardButton(text="🔄 Другой", callback_data=section_key)
            ]
        ]
    )

    # If this is a new question request (not initial), delete the previous message
    if callback.message:
        await callback.message.delete()

    # Send new message with question
    await callback.message.answer(message_text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()

async def handle_show_sections(callback: types.CallbackQuery) -> None:
    """
    Handle showing sections list callback.
    
    Args:
        callback: Callback query object.
    """
    # Create sections list keyboard
    buttons = []
    for key, section in SECTIONS.items():
        button = InlineKeyboardButton(text=section['title'], callback_data=key)
        buttons.append([button])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    # Edit current message to show sections list
    await callback.message.edit_text("Выберите раздел вопросов:", reply_markup=keyboard)
    await callback.answer() 