import argparse
import search
import os

#print(args)
def printHelp():
    print("Usage: Search Pattern (multiple accepted separated by commas)" )
    print("    --path or -p = Specify Path to Search, Default is current working directory.")
    print("    --ignore-case or -i = ignore Case Sensitivity.")
    print("    --recursive or -r = Search all subdirectories.")
    print("    --help or -h: Print this Help information.")

def run():
    path = args.path
    ignorecase = args.ignorecase
    recursive = args.recursive

    findPatterns = args.pattern.split(",")
    for pattern in findPatterns:
        foundFiles = search.findFiles(pattern, path, ignorecase, recursive)
        print("%d Files Matching \"%s\"" % (len(foundFiles),pattern))
        for f in foundFiles:
            print("\t",f)

        print()

        foundFolders = search.findFolders(pattern, path, ignorecase, recursive)
        print("%d Folders Found Matching \"%s\"" %  (len(foundFolders),pattern))
        if len(foundFolders) > 0:
            for f in foundFolders:
                print("\t",f)

        print()


parser = argparse.ArgumentParser(description='This is program searches for patterns', add_help=False)
parser.add_argument(dest='pattern', help='specify an pattern to search for')
parser.add_argument('--path', '-p', dest='path', help='specify the path of the search folder', default=os.getcwd())
parser.add_argument('--ignore-case', '-i', dest='ignorecase', action='store_true')
parser.add_argument('--recursive', '-r', dest='recursive', action='store_true')
parser.add_argument('--help', '-h', dest='help', action='store_true')
args = parser.parse_args()

if __name__ == '__main__':
    #print(args)
    if args.help:
        printHelp()
    else:
        run()

quit()
