def saveTo(folder, path):
    os.makedirs(path)
    for folderName, folder2 in folder['folders'].items():
        saveTo(folder2, os.path.join(path, folderName))
    for filename, filedata in folder['files'].items():
        with open(os.path.join(path, filename), 'wb') as f:
            f.write(filedata)

saveTo(courseNarc, os.path.join('../Testing/phMap', courseFilename))