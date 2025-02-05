from typing import List, Tuple, Dict
import logging
import json
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from pathlib import Path

from .config import SECTIONS, QUESTIONS_FILE, DATA_DIR

def save_questions_to_json(sections: Dict[str, dict]) -> None:
    """
    Save questions from all sections to a JSON file.
    
    Args:
        sections: Dictionary containing all sections with their questions.
    """
    # Create data directory if it doesn't exist
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # Prepare data for saving
    data = {
        key: {
            'title': section['title'],
            'url': section['url'],
            'questions': section['questions']
        }
        for key, section in sections.items()
    }
    
    # Save to JSON file
    with open(QUESTIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    logging.info(f"Questions saved to {QUESTIONS_FILE}")

def load_questions_from_json() -> bool:
    """
    Load questions from JSON file into sections.
    
    Returns:
        bool: True if questions were loaded successfully, False otherwise.
    """
    try:
        if not QUESTIONS_FILE.exists():
            logging.warning("Questions file not found.")
            return False
            
        with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Update sections with loaded data
        for key, section_data in data.items():
            if key in SECTIONS:
                SECTIONS[key]['questions'] = section_data['questions']
                
        logging.info("Questions loaded from JSON file successfully")
        return True
    except Exception as e:
        logging.error(f"Error loading questions from JSON: {e}")
        return False

def parse_questions(url: str) -> List[Tuple[int, str]]:
    """
    Parse questions from the given URL.
    
    Args:
        url: The URL to parse questions from.
        
    Returns:
        List of tuples containing (rating, question_text), sorted by rating in descending order.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
    }
    
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    try:
        response = session.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        logging.error(f"Error fetching {url}: {e}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    article_body = soup.find(itemprop="articleBody")
    questions = []
    
    if article_body:
        ul = article_body.find("ul")
        if ul:
            li_items = ul.find_all("li")
            for li in li_items:
                text = li.get_text(strip=True)
                parts = text.split(" ", 1)
                if len(parts) == 2:
                    rating_str, question_text = parts
                    try:
                        rating = int(rating_str)
                    except ValueError:
                        rating = 0
                    questions.append((rating, question_text))
    else:
        logging.error(f"Question block not found on page {url}")

    questions.sort(key=lambda x: x[0], reverse=True)
    return questions 