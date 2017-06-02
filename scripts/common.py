#!/usr/bin/env python
import sys,os
import subprocess
import urllib
# this module requires requests library

""" These stuff should be going to a common library """

GNMAP_HTTP="80/open/tcp//http"
GNMAP_HTTPS="443/open/tcp//https"
GNMAP_FTP="21/open/tcp//ftp"
GNMAP_TELNET="23/open/tcp//telnet"
GNMAP_SMB="445/open/tcp//microsoft-ds"

LOG_COLOR_RED=31
LOG_COLOR_GREEN=32
LOG_COLOR_BLUE=34
LOG_COLOR_MAGENTA=35
LOG_COLOR_CYAN=36
LOG_COLOR_DEFAULT=39

OUTPUT_PATH='output'


def usage():
    print "Usage: %s <gnmap file>" % (os.path.basename(__file__))
    sys.exit(0)

def grep_hosts(gnmap_file, pattern="80/open/tcp//http"):
    command=r"""grep "%s" %s | awk '{print $2}'""" % (pattern, gnmap_file)
    result = subprocess.check_output(command, shell=True)
    hosts = result.split()
    return hosts

def _color(color):
    print "\033[%sm" %color,

def _log(message, color=None):
    if color is not None:
        _color(color)
    print message,
    _color(LOG_COLOR_DEFAULT)
    print ""

def log(message):
    _log(message)

def log_green(message):
    _log(message, LOG_COLOR_GREEN)

def log_red(message):
    _log(message, LOG_COLOR_RED)

def log_blue(message):
    _log(message, LOG_COLOR_BLUE)


def output_result(host, module, filename, content, output_path):
    # ok we have no time to play with security...
    try:
        os.mkdir('/'.join([output_path,host]))
    except OSError:
        pass
    with open('/'.join([output_path.strip('/'),host,"%s-%s" % (module,urllib.quote_plus(filename))]),'w') as f:
        f.write(content.encode('utf-8'))

