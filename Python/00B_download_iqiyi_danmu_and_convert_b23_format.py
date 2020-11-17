#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-03-18 10:25:13
# @Author  : Lewis Tian (taseikyo@gmail.com)
# @Link    : github.com/taseikyo
# @Version : Python3.7

"""
搜索、获取 爱奇艺 的弹幕，并转化为哔哩哔哩格式

参考:
- https://blog.csdn.net/qq_41297934/article/details/104463851
"""


import os
import re
import zlib
from xml.dom.minidom import parse
import xml.dom.minidom
import requests
from bs4 import BeautifulSoup as Soup


HEADERS = {
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
}

# 由于没有起止时间，直接设置出现时间为开始
# 终止时间为出现时间+XML_INTERVAL
XML_INTERVAL = 5


def search(kw: str) -> dict:
    """
    返回搜索结果和对应的 albumid
    """
    ret = {}
    url = f"https://so.iqiyi.com/so/q_{kw}"
    r = requests.get(url, headers=HEADERS)
    soup = Soup(r.text, "html5lib")
    cards = soup.find_all("div", {"desc": "card"})
    for card in cards:
        title = card.find("a", {"class": "main-tit"})["title"]
        info = card["data-searchpingback-position"]
        albumid = re.findall(r"albumid=(\d+)&", info)[0]
        ret[title] = albumid

    return ret


def obtain_tvid(albumid: str) -> list:
    """
    返回 albumid 对应的所有 {tvid: duration}
    """
    ret = []
    page = 1
    while 1:
        url = f"https://pcw-api.iqiyi.com/albums/album/avlistinfo?aid={albumid}&page={page}&size=30"
        r = requests.get(url, headers=HEADERS)
        data = r.json()["data"]
        try:
            tv_list = data["epsodelist"]
        except:
            print("未找到数据")
            break
        for tv in tv_list:
            print(tv["tvId"], tv["name"], tv["duration"], tv["playUrl"])
            ret.append({str(tv["tvId"]): tv["duration"]})
        page += 1
        if page > data["page"]:
            break

    return ret


def obtain_bullet(tvid_info: dict) -> None:
    """
    弹幕链接为 https://cmts.iqiyi.com/bullet/视频编号的倒数4、3位/视频编号的倒数2、1位/视频编号_300_序号.z
    弹幕文件每5分钟（300秒）向服务器请求一次，故每集弹幕文件数量等于视频时间除以300之后向上取整
    然后返回是个压缩文件需要解压
    """
    if not os.path.exists("xml"):
        os.mkdir("xml")

    tvid, duration = list(tvid_info.items())[0]
    times = 0
    for x in duration.split(":"):
        times = times * 60 + int(x)

    pages = times // 300
    if times - pages * 300:
        pages += 1

    for page in range(1, pages + 1):
        url = f"https://cmts.iqiyi.com/bullet/{tvid[-4:-2]}/{tvid[-2:]}/{tvid}_300_{page}.z"
        res = requests.get(url, headers=HEADERS).content
        res_byte = bytearray(res)
        xml = zlib.decompress(res_byte).decode("utf-8")
        with open(f"xml/{tvid}_{page:03}.xml", "w", encoding="utf-8") as f:
            f.write(xml)


def xml_srt():
    """
    读取相同 id 的 xml 输出为 srt 字幕格式
    """
    if not os.path.exists("srt"):
        os.mkdir("srt")

    xmls = os.listdir("xml")
    ids = set([x.split("_")[0] for x in xmls])
    for xmlid in ids:
        srts = []
        for xml in xmls:
            if xml.startswith(xmlid):
                DOMTree = parse(f"xml/{xml}")
                root = DOMTree.documentElement
                bullets = root.getElementsByTagName("bulletInfo")
                for bullet in bullets:
                    content = bullet.getElementsByTagName("content")
                    time = bullet.getElementsByTagName("showTime")
                    srts.append([content[0].firstChild.data, time[0].firstChild.data])

        srt_str = []
        for index, (subtitle, time) in enumerate(srts):
            tmp = (
                f"""{index}\n{time}.00 --> {int(time)+XML_INTERVAL}.00\n{subtitle}\n"""
            )
            srt_str.append(tmp)
        with open(f"srt/{xmlid}.srt", "w", encoding="utf-8") as f:
            f.write("\n".join(srt_str))


def xml_b23xml():
    """
    <d p="0,1,25,16777215,1312863760,0,eff85771,42759017">前排占位置</d>
    第一个参数是弹幕出现的时间 以秒数为单位
    第二个参数是弹幕的模式1..3 滚动弹幕 4底端弹幕 5顶端弹幕 6.逆向弹幕 7精准定位 8高级弹幕
    第三个参数是字号， 12非常小,16特小,18小,25中,36大,45很大,64特别大
    第四个参数是字体的颜色 以HTML颜色的十位数为准
    第五个参数是Unix格式的时间戳。基准时间为 1970-1-1 08:00:00
    第六个参数是弹幕池 0普通池 1字幕池 2特殊池
    第七个参数是发送者的ID，用于“屏蔽此弹幕的发送者”功能
    第八个参数是弹幕在弹幕数据库中rowID 用于“历史弹幕”功能。
    """
    b23xml = """<?xml version="1.0" encoding="UTF-8"?>
<i>
<chatserver>chat.bilibili.com</chatserver>
<chatid>165771300</chatid>
<mission>0</mission>
<maxlimit>1500</maxlimit>
<state>0</state>
<real_name>0</real_name>
<source>k-v</source>
"""
    if not os.path.exists("b23"):
        os.mkdir("b23")

    danmu_pool = 0
    font_size = 25
    timestamps = 1584447851
    xmls = os.listdir("xml")
    ids = set([x.split("_")[0] for x in xmls])
    for xmlid in ids:
        danmus = []
        for xml in xmls:
            if xml.startswith(xmlid):
                DOMTree = parse(f"xml/{xml}")
                root = DOMTree.documentElement
                bullets = root.getElementsByTagName("bulletInfo")
                for bullet in bullets:
                    time = bullet.getElementsByTagName("showTime")[0].firstChild.data
                    mode = bullet.getElementsByTagName("position")[0].firstChild.data
                    if mode == "0":
                        mode = "1"
                    color = (
                        "0x" + bullet.getElementsByTagName("color")[0].firstChild.data
                    )
                    text = bullet.getElementsByTagName("content")[0].firstChild.data
                    uid = bullet.getElementsByTagName("uid")[0].firstChild.data
                    pid = uid
                    danmu = f'<d p="{time},{mode},{font_size},{int(color, 16)},{timestamps},{danmu_pool},{uid},{pid}">{text}</d>'
                    danmus.append(danmu)

        b23xml += "\n".join(danmus) + "\n</i>"
        with open(f"b23/{xmlid}.xml", "w", encoding="utf-8") as f:
            f.write(b23xml)


if __name__ == "__main__":
    print(search("爱情公寓"))
    # print(obtain_tvid(212447801))
    # obtain_bullet({"11298454000": "55:44"})
    # xml_srt()
    # xml_b23xml()
