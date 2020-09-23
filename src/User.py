import json
import requests

class User:
    def __init__(self, name, token: str):
        self.name = name
        self.token = token
        self.email = None
        self.filesCount = None
        self.filesSize = None

    def save(self):
        pass

    def getUserInfo(self):
        pass

    def getUploadsList(self):
        pass

    def getBestServer(self):
        pass

    def uploadFile(self, path):
        pass

    def deleteUpload(self):
        pass
