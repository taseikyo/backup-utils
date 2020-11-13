#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-01-08 11:32:09
# @Author  : Lewis Tian (taseikyo@gmail.com)
# @Link    : github.com/taseikyo
# @Version : python3.8

"""
download & convert bilibili cc subtitles
to srt subtitle format
"""

import re
import requests
import datetime


def obtain_cc_subtitle(avid: str = "77948393") -> None:
    """
    obtain cc subtitles

    $avid: id of the video
    """
    url = f"https://www.bilibili.com/video/av{avid}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    }
    r = requests.get(url, headers=headers)
    subtitle_urls = re.findall(r"subtitle_url\":\"(.*?json)", r.text)
    if not subtitle_urls:
        print("There is no cc subtitle in this video!")
        return

    for url in subtitle_urls:
        url = url.replace("\\u002F", "/")
        r = requests.get(url, headers=headers)
        convert_to_srt(url.split("/")[-1].split(".")[0], r.json()["body"])


def convert_to_srt(srt_id: str, subtitles: list) -> None:
    """
    convert cc subtitles to srt subtitles

    $subtitles: a json foramt cc subtitles
    """
    srt = []
    for index, subtitle in enumerate(subtitles):
        from_timestamp = convert_timestamp_format(subtitle["from"])
        to_timestamp = convert_timestamp_format(subtitle["to"])
        srt_tmp = f"""{index}\n{from_timestamp} --> {to_timestamp}\n{subtitle["content"]}\n"""
        srt.append(srt_tmp)

    with open(f"{srt_id}.srt", "w", encoding="utf-8") as f:
        f.write("\n".join(srt))


def convert_timestamp_format(cc_timestamp: float) -> str:
    """
    convert cc timestamp format to srt subtitles timestamp format

    $cc_timestamp: a seconds format cc timestamp
    """
    cc_timestamp = str(cc_timestamp)
    s = 0
    mm = 0
    if "." in cc_timestamp:
        s = int(cc_timestamp.split(".")[0])
        mm = int(cc_timestamp.split(".")[1])
    else:
        s = int(cc_timestamp)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return f'{h:02d}:{m:02d}:{s:02d},{mm:03d}'

if __name__ == "__main__":
    obtain_cc_subtitle("60977932")
