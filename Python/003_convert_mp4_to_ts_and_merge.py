#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-09-14 17:55:55
# @Author  : Lewis Tian (taseikyo@gmail.com)
# @Link    : https://github.com/taseikyo
# @Version : Python3.7


"""
0. convert flv to mp4
1. convert mp4 to ts
2. merge ts to mp4
"""

import os


def flv2mp4():
    """
    convert flv to mp4
    """

    for x in os.listdir("."):
        if x.endswith("flv"):
            cmd = f"ffmpeg -i {x} -vcodec copy -acodec copy {x.split('.')[0]}.mp4"
            os.system(cmd)


def mp42ts():
    """
    convert mp4 to ts
    """
    for x in os.listdir("."):
        if x.endswith("mp4"):
            cmd = f"ffmpeg -i {x} -vcodec copy -acodec copy -vbsf h264_mp4toannexb {x.split('.')[0]}.ts"
            os.system(cmd)


def merge():
    """
    merge ts as mp4
    """
    files = []
    for x in os.listdir("."):
        if x.endswith("ts"):
            files.append(x)
    if not files:
        return
    cmd = f"""ffmpeg -i "concat:{'|'.join(files)}" -acodec copy -vcodec copy -absf aac_adtstoasc output.mp4"""
    os.system(cmd)


if __name__ == "__main__":
    flv2mp4()
    mp42ts()
    merge()
