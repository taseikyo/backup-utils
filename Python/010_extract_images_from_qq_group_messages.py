#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-08-30 11:29:58
# @Author  : Lewis Tian (taseikyo@gmail.com)
# @Link    : github.com/taseikyo
# @Version : Python 3.8

"""
从 QQ 群备份消息中提取图片
注意，备份格式是 mth 才行
"""

import os
import base64


def extract(path: str = ".") -> None:
    """
    将脚本目录下所有的 .mht 消息中图片都解包出来
    """
    for file in os.listdir(path):
        if not file.endswith("mht"):
            continue

        with open(f"{path}/{file}", encoding="utf-8") as f:
            # 图片 id 和后缀
            name = ""
            ext = ""
            # base64 编码的图片内容
            img_content = []
            # 标记是否开始保存到 img_content
            content_start = False
            for line, txt in enumerate(f):
                if txt.startswith("Content-Type:image"):
                    ext = txt.split("/")[-1][:-1]
                if txt.startswith("Content-Location"):
                    name = txt.split("{")[-1].split("}")[0]

                if content_start:
                    img_content.append(txt)

                if ext and txt == "\n":
                    content_start = not content_start

                if not content_start and img_content:
                    save(f"{name}.{ext}", img_content)
                    img_content.clear()


def save(name: str, img_content: list) -> None:
    """
    将图片保存为 imgs/$name
    name 中包含图片的 id 和后缀名，如 123-345-678.gif
    """
    if not os.path.exists("imgs"):
        os.mkdir("imgs")
    try:
        imgdata = base64.b64decode("".join(img_content))
    except Exception as e:
        print(e)
        print("fail to decode the `img_content` using base64 :O")
        return
    try:
        with open(f"imgs/{name}", "wb") as f:
            f.write(imgdata)
        print(f"{name} has been saved :3")
    except Exception as e:
        print(e)
        print(f"fail to save imgs/{name} :(")


if __name__ == "__main__":
    extract()
