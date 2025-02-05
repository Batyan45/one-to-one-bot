from typing import List, Tuple
import logging
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

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