#!/bin/bash
TARGET="10.11.1.1-254"
nmap -vv -sS -p 139 --script smb-enum-shares ${TARGET}
