import aiosqlite
import os

DB_PATH = "spinbox.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        # Включаем поддержку внешних ключей
        await db.execute("PRAGMA foreign_keys = ON")
        # Таблица пользователей
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                level TEXT,
                grip TEXT,
                style TEXT,
                strong_sides TEXT,
                weak_sides TEXT,
                rating INTEGER,
                goal TEXT
            )
        ''')
        # Тренировки
        await db.execute('''
            CREATE TABLE IF NOT EXISTS trainings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                datetime TEXT,
                duration_minutes INTEGER,
                type TEXT,
                notes TEXT,
                racket_id INTEGER,
                FOREIGN KEY(user_id) REFERENCES users(user_id),
                FOREIGN KEY(racket_id) REFERENCES my_equipment(id)
            )
        ''')
        # Соперники
        await db.execute('''
            CREATE TABLE IF NOT EXISTS opponents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                name TEXT,
                level TEXT,
                style TEXT,
                grip TEXT,
                hand TEXT,
                base TEXT,
                fh_rubber TEXT,
                bh_rubber TEXT,
                special_rubber TEXT,
                speed_attack INTEGER,
                serve_strength INTEGER,
                receive INTEGER,
                topspin_spin INTEGER,
                fh_game INTEGER,
                bh_game INTEGER,
                footwork INTEGER,
                psychology TEXT,
                tactical_notes TEXT,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        ''')
        # Матчи
        await db.execute('''
            CREATE TABLE IF NOT EXISTS matches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                opponent_id INTEGER,
                date TEXT,
                score TEXT,
                result TEXT,
                notes TEXT,
                FOREIGN KEY(opponent_id) REFERENCES opponents(id)
            )
        ''')
        # Моя экипировка
        await db.execute('''
            CREATE TABLE IF NOT EXISTS my_equipment (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                base TEXT,
                fh_rubber TEXT,
                bh_rubber TEXT,
                install_date TEXT,
                active INTEGER DEFAULT 1,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        ''')
        await db.commit()