'''
Mark Hesser
www.hessercan.com
mark@hessercan.com
Python Project 6: Gen-Picture
'''

# imports
import os
import sys
import subprocess
import datetime
import urllib.request
import hashlib

# Declarations of final variables
genpicURL = "https://github.com/ccoble/sh-genpic.git"
scriptPath = os.path.dirname(os.path.abspath(__file__))
logFile = os.path.join(scriptPath,"results.txt")
gitPath = os.path.join(scriptPath,"sh-genpic")
gitScript = os.path.join(gitPath, "gen-picture")
testCases =  {1:"dog",2:"ducks",3:"flower",4:"moon",5:"mountain",6:"",7:"sun", }
compareURLs = {
    1: "http://downloads.ascentops.com/southhills/pictures/dog.jpg",
    2: "http://downloads.ascentops.com/southhills/pictures/ducks.jpg",
    3: "http://downloads.ascentops.com/southhills/pictures/flower.jpg",
    4: "http://downloads.ascentops.com/southhills/pictures/moon.jpg",
    5: "http://downloads.ascentops.com/southhills/pictures/mountain.jpg",
    6: "0",
    7: "0",
}
expectOutputCodes = [0,0,0,0,0,2,2]

# Main Program
# Clones or Fetches the required git repository
# Initializes the log file and runs the tests
def main():
    if os.path.exists(gitPath):
        gitFetch(genpicURL)
    else:
        gitClone(genpicURL)

    createLog(logFile)
    initLog(logFile, runTests())
    print("Check Log File for more details.")
    print("Log saved to: {}".format(logFile))
    print("Thanks for Playing... ;)")

# Clones a git repository to the same directory __file__ is in
# Requires a url to be passed in
def gitClone(url):
    try:
        output = subprocess.check_output(['git', 'clone', url], stderr=subprocess.STDOUT)
        output = output.decode('utf-8')
        print('Cloning Git Repository')
    except subprocess.CalledProcessError as e:
        print("return code {}".format(e.returncode))
        print(e.output.decode('utf-8'))

# Fetches a git repository to the same directory __file__ is in
# Requires a url to be passed in
def gitFetch(url):
    try:
        output = subprocess.check_output(['git', 'fetch', url], stderr=subprocess.STDOUT)
        output = output.decode('utf-8')
        print('Repository Exists')
        print('Fetching Git Repository')
    except subprocess.CalledProcessError as e:
        print("return code {}".format(e.returncode))
        print(e.output.decode('utf-8'))

# Gets a formatted version of the current Date and Time for the logFile
# Returns as a String
def getNowFormat():
    now = datetime.datetime.now()
    nowFormat = "{}-{}-{} {}:{}".format(now.year, now.month, now.day, now.hour, now.minute)
    return nowFormat

# Gets the version of code from the git repository
# Requires the path to the repository to be passed in
def getVersion(path):
    versionFile = os.path.join(path, "VERSION")
    with open (versionFile, "r") as vf:
        version = vf.read().splitlines()
        return version[0]

# Main Function for running tests
# Returns Pass and Fails in a Dictionary
# pf = { 'pass': result, 'fail': result, }
def runTests():
    # Keeps Track of Pass and Fails
    pf = {
        'pass': 0,
        'fail': 0,
    }

    testResults = {}
    for key,case in testCases.items():
        command = "python3 {} {}".format(gitScript,case)
        print("Testing Case #{}: ".format(key), end='')
        try:
            output = subprocess.check_output(['python3', gitScript, case], stderr=subprocess.STDOUT)
            output = output.decode('utf-8')
            opath = output.strip("Success:  picture saved at ")
            opath = opath.rstrip("\n\r")
            # print(output)
            testResults[key] = result(key, 0, command, output, opath)
            print("PASS")
            pf['pass'] += 1

        except subprocess.CalledProcessError as e:
            output = e.output.decode('utf-8')
            code = e.returncode
            opath = 0
            # print("command returned with return code {}".format(e.returncode))
            # print(e.output.decode('utf-8'))
            testResults[key] = result(key, code, command, output, opath)
            print("FAIL")
            pf['fail'] += 1


    logResults(testResults)
    checkFiles(testResults)
    return pf

# Takes in the data from the test and returns a Dictionary of results
def result(key, code, command, output, opath):
    if code == 0:
        result = "PASS"
    elif code > 0:
        result = "FAIL"

    result = {
        'result': result,
        'command': command,
        'status': code,
        'expected': expectOutputCodes[key-1],
        'output': output.splitlines(),
        'path': opath
    }

    return result

# uses the dictionary of results to create the log entries from the tests
# formats the dictionary into a list of strings
def logResults(testResults):
    results = []
    for key,result in testResults.items():
        results.append("Test Case #{}\n".format(key))
        results.append("    Result = {}\n".format(result['result']))
        results.append("    Running command: {}\n".format(result['command']))
        results.append("    Command status code = {}\n".format(result['status']))
        results.append("    Expected status code = {}\n".format(result['expected']))
        results.append("    Command output: \n")
        for o in result['output']:
            results.append("         {}\n".format(o))
        results.append("\n")

    for r in results:
        appendLog(r, logFile)

# Creates a Blank Log File
def createLog(file):
    with open(file, "w") as f:
        f.write("")

# Appends the Header of the Log to the Top of the Log File
# Requires the path to the log file, and a dictionary of pass/fail results
# pf = { 'pass': result, 'fail': result, }
def initLog(file, pf):
    totalTests = pf['pass'] + pf['fail']
    logData = [
        str("===============================  TEST RESULTS  ===============================\n"),
        str("Date/Time: {}\n".format(getNowFormat())),
        str("Code Version: {}\n".format(getVersion(gitPath))),
        str("Number of Tests Run:  {}\n".format(totalTests)),
        str("PASS = {}\n".format(pf['pass'])),
        str("FAIL = {}\n".format(pf['fail'])),
        str("+++++++++++++  Log ++++++++++++++\n\n"),
    ]
    with open (file, "r+") as f:
        logData.append(f.read())
        f.seek(0,0)
        f.writelines(logData)

# Appends data to file
def appendLog(data, file):
    with open (file, "a") as f:
        f.write(data)

# Gathers the file paths and urls to check based on a pass result
def checkFiles(testResults):
    for key,value in testResults.items():
        # print(value)
        if value['path'] != 0:
            compareChecksum(value['path'], compareURLs[key])

# Checks the checksum of the file with the url to compare
# Returns 0 if pass, 1 if fail
def compareChecksum(file, url):
    fileChecksum = hashlib.md5()
    urlChecksum = hashlib.md5()
    try:
        with urllib.request.urlopen(url) as furl:
            urldata = furl.read()
            urlChecksum.update(urldata)
    except urllib.error.URLError:
        print("Failed Download")
    except Exception as e:
        print(e)

    try:
        with open(file, 'rb') as f:
            filedata = f.read()
            fileChecksum.update(filedata)
    except Exception as e:
        print(e)

    print("Verifying File {}: ".format(os.path.split(file)[1]), end='')
    if urlChecksum.hexdigest() == fileChecksum.hexdigest():
        print("PASS")
        return 0 #Pass
    else:
        print("FAIL")
        return 1 #Fail

# Only runs main() if run script from command line
if __name__ == '__main__':
    sys.exit(main())
