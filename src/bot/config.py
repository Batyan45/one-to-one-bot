from typing import Dict, TypedDict
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(env_path)

class Section(TypedDict):
    """Type definition for section configuration."""
    title: str
    url: str
    questions: list

def get_api_token() -> str:
    """
    Get the Telegram Bot API token from environment variables.
    
    Returns:
        str: The API token.
        
    Raises:
        ValueError: If TELEGRAM_API_TOKEN is not set in environment variables.
    """
    api_token = os.getenv('TELEGRAM_API_TOKEN')
    if not api_token:
        raise ValueError(
            'TELEGRAM_API_TOKEN environment variable is not set. '
            'Please set it in your .env file or environment variables.'
        )
    return api_token

# Telegram Bot API Token
API_TOKEN = get_api_token()

# Sections configuration
SECTIONS: Dict[str, Section] = {
    "udalennie": {
        "title": "Удаленные команды",
        "url": "https://pritula.academy/tpost/9n9vnetijt-500-voprosov-dlya-1-1-udalennie-komandi",
        "questions": []
    },
    "podderzhka": {
        "title": "Поддержка руководителя",
        "url": "https://pritula.academy/tpost/pl3x13xrfi-500-voprosov-dlya-1-1-podderzhka-rukovod",
        "questions": []
    },
    "tseli": {
        "title": "Цели и согласованность",
        "url": "https://pritula.academy/tpost/6smfhyiujo-500-voprosov-dlya-1-1-tseli-i-soglasovan",
        "questions": []
    },
    "meshaet": {
        "title": "Что мешает в работе",
        "url": "https://pritula.academy/tpost/esamuuzrsr-500-voprosov-dlya-1-1-chto-meshaet-v-rab",
        "questions": []
    },
    "feedback": {
        "title": "Обратная связь",
        "url": "https://pritula.academy/tpost/u900gajn92-500-voprosov-dl-1-1-obratnaya-svyaz",
        "questions": []
    },
    "priznanie": {
        "title": "Признание",
        "url": "https://pritula.academy/tpost/hpij8tbj72-500-voprosov-dlya-1-1-priznanie",
        "questions": []
    },
    "career": {
        "title": "Карьера и развитие",
        "url": "https://pritula.academy/tpost/sor876011c-500-voprosov-dlya-1-1-karernii-rost-i-ra",
        "questions": []
    },
    "tools": {
        "title": "Инструменты и ресурсы",
        "url": "https://pritula.academy/tpost/40uajzj3kh-500-voprosov-dlya-1-1-instrumenti-i-resu",
        "questions": []
    },
    "duties": {
        "title": "Обязанности и показатели",
        "url": "https://pritula.academy/tpost/371n7j4kae-500-voprosov-dlya-1-1-obyazannosti-i-pok",
        "questions": []
    },
    "teamwork": {
        "title": "Работа в команде",
        "url": "https://pritula.academy/tpost/pbu5ztsz3r-500-voprosov-dlya-1-1-rabota-v-komande-i",
        "questions": []
    },
    "satisfaction": {
        "title": "Удовлетворенность работой",
        "url": "https://pritula.academy/tpost/53foxs5441-500-voprosov-dlya-1-1-udovletvorennost-r",
        "questions": []
    },
    "role": {
        "title": "Ясность роли и ожидания",
        "url": "https://pritula.academy/tpost/nm2flfz9as-500-voprosov-dlya-1-1-yasnost-roli-i-ozh",
        "questions": []
    },
    "company_feedback": {
        "title": "Обратная связь компании",
        "url": "https://pritula.academy/tpost/xyra5lmd8p-500-voprosov-dlya-1-1-obratnaya-svyaz-s",
        "questions": []
    },
    "icebreakers": {
        "title": "Ледоколы",
        "url": "https://pritula.academy/tpost/7mcpo3lc9p-500-voprosov-dlya-1-1-ledokoli",
        "questions": []
    }
} 