import sqlite3
import User

FILENAME = 'users.db'
db = sqlite3.connect(FILENAME)
cursor = db.cursor()

class UserExistException(Exception):
    pass

class UserNotExistException(Exception):
    pass


class DBManager:
    @staticmethod
    def createTable():
        sql = """
        CREATE TABLE IF NOT EXISTS Users(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            name VARCHAR(30) NOT NULL UNIQUE,
            token VARCHAR(128) NOT NULL UNIQUE,
            email VARCHAR(30),
            filesCount INTEGER,
            filesSize INTEGER
        );
        """
        cursor.execute(sql)

    @staticmethod
    def addUser(user: User):
        if DBManager.userExists(user):
            raise UserExistException('User already exists!')
        sql = """
        INSERT INTO Users (name, token, email, filesCount, filesSize) VALUES (?, ?, ?, ?, ?)
        """

        params = (user.name, user.token, user.email, user.filesCount, user.filesSize,)

        try:
            cursor.execute(sql, params)
            db.commit()
        except:
            return False
        else:
            return True

    @staticmethod
    def addUsers(users: list):
        users = [user for user in users if not DBManager.userExists(user)]
        sql = """
        INSERT INTO Users (name, token, email, filesCount, filesSize) VALUES (? ?, ?, ?, ?)
        """

        params = [(user.name, user.token, user.email, user.filesCount, user.filesSize,) for user in users]

        try:
            cursor.executemany(sql, params)
            db.commit()
        except Exception as e:
            return False, e
        else:
            return True, ''

    @staticmethod
    def userExists(user: User):
        sql = """
        SELECT * FROM Users WHERE token='{}'
        """.format(user.token)

        try:
            cursor.execute(sql)
        except:
            return False
        else:
            return True

    @staticmethod
    def updateUser(user: User):
        if not DBManager.userExists(user):
            raise UserNotExistException('User not exists')

        sql = "UPDATE Users SET email=?,filesCount=?,filesSize=? WHERE token=?"
        params = (user.email, user.filesCount, user.filesSize, user.token, )

        cursor.execute(sql, params)
        db.commit()

    @staticmethod
    def deleteUser(user: User):
        sql = "DELETE FROM Users WHERE token=?"
        params = (user.token, )

        cursor.execute(sql, params)
        db.commit()