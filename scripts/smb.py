#!/usr/bin/env python
import sys,os
import subprocess
# this module requires requests library
from ftplib import FTP
from common import *

def nmap_scripts(hosts):
    command="nmap -p 445 -d --script smb-enum-shares,smb-ls,smb-vuln-* %s" % ' '.join(hosts)
    log(command)
    result = subprocess.check_output(command, shell=True)
    log(result)


def main():
    hosts = grep_hosts(sys.argv[1], GNMAP_SMB)
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
    nmap_scripts(hosts)
    

if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
    else:
        main()
