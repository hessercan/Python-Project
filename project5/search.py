import os

def findFiles(pattern, path, ignorecase, recursive):
    foundFiles = []
    findFilesRecursive(pattern, path, ignorecase, recursive, foundFiles)
    return foundFiles

def findFilesRecursive(pattern, path, ignorecase, recursive, foundFiles):
    fileList = os.listdir(path)

    for file in fileList:
        absPath = os.path.join(path,file)

        if os.path.isdir(absPath) and recursive:
            findFilesRecursive(pattern,absPath,ignorecase,recursive,foundFiles)
        elif os.path.isfile(absPath):
            if ignorecase:
                if pattern.lower() in file.lower():
                    foundFiles.append(absPath)
            else:
                if pattern in file:
                    foundFiles.append(absPath)

def findFolders(pattern, path, ignorecase, recursive):
    foundFolders = []
    findFoldersRecursive(pattern, path, ignorecase, recursive, foundFolders)
    return foundFolders

def findFoldersRecursive(pattern, path, ignorecase, recursive, foundFolders):
        fileList = os.listdir(path)

        for file in fileList:
            absPath = os.path.join(path,file)

            if os.path.isdir(absPath):
                if ignorecase:
                    if pattern.lower() in file.lower():
                        foundFolders.append(absPath)
                else:
                    if pattern in file:
                        foundFolders.append(absPath)

            # Iterates recursive functionality
            if os.path.isdir(absPath) and recursive:
                findFoldersRecursive(pattern,absPath,ignorecase,recursive,foundFolders)


def printUsage():
    print("When Searching multiple patterns, you must clear the results using clearFind()")
    print("Usage: Pattern, Path, Case Sensitive, Recursive")

if __name__ == '__main__':
    printUsage()
