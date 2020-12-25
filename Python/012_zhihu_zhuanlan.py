#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Date    : 2020-12-25 10:37:34
# @Author  : Lewis Tian (taseikyo@gmail.com)
# @Link    : github.com/taseikyo
# @Version : python3.8

"""
保存知乎专栏文章为 HTML
并用 pandoc 转化为 Markdown
"""

import json
import os
import re
import time

import requests
from faker import Faker
from pyquery import PyQuery as query

# 转化为 Markdown 后删除 HTML
DEL_HTML = True


def get_column_pages(url: str, offset: int = 0):
    """
    获取 $url 专栏所有文章

    返回的 json 数据就包含了文章的内容
    所以我为什么要先写 get_one_page？
    """
    assert url.strip(), "Invalid url!"

    if url.startswith("c_"):
        cid = url
    elif url.startswith("http"):
        cid = url.split("/")[-1]
        if cid.endswith("/"):
            cid = cid[:-1]
    else:
        print("Bad url...")
    headers = {"user-agent": Faker().chrome()}
    json_file = f"files/{cid}_{offset//10}.json"
    if not os.path.exists(json_file):
        url = (
            f"https://www.zhihu.com/api/v4/columns/{cid}/items?limit=10&offset={offset}"
        )
        r = requests.get(url, headers=headers)

        with open(json_file, "w", encoding="utf-8") as f:
            f.write(r.text)

        data = r.json()
    else:
        with open(json_file, encoding="utf-8") as f:
            data = json.load(f)
    pages = data["data"]
    for page in pages:
        title = page["title"].replace("/", "_")
        page_id = page["id"]
        content = page["content"]
        dump_one_page(title, page_id, content)

    if not data["paging"]["is_end"]:
        get_column_pages(cid, offset + 10)
        time.sleep(1)


def dump_one_page(title: str, page_id: str, content: str):
    """
    保存文章
    $title: 文章标题
    $page_id: 文章的 id
    $content: 文章的 html 文档
    """
    print(f"\n***[SAVING {page_id}]***")
    html_file = f"files/{title} - {page_id}.html"
    md_file = f"files/{title} - {page_id}.md"
    print(f"Saving the article to {html_file}...")
    with open(f"{html_file}", "w", encoding="utf-8") as f:
        f.write(content)
    print("Converting html to md...")
    os.system(f'pandoc -o "{md_file}" "{html_file}"')
    print("Cleaning the md...")
    with open(f"{md_file}") as f:
        lines = f.readlines()
    text = re.sub(r"{\..*?}", "", "".join(lines), flags=re.S)
    while re.search(r"{\..*?}", text, flags=re.S):
        text = re.sub(r"{\..*?}", "", text, flags=re.S)
    text = text.replace("\\\n", "").replace(":::", "")
    with open(f"{md_file}", "w", encoding="utf-8") as f:
        f.write(text)

    if DEL_HTML:
        print(f"Removing {html_file}...")
        os.remove(f"{html_file}")


def get_one_page(url: str):
    """
    将 $url 对应的文章保存为 html 和 md
    虽然最后有清洗的步骤，最后格式还是需要手动调整（比如强迫症的我）
    """
    assert url.strip(), "Invalid url!"

    headers = {
        "user-agent": Faker().chrome(),
    }
    if url[-1] == "/":
        url = url[:-1]
    page_id = url.split("/")[-1]

    if not os.path.exists(f"files/{page_id}.html"):
        print(f"Retrieving {url}...")
        r = requests.get(url, headers=headers)
        doc = query(r.text)
        print(f"Saving the article to files/{page_id}.html...")
        with open(f"files/{page_id}.html", "w", encoding="utf-8") as f:
            f.write(doc("article").html())
    print("Converting html to md...")
    os.system(f"pandoc -o files/{page_id}.md files/{page_id}.html")
    print("Cleaning the md...")
    with open(f"files/{page_id}.md") as f:
        lines = f.readlines()

    trash_dots_lines = []
    for idx, line in enumerate(lines):
        if line.startswith(":::"):
            trash_dots_lines.append(idx)
        if re.search(r"{#.*?}", line):
            lines[idx] = re.sub(r"{#.*?}", "", line)

    for x in trash_dots_lines[::-1]:
        lines.pop(x)

    text = re.sub(r"{\..*?}", "", "".join(lines), flags=re.S)
    while re.search(r"{\..*?}", text, flags=re.S):
        text = re.sub(r"{\..*?}", "", text, flags=re.S)
    text = re.sub(r"<div>.*?</div>", "", text, flags=re.S)
    text = text.replace("\\\n", "").replace("\n\n\n", "\n\n").replace("\n\n\n", "\n\n")
    with open(f"files/{page_id}.md", "w", encoding="utf-8") as f:
        f.write(text)


if not os.path.exists("files"):
    os.mkdir("files")

if __name__ == "__main__":
    get_column_pages("c_1108400140804726784")
