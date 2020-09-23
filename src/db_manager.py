import sqlite3
import User

FILENAME = 'users.db'
db = sqlite3.connect(FILENAME)
cursor = db.cursor()

class DBManager:


    @staticmethod
    def createTable():
        sql = """
        CREATE TABLE IF NOT EXISTS Users(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            token VARCHAR(128) NOT NULL,
            email VARCHAR(30),
            filesCount INTEGER,
            filesSize INTEGER
        );
        """
        cursor.execute(sql)

    @staticmethod
    def addUser(user: User):
        sql = """
        INSERT INTO Users (token, email, filesCount, filesSize) VALUES (?, ?, ?, ?)
        """

        values = (user.token, user.email, user.filesCount, user.filesSize,)

        try:
            cursor.execute(sql, values)
            db.commit()
        except Exception as e:
            return (False, e)
        else:
            return (True, '')

    @staticmethod
    def addUsers(users: list):
        sql = """
        INSERT INTO Users (token, email, filesCount, filesSize) VALUES (?, ?, ?, ?)
        """

        values = [(user.token, user.email, user.filesCount, user.filesSize,) for user in users]

        try:
            cursor.executemany(sql, values)
            db.commit()
        except Exception as e:
            return (False, e)
        else:
            return (True, '')

