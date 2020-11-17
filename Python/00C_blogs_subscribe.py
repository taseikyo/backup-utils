#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-05-25 18:29:10
# @Author  : Lewis Tian (taseikyo@gmail.com)
# @Link    : github.com/taseikyo
# @Version : Python3.8

"""
将订阅的博客拉取到本地
使用 pandoc 将其转化为 markdown 格式
"""

import os
import re
import time
import requests
from selenium import webdriver
from bs4 import BeautifulSoup as Soup


HEADERS = {
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36",
}


def get_ruanyf_weekly():
    """
    获取阮一峰技术周刊最新一期
    """
    url = "https://github.com/ruanyf/weekly"
    r = requests.get(url, headers=HEADERS).text
    result = re.findall(r"<a href=\"(.*?issue-\d*\.md)\">(.*?)</a>", r)
    url, num = result[0]

    if os.path.exists(f"blogs/ruanyf_weekly_{num}.md"):
        print(f"blogs/ruanyf_weekly_{num}.md has already existed!")
        return

    readme_url = "https://github.com" + url
    readme_content = requests.get(readme_url, headers=HEADERS).text

    bs = Soup(readme_content, "html5lib").find("article")

    html = f"""
        <html lang="en">
        <head>
            <meta charset="UTF-8">
        </head>
        <body>
            <div>
                <a href="{readme_url}">阮一峰技术周刊{num} 📅</a></br></br>
                {bs}
            <div>
        </body>
        </html>
    """

    prefix = "blogs/ruanyf_weekly_"
    with open(f"{prefix}{num}.html", "w", encoding="utf-8") as f:
        f.write(html)

    try:
        cmd = f'pandoc "{prefix}{num}.html" -o "{prefix}{num}.md"'
        os.system(cmd)
        os.remove(f"{prefix}{num}.html")
        with open(f"{prefix}{num}.md", encoding="utf-8") as f:
            data = f.read()
        data = re.sub(r"{#.*?}", "", data)
        with open(f"{prefix}{num}.md", "w", encoding="utf-8") as f:
            f.write(data)
    except Exception as e:
        print(e)
        return


def get_lofter_blogs(uname, greedy=False):
    """
    获取 lofter 的博客

    @uname: 链接关键词
    @greedy: 是否爬取所有博客

    加密算法难搞，直接用 selenium 简单完事
    由于样式的问题，还是不转化为 md 算了
    """
    url = f"https://{uname}.lofter.com/view"
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(1)
    driver.get(url)
    time.sleep(1.5)
    divs = Soup(driver.page_source, "html5lib").find_all(
        "div", {"class": "m-filecnt"})
    for div in divs:
        # 每个 div 对应一个月的博客，下面 ul 包含的 li 对应是每一篇
        blog_urls = div.find("ul").find_all("li")
        for bu in blog_urls:
            blog_url = bu.a["href"]
            driver.get(f"https://kouucocu.lofter.com{blog_url}")
            time.sleep(1.5)
            post = Soup(driver.page_source, "html5lib").find(
                "div", {"class": "postinner"}
            )
            html = f"""
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                </head>
                <body>
                    <div>
                        {post}
                    <div>
                </body>
                </html>
            """
            prefix = f"blogs/{uname}_{blog_url.split('/')[-1]}"
            print(prefix)
            with open(f"{prefix}.html", "w", encoding="utf-8") as f:
                f.write(html)
            if not greedy:
                break
    driver.quit()


def main():
    if not os.path.exists("blogs"):
        os.mkdir("blogs")

    get_ruanyf_weekly()
    get_lofter_blogs("kouucocu")


if __name__ == "__main__":
    main()
