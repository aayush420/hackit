#!/usr/bin/env python
import sys,os
import subprocess
# this module requires requests library
from ftplib import FTP
from common import *

def request_anon(host, **kwargs):
    ftp = FTP(host, **kwargs)
    welcome = ftp.getwelcome()
    if welcome: log_green(welcome)
    auth_result = ftp.login()
    if not auth_result.strip().startswith('230'):
        log_red('Anonymous login failed')
        return

    log_green('Anonymous login success')
    log('current directory: %s' % ftp.pwd())
    log('Trying to obtain directory listing...')
    ftp.retrlines('LIST')
        

def main():
    hosts = grep_hosts(sys.argv[1], GNMAP_FTP)
    # for each host, we need to perform the following logic
    # 1. test server response, to obtain
    # 1.1 server fingerprinting
    #       - we are not re-inventing the wheel here. We just try to grab server header as quick as possible. Real fingerprinting kung fu should go to nmap instead
    # 1.2 root / response
    #       - try to text2html and screenshot
    #       - if forbidden at least show the content
    # 1.3 robots.txt
    #       - alert if exists
    #       - iterate entries
    # 1.4 dirbusting?
    """
    log('test')
    log_green('test_green')
    log_red('test_red')
    log_blue('test_blue')
    log('test_white')
    """
    options={'timeout':3}
    for host in hosts:
        log("*** HOST %s ***" % host)
        try:
            request_anon(host, **options)
        except Exception as e:
            print e
            log_red('Exception occured. Skipping to next host')

    

if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
    else:
        main()
