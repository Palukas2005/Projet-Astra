import sqlite3
import json

class Memory:
    def __init__(self, db_path="data/memory.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS souvenirs (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                type TEXT,
                                contenu TEXT,
                                emotions TEXT
                            )""")
        self.conn.commit()

    def add_memory(self, type_, contenu, emotions):
        self.cursor.execute("INSERT INTO souvenirs (type, contenu, emotions) VALUES (?, ?, ?)",
                            (type_, contenu, json.dumps(emotions)))
        self.conn.commit()

    def get_memories(self, limit=5):
        self.cursor.execute("SELECT contenu, emotions FROM souvenirs ORDER BY id DESC LIMIT ?", (limit,))
        return self.cursor.fetchall()