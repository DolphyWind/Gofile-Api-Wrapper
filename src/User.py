import requests
from db_manager import DBManager, UserExistException, UserNotExistException
from UploadInfo import UploadInfo, getKey

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
        data = req.json()
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
        data = req.json()
        if data['status'] != 'ok':
            raise Exception('An error occured!')

        data = data['data']
        uploadInfoList = list()
        for i, d in data.items():
            uploadInfo = UploadInfo(getKey(d, 'files'))
            uploadInfo.code = getKey(d, 'code')
            uploadInfo.server = getKey(d, 'server')
            uploadInfo.views = getKey(d, 'views')
            uploadInfo.number = getKey(d, 'number')
            uploadInfo.totalSize = getKey(d, 'totalSize')
            uploadInfo.uploadTime = getKey(d, 'uploadTime')
            uploadInfo.removalCode = getKey(d, 'removalCode')
            uploadInfo.adminCode = getKey(d, 'adminCode')
            uploadInfo.removalDate = getKey(d, 'removalDate')
            uploadInfoList.append(uploadInfo)
        return uploadInfoList

    @staticmethod
    def getBestServer():
        req = requests.get('https://apiv2.gofile.io/getServer')
        data = req.json()
        if data['status'] != 'ok':
            raise Exception('An error occured!')

        return data['data']['server']

    def uploadFile(self, filePath: str, adminCode=None, description=None, password=None, tags=None, expire=None):
        server = User.getBestServer()
        url = f'https://{server}.gofile.io/uploadFile'

        data = {'email': self.email}
        if adminCode:
            data['ac'] = adminCode
        if description:
            data['description'] = description
        if password:
            data['password'] = password
        if tags:
            if len(tags) > 1:
                tags = ','.join(tags)
            data['tags'] = tags
        if expire:
            data['expire'] = expire

        files = {'file': open(filePath, 'rb')}

        r = requests.post(url, files=files, data=data)
        json_data = r.json()
        if json_data['status'] == 'ok':
            json_data = json_data['data']

            uploadInfo = UploadInfo({})
            uploadInfo.code = getKey(json_data, 'code')
            uploadInfo.adminCode = getKey(json_data, 'adminCode')
            return uploadInfo
        else:
            return json_data['status']

    def uploadMany(self, filePaths: list, adminCode=None, description=None, password=None, tags=None, expire=None):
        informations = list()
        for p in filePaths:
            info = self.uploadFile(p, adminCode=adminCode, description=description, password=password, tags=tags, expire=expire)
            if adminCode is None:
                adminCode = info.adminCode
            informations.append(info)
        return informations


    def deleteUpload(self, adminCode: str):
        req = requests.get('https://apiv2.gofile.io/deleteUpload?ac=' + adminCode)
        data = req.json()
        return data['status'] == 'ok'
