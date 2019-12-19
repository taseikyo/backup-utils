#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-03-31 13:25:51
# @Author  : Lewis Tian (taseikyo@gmail.com)
# @Link    : https://taseikyo.github.io
# @Version : Python3.7

"""
This is a dedicated script that generates a toc for my weekly markdown file.

Usage:
    add a [TOC] or [toc] tag to the .md file (put in a suitable location)
    this script will generate toc of the file 
    and replace the [TOC]/[toc]
"""

import sys


# @HAS_L1_TOC is True means your md file contant `# h1`
# so h2 indent is one '\t'
# if @HAS_L1_TOC is False
# then h2 indent is zero '\t'
HAS_L1_TOC = False


def auto_generate_toc(filename):
    print(f"generate toc for {filename}")
    with open(filename, encoding="utf-8") as f:
        lines = f.readlines()

    toc = []
    top_level = 4 if HAS_L1_TOC else 3

    for line in lines:
        if line.startswith("#####"):
            line = line.replace("##### ", "").strip()
            indent = "\t" * top_level
            toc.append(f"{indent}- [{line}](#{line.replace(' ', '-').lower()})")
        elif line.startswith("####"):
            line = line.replace("#### ", "").strip()
            indent = "\t" * (top_level - 1)
            toc.append(f"{indent}- [{line}](#{line.replace(' ', '-').lower()})")
        elif line.startswith("###"):
            line = line.replace("### ", "").strip()
            indent = "\t" * (top_level - 2)
            toc.append(f"{indent}- [{line}](#{line.replace(' ', '-').lower()})")
        elif line.startswith("##"):
            line = line.replace("## ", "").strip()
            indent = "\t" * (top_level - 3)
            toc.append(f"{indent}- [{line}](#{line.replace(' ', '-').lower()})")
        elif line.startswith("#"):
            line = line.replace("# ", "").strip()
            indent = "\t" * (top_level - 4)
            toc.append(f"{indent}- [{line}](#{line.replace(' ', '-').lower()})")

    for k, v in enumerate(lines):
        if v.find("TOC") >= 0 or v.find("toc") >= 0:
            lines[k] = "## Table of Contents\n" + "\n".join(toc) + "\n"
            break

    with open(filename, "w", encoding="utf-8") as f:
        f.write("".join(lines))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1:]
        any(map(auto_generate_toc, filename))
        input("input anything to exit...")
    else:
        print("input the README file...")
        print(f"[e.g.] python {__file__.replace('py', 'md')}")
        input("input anything to exit...")
