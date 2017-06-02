#!/bin/bash
#set -x
SCRIPTNAME=$0
GREP_PATTERN="80/open/tcp//http"
MODULE="HTTP"

grep_targets(){
    local GREP_PATTERN=$1
    local GREP_FILE=$2
    $1=`grep "${GREP_PATTERN}" ${GREP_FILE} | awk '{print $2}'`
}

usage(){
    echo "${SCRIPTNAME} <nmap file>"
    exit 0
}

log(){
    if [[ $# -ge 1 ]]; then
    case "$1" in
        red)
            COLOR_CODE="31"
            ;;
        green)
            COLOR_CODE="32"
            ;;
        blue)
            COLOR_CODE="34"
            ;;
        magenta)
            COLOR_CODE="35"
            ;;
        cyan)
            COLOR_CODE="36"
            ;;
    esac
    echo -en  "\e[${COLOR_CODE}m"
    shift 
    fi

    if [[ -n "${*// }" ]]; then    
        echo -n "$HOST $MODULE $*"
    fi

    # fall back to default
    echo -e "\e[39m"
}

[[ $# -eq 0 ]] && usage

GNMAP_FILE=$1

# Grep all related hosts
HOSTS=`grep "${GREP_PATTERN}" ${GNMAP_FILE} | awk '{print $2}'`

# now each host per line
for HOST in ${HOSTS}; do
    # grep server header
    # try access /

    # do we need python to fork in parallel instead?
    log green "Attempting to fetch server header"
    RESPONSE=$(curl -D - -sL http://${HOST}/ 2>&1 | tee -a test-output)
    printf "%s"  $RESPONSE
    SERVER_HEADER=`printf "%s" ${RESPONSE} | sed -n "s/\(Server:.*\)/\\1/p"`
    if [[ -n "${SERVER_HEADER// }" ]]; then 
        log blue ${SERVER_HEADER}
    else
        log blue "No Server header found"
    fi
done




# First, try to probe these http
