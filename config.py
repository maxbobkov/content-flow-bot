from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
ADMIN_IDS = [
    123456789,
    987654321  # Replace with the real IDs of the administrators
]

PHOTOS_DIR = Path('data/photos')
DB_PATH = Path('data/database.sqlite')

PHOTOS_DIR.mkdir(parents=True, exist_ok=True)