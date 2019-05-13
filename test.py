import os

def searchFiles(dirPath, pattern):
    dirList = os.listdir(dirPath)
    for name in dirList:
        absPath = os.path.join(dirPath, name)
        if os.path.isdir(absPath):
              searchFiles(absPath, pattern)
        elif pattern.lower() in name.lower():
              print(absPath)

pattern = input("Enter text pattern:  ")
searchFiles(os.getcwd(), pattern)
