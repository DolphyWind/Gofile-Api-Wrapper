from User import User

def main():
    # Name is not needed for plugin. It's for database
    user = User('name', '<your_token>')

    # You can save user to database if you want to
    user.save()

    # Get user info
    user.getUserInfo()

    # Print user info
    user.printUserInfo()

    # Get best server
    print("Best server:", user.getBestServer())

    # Get uploads list
    uploads = user.getUploadsList()

    # Print uploads
    print('*-' * 25)
    for upload in uploads:
        for file in upload.filesList:
            print(file.name)            # Name
            print(file.mimetype)        # Mimetype
            print(file.size)            # Size
            print(file.md5)             # MD5
            print('-' * 50)
        print(upload.totalSize)         # Total size
        print(upload.views)             # Views
        print(upload.removalDate)       # Removal date
        print(upload.adminCode)         # Admin Code
        print('*-' * 25)

    # Single upload
    upload_info = user.uploadFile('example_file_1.txt', description='Single file upload via api')
    print(upload_info.code)
    print(upload_info.adminCode)
    print('-' * 50)

    # Multiple upload
    upload_infos = user.uploadMany(['example_file_1.txt', 'example_file_2.txt'], description='Multiple file upload via api.')
    for info in upload_infos:
        print(info.code)
        print(info.adminCode)

    # Delete any upload
    user.deleteUpload(adminCode='<admin_code>')

if __name__ == '__main__':
    main()