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


def flv2mp4(path: str = ".") -> None:
    """
    convert flv to mp4
    """
    files = [f for f in os.listdir(path) if f.endswith("flv")]
    for file in files:
        ofile = os.path.splitext(file)[0]
        cmd = f"ffmpeg -i {path}/{file} -vcodec copy -acodec copy {path}/{ofile}.mp4"
        os.system(cmd)


def mp42ts(path: str = ".") -> None:
    """
    convert mp4 to ts
    """
    files = [f for f in os.listdir(path) if f.endswith("mp4")]
    for file in files:
        ofile = os.path.splitext(file)[0]
        cmd = f"ffmpeg -i {path}/{file} -vcodec copy -acodec copy -vbsf h264_mp4toannexb {path}/{ofile}.ts"
        os.system(cmd)


def merge(path: str = ".") -> None:
    """
    merge ts as mp4
    """
    files = [f"{path}/{f}" for f in os.listdir(path) if f.endswith("ts")]
    if not files:
        return
    cmd = f"""ffmpeg -i "concat:{'|'.join(files)}" -acodec copy -vcodec copy -absf aac_adtstoasc {path}/output.mp4"""
    os.system(cmd)


if __name__ == "__main__":
    flv2mp4()
    mp42ts()
    merge()
