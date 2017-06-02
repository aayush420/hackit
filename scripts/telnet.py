#!/usr/bin/env python
import sys,os
import subprocess
# this module requires requests library
from common import *
import urllib
import telnetlib
import time

result_obj = {}
output_path = 'output/'

def grab_banner(host, **kwargs):
    t = telnetlib.Telnet()
    t.open(host,23,kwargs['timeout'])
    # 3 seconds for waiting before grabing anything
    time.sleep(3)
    message = t.read_until()
    if message is None:
        raise Exception("timed out")
    log_green(message)
    t.close()
    

def main():
    hosts = grep_hosts(sys.argv[1], GNMAP_TELNET)
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
    try:
        os.mkdir(output_path)
    except OSError:
        pass
    

    options={'timeout':5, 'verify':False}
    for host in hosts:
        log("*** HOST %s ***" % host)
        try:
            grab_banner(host, **options)
        except:
            log_red("%s timed out. Skipping to next host" % host)


    

if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
    else:
        main()
