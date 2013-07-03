#!/usr/bin/env python

import os
import os.path
import sys
import hashlib

#checksum = hashlib.sha1
# outputSuffix = ".sha1"
checksum = hashlib.md5
outputSuffix = ".md5"

# ignoreFileList = [".gitignore", ".gitsubmodule"]
ignoreFileList = []
#ignoreDirectoryList = [".svn", ".git"]
ignoreDirectoryList = []


def getChecksum(f):
    with open(f, "r") as fin:
        return checksum(fin.read()).hexdigest()


def recursiveChecksum(dirName):
    outputFileName = dirName.replace("/", "_")
    with open(outputFileName+".sha1", "w") as fout:
        for root, subdirs, files in os.walk(dirName):
            print "Processing ", root
            for f in files:
                if f in ignoreFileList:
                    continue
                filePath = os.path.join(root, f)
                relPath = os.path.relpath(filePath, dirName)
                fout.write(relPath)
                fout.write(" ")
                digest = getChecksum(filePath)
                fout.write(digest)
                fout.write("\n")
            for directory in ignoreDirectoryList:
                if directory in subdirs:
                    subdirs.remove(directory)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: %s <directory name>" % sys.argv[0]
    dirName = sys.argv[1]
    recursiveChecksum(dirName)
