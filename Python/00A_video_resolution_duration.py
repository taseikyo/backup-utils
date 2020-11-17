#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-03-15 12:42:15
# @Author  : Lewis Tian (taseikyo@gmail.com)
# @Link    : github.com/taseikyo
# @Version : Python3.7

"""
get video resolution and duration using `ffmpeg`

reference:
- https://www.cnblogs.com/heweiblog/p/6955698.html
"""


import os
import shutil
import subprocess
import json


def get_resolution(filename: str) -> str:
    """
    returns the resolution as widthxheight
    """
    command = [
        "ffprobe",
        "-loglevel",
        "quiet",
        "-print_format",
        "json",
        "-show_streams",
        "-i",
        filename,
    ]
    result = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    out = str(result.stdout.read())
    out = out.replace("\\r\\n", "").replace(" ", "")[2:-1]

    try:
        width = json.loads(out)["streams"][1]["width"]
        height = json.loads(out)["streams"][1]["height"]
    except:
        width = json.loads(out)["streams"][0]["width"]
        height = json.loads(out)["streams"][0]["height"]

    return f"{width}x{height}"


def get_duration(filename: str) -> str:
    """
    returns video duration in seconds
    """
    command = [
        "ffprobe.exe",
        "-loglevel",
        "quiet",
        "-print_format",
        "json",
        "-show_format",
        "-i",
        filename,
    ]
    result = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    out = str(result.stdout.read())
    out = out.replace("\\r\\n", "").replace(" ", "")[2:-1]
    data = json.loads(out)["format"]["duration"]
    return data


def main():
    """
    move videos of the same resolution to the same directory
    """
    files = os.listdir()
    data = {}
    for file in files:
        if not file.endswith("mp4"):
            continue

        ret = get_resolution(file)
        if ret in data:
            data[ret].append(file)
        else:
            data[ret] = [file]

    for k, v in data.items():
        os.mkdir(k)
        for x in v:
            shutil.move(x, k)


if __name__ == "__main__":
    main()
