#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-12-12 15:00:35
# @Author  : Lewis Tian (taseikyo@gmail.com)
# @Link    : github.com/taseikyo
# @Version : python3.5

"""
obtain video information that exceeds the play threshold
"""

import os
import sys
import csv
import requests
import pandas as pd

PLAY_THRESHOLD = 500


def obtain_video_play_info(mid, page=1):
    """obtain upper's (@mid) video information
    that exceeds the `PLAY_THRESHOLD`
    """
    url = "https://api.bilibili.com/x/space/arc/search"
    payloads = {
        "mid": mid,
        "ps": 30,
        "tid": 0,
        "pn": page,
        "keyword": "",
        "order": "pubdate",
        "jsonp": "jsonp",
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3904.97"
    }
    r = requests.get(url, headers=headers, params=payloads)

    videos = r.json()["data"]["list"]["vlist"]
    if not videos:
        return

    video_list = []
    for video in videos:
        video_aid = video["aid"]
        video_title = video["title"]
        video_play = video["play"]
        video_description = video["description"].replace("\n", " || ")
        video_created = video["created"]

        if video_play >= PLAY_THRESHOLD:
            video_list.append(
                [video_aid, video_title, video_play, video_description, video_created]
            )
        print(video_title, video_play)

    if video_list:
        dump(mid, video_list, page)

    obtain_video_play_info(mid, page + 1)


def dump(mid, data, page):
    """save @data as csv named @mid_@page.csv
    """
    print(f"begin to dump @{mid}'data page {page}...")
    with open(f"{mid}_{page}.csv", "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            [
                "video_aid",
                "video_title",
                "video_play",
                "video_description",
                "video_created",
            ]
        )
        writer.writerows(data)


def merge(mid):
    """merge all @mid_@page.csv to @mid.csv
    """
    merge_list = []
    files = os.listdir()
    for file in files:
        if file.startswith(f"{mid}"):
            merge_list.append(file)

    if len(merge_list) == 1:
        os.rename(merge_list[0], f"{mid}.csv")
        return

    df1 = pd.read_csv(merge_list[0], encoding="utf-8")
    for file in merge_list[1:]:
        df2 = pd.read_csv(file, encoding="utf-8")
        df1 = pd.concat([df1, df2], axis=0, ignore_index=True, sort=False)

    df1.to_csv(f"{mid}.csv", index=False)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("please input mid...")
        print(f"[example] python {__file__} 9272615")
    else:
        for mid in sys.argv[1:]:
            obtain_video_play_info(mid)
            merge(mid)
