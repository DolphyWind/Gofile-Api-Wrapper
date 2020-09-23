from File import File

def getKey(d: dict, key: str):
    try:
        val = d[key]
    except KeyError:
        return None
    else:
        return val

class UploadInfo:
    def __init__(self, files: dict):
        self.code = str()
        self.filesList = list()
        for i, data in files.items():
            f = File()
            f.name = getKey(data, 'name')
            f.mimetype = getKey(data, 'mimetype')
            f.size = getKey(data, 'size')
            f.md5 = getKey(data, 'md5')
            self.filesList.append(f)

        self.server = str()
        self.views = int()
        self.number = int()
        self.totalSize = int()
        self.uploadTime = int()
        self.removalCode = str()
        self.adminCode = str()
        self.removalDate = int()