import os

workingDir = os.getcwd()
#print(workingDir)

scriptDir = os.path.dirname(os.path.abspath(__file__))
#print(scriptDir)

homeDir = os.path.expanduser('~')
subDir = "python"
#print(homeDir)


path = os.path.join(homeDir,subDir)
print(path)

fileList = os.listdir(os.getcwd())

for f in fileList:
    if os.path.isfile(f):
        print(f)

# Problem 2
def searchFiles(dirPath,pattern):
    dirList = os.listdir(dirPath)
    for name in dirList:
        absPath = os.path.join(dirPath,name)
        if os.path.isdir(absPath):
            searchFiles(absPath,pattern)
        elif pattern.lower() in name.lower():
            print(absPath)

pattern = input("Enter text pattern: ")
searchFiles(os.getcwd(),pattern)
