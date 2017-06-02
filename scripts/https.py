#!/usr/bin/env python
import sys,os
import subprocess
# this module requires requests library
import requests
from common import *

def request_root(host, **kwargs):
    r = requests.get('https://%s' % host, **kwargs)
    if r.status_code == 200:
        log_green('Web server responsed with HTTP 200')
    server_header = r.headers.get('Server')
    if server_header:
        log_green("Server: %s" % server_header)

def request_robots(host, **kwargs):
    r = requests.get('https://%s/robots.txt' % host, **kwargs)
    if r.status_code == 200:
        log_green('robots.txt found!')
        log(r.text)
        

def main():
    hosts = grep_hosts(sys.argv[1], GNMAP_HTTPS)
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
    options={'timeout':3, 'verify':False}
    for host in hosts:
        log("*** HOST %s ***" % host)
        try:

            request_root(host, **options)
            request_robots(host, **options)
        except requests.ConnectTimeout as e:
            log_red("%s timed out. Skipping to next host" % host)


    

if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
    else:
        main()
