import json
import requests
from db_manager import DBManager, UserExistException, UserNotExistException

class User:
    def __init__(self, name, token: str):
        self.name = name
        self.token = token
        self.email = None
        self.filesCount = None
        self.filesSize = None

    def save(self):
        DBManager.createTable()
        try:
            DBManager.addUser(self)
        except UserExistException as e:
            self.update()

    def update(self):
        DBManager.updateUser(self)

    def delete(self):
        DBManager.deleteUser(self)

    def getUserInfo(self):
        req = requests.get(f'https://apiv2.gofile.io/getAccountInfo?token={self.token}')
        data = json.loads(req.text)
        if data['status'] != 'ok':
            raise Exception('An error is occured!')

        data = data['data']
        self.email = data['email']
        self.filesCount = data['filesCount']
        self.filesSize = data['filesSize']
        self.update()

    def printUserInfo(self):
        print('Name:', self.name)
        print('Token:', self.token)
        print('Email:', self.email)
        print('filesCount:', self.filesCount)
        print('filesSize:', self.filesSize)

    def getUploadsList(self):
        pass

    @staticmethod
    def getBestServer(self):
        pass

    def uploadFile(self, path):
        pass

    def deleteUpload(self):
        pass
