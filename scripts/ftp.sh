#!/bin/bash
TARGET="10.11.1.1-254"
time nmap -v -p 21 --script ftp-anon ${TARGET}
