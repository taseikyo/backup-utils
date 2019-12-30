#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-05-09 11:40:49
# @Author  : Lewis Tian (taseikyo@gmail.com)
# @Link    : https://github.com/taseikyo
# @Version : Python3.7

from glob import glob

"""
complete the path to images

note:
    images have to be `png` format

usage:
    put `-[fig{i}]` or `-[tab{i}]` or `-[alg{i}]` in proper position
    the script will replace it with ![fig{i}](images/{doc-prefix}.fig{i}.png)
    or ![tab{i}](images/{doc-prefix}.tab{i}.png)

example:
    001.Alto Lightweight VMs using Virtualization-aware Managed.md
    -[fig1] => ![fig1](images/001.fig1.png)
"""


def main():
    images = [i.split("\\")[-1] for i in glob("images/*.png")]

    for x in glob("*.md"):
        # whether file has been modified
        flag = False
        # doc number
        doc = x.split(".")[0]

        with open(x, encoding="utf-8") as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            if (
                line.find("-[fig") >= 0
                or line.find("-[tab") >= 0
                or line.find("-[alg") >= 0
            ):
                img_id = line.split("[")[-1].split("]")[0]
                img_name = f"{doc}.{img_id}.png"
                if img_name in images:
                    flag = True
                    lines[i] = f"![{img_id}](images/{img_name})"
                    lines[i] += "\n"

        if flag:
            with open(x, "w", encoding="utf-8") as f:
                f.write("".join(lines))


if __name__ == "__main__":
    main()
