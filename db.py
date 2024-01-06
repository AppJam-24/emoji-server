import sqlite3


class db:
    def __init__(self) -> None:
        self.conn = sqlite3.connect("data.sqlite", check_same_thread=False)
        self.cursor = self.conn.cursor()

        self.initDB()

    def __del__(self):
        self.conn.close()

    def initDB(self):
        self.cursor.execute(
            """
            SELECT name FROM sqlite_master WHERE type='table' AND name='diary'
            """
        )
        if not self.cursor.fetchone():
            self.createTable()

    def createTable(self):
        self.cursor.execute(
            """
            CREATE TABLE diary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user INTEGER NOT NULL,
                date TEXT NOT NULL,
                emotion TEXT NOT NULL,
                diary TEXT NOT NULL,
                gpt TEXT NOT NULL,
                image TEXT
            )
            """
        )
        self.conn.commit()

    def insert(self, user, date, emotion, diary, gpt):
        self.cursor.execute(
            """
            INSERT INTO diary (user, date, emotion, diary, gpt) VALUES (?, ?, ?, ?, ?)
            """,
            (user, date, emotion, diary, gpt),
        )
        self.conn.commit()

        self.cursor.execute(
            """
            SELECT id FROM diary WHERE user = ? AND date = ?
            """,
            (user, date),
        )
        return self.cursor.fetchone()[0]

    def updateImage(self, id, image):
        self.cursor.execute(
            """
            UPDATE diary SET image = ? WHERE id = ?
            """,
            (image, id),
        )
        self.conn.commit()

    def getAll(self, user):
        self.cursor.execute(
            """
            SELECT * FROM diary WHERE user = ? ORDER BY id DESC
            """,
            (user,),
        )
        return self.cursor.fetchall()

    def get(self, id):
        self.cursor.execute(
            """
            SELECT * FROM diary WHERE id = ?
            """,
            (id,),
        )
        return self.cursor.fetchone()
