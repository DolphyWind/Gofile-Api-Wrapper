import json
import requests
from db_manager import DBManager, UserExistException, UserNotExistException
from UploadData import UploadData, getKey

class User:
    # Initialization. name is not a part of api
    def __init__(self, name, token: str):
        self.name = name
        self.token = token
        self.email = None
        self.filesCount = None
        self.filesSize = None

    # Save or Update user
    def save(self):
        DBManager.createTable()
        try:
            DBManager.addUser(self)
        except UserExistException as e:
            self.update()

    # Update user
    def update(self):
        DBManager.updateUser(self)

    # delete user
    def delete(self):
        DBManager.deleteUser(self)

    # Get information
    def getUserInfo(self):
        req = requests.get(f'https://apiv2.gofile.io/getAccountInfo?token={self.token}')
        data = json.loads(req.text)
        if data['status'] != 'ok':
            raise Exception('An error occured!')

        data = data['data']
        self.email = data['email']
        self.filesCount = data['filesCount']
        self.filesSize = data['filesSize']
        self.update()

    # Print information
    def printUserInfo(self):
        print('Name:', self.name)
        print('Token:', self.token)
        print('Email:', self.email)
        print('filesCount:', self.filesCount)
        print('filesSize:', self.filesSize)

    def getUploadsList(self):
        req = requests.get('https://apiv2.gofile.io/getUploadsList?token={}'.format(self.token))
        data = json.loads(req.text)
        if data['status'] != 'ok':
            raise Exception('An error occured!')

        data = data['data']
        uploadDatas = list()
        for i, d in data.items():
            uploadData = UploadData(getKey(d, 'files'))
            uploadData.code = getKey(d, 'code')
            uploadData.server = getKey(d, 'server')
            uploadData.views = getKey(d, 'views')
            uploadData.number = getKey(d, 'number')
            uploadData.totalSize = getKey(d, 'totalSize')
            uploadData.uploadTime = getKey(d, 'uploadTime')
            uploadData.removalCode = getKey(d, 'removalCode')
            uploadData.adminCode = getKey(d, 'adminCode')
            uploadData.removalDate = getKey(d, 'removalDate')
            uploadDatas.append(uploadData)
        return uploadDatas

    @staticmethod
    def getBestServer(self):
        req = requests.get('https://apiv2.gofile.io/getServer')
        data = json.loads(req.text)
        if data['status'] != 'ok':
            raise Exception('An error occured!')

        return data['data']['server']

    def uploadFile(self, path):
        pass

    def deleteUpload(self, adminCode: str):
        req = requests.get('https://apiv2.gofile.io/deleteUpload?ac=' + adminCode)
        data = json.loads(req.text)
        return data['status'] == 'ok'
