#!/usr/bin/env python
import sys,os
import subprocess
# this module requires requests library
import requests
import html2text
from common import *
import urllib

result_obj = {}
output_path = 'output/'


def request_root(host, **kwargs):
    r = requests.get('http://%s' % host, **kwargs)
    if r.status_code == 200:
        log_green('Web server responsed with HTTP 200')
    server_header = r.headers.get('Server')
    if server_header:
        log_green("Server: %s" % server_header)

def request_robots(host, **kwargs):
    headers = kwargs.get('headers',{})
    # to avoid blocked by some server
    if headers.get('User-Agent', None) is None:
        headers['User-Agent'] = 'Googlebot/2.1 ( http://www.google.com/bot.html)'
    _kwargs = kwargs.copy()
    _kwargs['headers'] = headers
    r = requests.get('http://%s/robots.txt' % host, **_kwargs)
    if r.status_code == 200:
        log_green('robots.txt found!')
        log(r.text)
        # should save the file to a certain folder, we need a function
        # save(host, 'robots.txt', r.text)
        output_result(host, 'http-robots', 'robots.txt', r.text, output_path)
        lines = r.text.split('\n')
        for line in lines:
            if line.startswith('#'):
                next
            cols = line.split(': ', 2)
            if len(cols) < 2:
                next
            if cols[0] in ['Allow', 'Disallow']:
                if cols[1].strip() != '/':
                    # try request the specific resources
                    _request_resources(host, cols[1].strip(), **kwargs)

def _request_resources(host, path, **kwargs):
    # request specific resources
    try:
        _kwargs = kwargs.copy()
        _kwargs['timeout']=5
        r = requests.get('http://%s/%s' % (host, path), **_kwargs)
    except requests.exceptions.ReadTimeout as e:
        pass
    else:
        if r.status_code == 200:
            text = html2text.html2text(r.text)
            log_green('Path %s is accessible' %path)
            log(text)
            output_result(host, 'http-text', path, html2text.html2text(r.text), output_path)
            output_result(host, 'http-raw', path, r.text, output_path)

                
        

def main():
    hosts = grep_hosts(sys.argv[1])
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
