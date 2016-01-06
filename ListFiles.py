# This script walks through Documents folder in your home directory
# and compiles list of all the files with provided extensions.
# ListFiles.py .docx .pdf

import os
import sys

# Parse command line
if len(sys.argv) is 1:
    sys.exit("Must provide extensions of files to collect")


docListFile = 'listfiles.txt'
outFile = ""
# Get user name
userName = os.environ.get("USERNAME")
# Make path to the Documents directory (on windows system)
pathToDir = 'C:\Users\\'+userName+'\Documents\HR'

# Open file to write the list
try:
    outFile = open(docListFile, 'w');
except IOError as e:
    print "Failed to open file ", docListFile
    sys.exit(e.errno)

# Walk through every directory under Documents folder
# and find files with dersired extensions.
for path, dirs, files in os.walk(pathToDir):
    for file in files:
        fileName, fileExt = os.path.splitext(file)
        fullPath = os.path.join(path, file)
        print fullPath, fileExt
        for ext in sys.argv:
            if fileExt.startswith(ext):
                # Write the full path to the file
                outFile.writelines(fullPath+'\n')

outFile.close()
                    
