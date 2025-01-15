import sqlite3
from pathlib import Path

class Database:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS photos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_path TEXT NOT NULL,
                    caption TEXT,
                    is_posted BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
    
    def add_photo(self, file_path: str, caption: str = None):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                'INSERT INTO photos (file_path, caption) VALUES (?, ?)',
                (file_path, caption)
            )
    
    def get_random_unposted_photo(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                'SELECT id, file_path, caption FROM photos WHERE is_posted = FALSE ORDER BY RANDOM() LIMIT 1'
            )
            result = cursor.fetchone()
            return result if result else None
    
    def mark_as_posted(self, photo_id: int):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                'UPDATE photos SET is_posted = TRUE WHERE id = ?',
                (photo_id,)
            )
    
    def has_unposted_photos(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('SELECT COUNT(*) FROM photos WHERE is_posted = FALSE')
            return cursor.fetchone()[0] > 0