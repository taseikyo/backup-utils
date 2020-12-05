#!/bin/python3
# -*- coding: utf-8 -*-
# @Date    : 2020-12-05 15:30:26
# @Author  : Lewis Tian (taseikyo@gmail.com)
# @Link    : github.com/taseikyo
# @Version : python3.8

"""
Download lyric from https://music.163.com/

PyQt Version: https://github.com/taseikyo/NeteaseLyric

双语歌词在 potplayer 中测试使用没有问题

使用方法如下，仅传入 id 或者完整链接都 OK

1. parse("12345")
2. parse("https://music.163.com/#/song?id=12345/")
"""

import json
import requests
from faker import Faker


def lrc_to_dict(lyric: str) -> dict:
    """
    将歌词转为字典 {time: lyric}
    """
    lrc_dict = {}
    for line in lyric.strip().split("\n"):
        try:
            foo = line.split("]")
            timeline = foo[0][1:]
            # 认为歌词是 [01:38.90]xxxx
            # 即第二个字符为数字（可能存在超长串烧为 10+ 分钟）
            if not timeline[0].isdigit():
                continue
            # 不确定是否歌词中存在 "[]" 符号
            # 所以直接拼接一下
            lrc = "".join(foo[1:]).strip()
            lrc_dict[timeline] = [lrc]
        except Exception as e:
            print(line)

    return lrc_dict


def merge(lyric: str, tlyric: str) -> str:
    """
    将两种歌词按照时间轴合并

    $lyric: 歌词
    $tlyric: 如果是外语歌词，这个一般是中文
    """
    lyric_dict = lrc_to_dict(lyric)
    tlyric_dict = lrc_to_dict(tlyric)
    for timeline in lyric_dict.keys():
        if timeline in tlyric:
            lyric_dict[timeline] += tlyric_dict[timeline]

    def timeline_to_int(timeline: str) -> int:
        """
        convert time to int
        00:01.000
        mm:ss.uu
        mm*60*1000+ss*1000+uu
        """
        foo = timeline.split(":")
        mm = int(foo[0])
        ss, uu = [int(x) for x in foo[1].split(".")]
        return mm * 60 * 1000 + ss * 1000 + uu

    new_lyric_tuple = sorted(
        lyric_dict.items(), key=lambda x: timeline_to_int(x[0]))

    # for timeline, lrcs in new_lyric_tuple:
    #     if len(lrcs) == 1:
    #         print(f"[{timeline}]{lrcs[0]}")
    #     else:
    #         print(f"[{timeline}]{lrcs[0]}")
    #         print(f"[{timeline}]{lrcs[1]}")

    new_lyric = "\n".join(
        f"[{timeline}]{lrcs[0]}"
        if len(lrcs) == 1
        else "\n".join(f"[{timeline}]{lrc}" for lrc in lrcs)
        for (timeline, lrcs) in new_lyric_tuple
    )

    return new_lyric


def parse(mid: str) -> str:
    """
    返回对应 id 的歌词，如果存在双语歌词
    则合并时间轴再返回

    $mid: 歌曲的 id
    """
    if mid[:4] == "http":
        mid = mid.split("=")[-1].split("/")[0]
    url = f"http://music.163.com/api/song/lyric?os=pc&id={mid}&lv=-1&kv=-1&tv=-1"
    headers = {
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": Faker().chrome()
    }
    try:
        r = requests.get(url, headers=headers)
        data = json.loads(r.text)
    except Exception as e:
        print(e)
        return ""
    lyric = data["lrc"]["lyric"]
    tlyric = data["tlyric"]["lyric"]
    if not tlyric:
        return lyric
    return merge(lyric, tlyric)


if __name__ == "__main__":
    mid = "1330348068"
    lrc = parse(mid)
    with open(f"{mid}.lrc", "w", encoding="utf-8") as f:
        f.write(lrc)
