#!/bin/bash
# @Date    : 2019-10-24 16:52:45
# @Author  : Lewis Tian (taseikyo@gmail.com)
# @Link    : github.com/taseikyo

# get pid according to process-name
# and kill the process

if [ -n "$1" ]; then
    pid=$(ps -ef | grep $1 | grep -v grep | grep -v sh | awk '{print $2}')

    echo "$1 pid: ${pid}"
    kill ${pid}
else
    echo "plz input process name!"
    echo "[example] $0 taseikto.py"
fi