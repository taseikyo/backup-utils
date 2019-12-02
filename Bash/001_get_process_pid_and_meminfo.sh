#!/bin/bash
# @Date    : 2019-10-24 16:52:45
# @Author  : Lewis Tian (taseikyo@gmail.com)
# @Link    : github.com/taseikyo

# get pid according to process-name
# and print process's memory info

if [ -n "$1" ]; then
    pid=$(ps -ef | grep $1 | grep -v grep | grep -v sh | awk '{print $2}')

    echo "$1 pid: ${pid}"
    cat /proc/${pid}/status
else
    echo "plz input process name!"
    echo "[example] $0 taseikto.py"
fi
