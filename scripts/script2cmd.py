#!/usr/bin/env python
import sys

def usage():
    print "Usage: script2cmd.py <destination file>"
    print ""
    print "This script read input line by line to convert to cmd shell understandable format and concat into a file"
    print "Paste your stuff and then type Ctrl-D to let it flush out everything at once"

def escape(text):
    line = text.strip('\r\n').replace('^','^^') # escape must be escaped first
    for i in ['\\','&','|','>','<','"']:
        line = line.replace(i,'^%s' % i)
    return line

def main(destination):
    line = sys.stdin.readline()
    count = 0
    output = ""
    if not line:
        return
    # first line use single bracket
    output += "echo %s > \"%s\"\r\n" % (escape(line), destination)
    line = sys.stdin.readline()
    while line:
        if line.strip():
            output += "echo %s >> \"%s\"\r\n" % (escape(line), destination)
        else: # if empty line
            output += "echo. >> \"%s\"\r\n" % (destination)
        line = sys.stdin.readline()
    output += ""
    output += "cscript \"%s\"" % destination
    print output



if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:    
        destination = sys.argv[1].replace('/','\\')
        main(destination)
