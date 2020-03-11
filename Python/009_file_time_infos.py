#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-03-10 15:29:05
# @Author  : Lewis Tian (taseikyo@gmail.com)
# @Link    : github.com/taseikyo
# @Version : Python3.7


"""
get file size, access time, modification time and creation time
"""

import os
import sys
import time


def get_file_size(path):
    index = 0
    ext = ["B", "KB", "MB", "GB", "TB"]
    fsize = os.path.getsize(path)
    while fsize > 1024:
        fsize /= 1024
        index += 1
    return f"{round(fsize, 2)}{ext[index]}"


def get_file_access_time(path):
    t = os.path.getatime(path)
    return timestamp_to_time(t)


def get_file_create_time(path):
    t = os.path.getctime(path)
    return timestamp_to_time(t)


def get_file_modify_time(path):
    t = os.path.getmtime(path)
    return timestamp_to_time(t)


def timestamp_to_time(timestamp):
    t = time.localtime(timestamp)
    return time.strftime("%Y-%m-%d %H:%M:%S", t)


def main():
    if len(sys.argv) < 2:
        print("input file path!")
    else:
        path = sys.argv[1]
        print(
            f"file size: {get_file_size(path)}\n"
            f"access time: {get_file_access_time(path)}\n"
            f"modification time: {get_file_modify_time(path)}\n"
            f"creation time: {get_file_create_time(path)}"
        )


if __name__ == "__main__":
    main()
