#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020-09-21 11:26:59
# @Author  : Lewis Tian (taseikyo@gmail.com)
# @Link    : github.com/taseikyo
# @Version : python3.8

"""
bash 和 zsh 会记录重复命令 于是有了这个脚本来
去除 .zsh_history/.bash_history 中的重复命令

为了保持顺序 使用 set 和list

若想每次自动去重 可以将脚本放入 ~/.bashrc 中：

tian@node:~$ chmod +x ./remove_duplicate_cmds.py
tian@node:~$ echo "/home/tian/remove_duplicate_cmds.py" >> .bashrc
"""

import os
import time
from datetime import datetime

BASH_HISTORY_PATH = "/home/tian/.bash_history"
ZSH_HISTORY_PATH = "/home/tian/.zsh_history"
CMDER_HISTORY_PATH = "D:/Programs/cmder/config/.history"
# 定义一个时间阈值 避免每次切换/登录都要跑一遍
THRESHOLD_SECONDS = 3600


def cal_time(stamp):
    """
    计算 stamp 到当前时间的间隔秒数
    """
    t1 = datetime.utcfromtimestamp(time.time())
    t2 = datetime.utcfromtimestamp(stamp)
    return (t1 - t2).seconds


def cmd_history(path):
    """
    清理 cmder/bash 类似的历史记录
    这类历史记录仅仅记录命令而不记录多余的信息
    """
    table = set()
    cmds = []
    cnt = 0
    # 如果修改时间小于时间阈值则不管
    if cal_time(os.path.getmtime(path)) < THRESHOLD_SECONDS:
        return

    with open(path, encoding="utf-8") as f:
        for cmd in f:
            cnt += 1
            if cmd in table:
                continue
            table.add(cmd)
            cmds.append(cmd)

    print(f"{path} {cnt} -> {len(cmds)}")
    with open(path, "w", encoding="utf-8") as f:
        f.write("".join(cmds))


def zsh_history():
    """
    由于 zsh 会在命令前面加入时间戳
    所以需要一个 split 的操作
    """
    table = set()
    cmds = []
    cnt = 0
    # 如果修改时间小于时间阈值则不管
    if cal_time(os.path.getmtime(ZSH_HISTORY_PATH)) < THRESHOLD_SECONDS:
        return
    with open(ZSH_HISTORY_PATH, encoding="utf-8") as f:
        for cmd in f:
            cnt += 1
            purge_cmd = "".join(cmd.split(":")[2:])
            if purge_cmd in table:
                continue
            table.add(purge_cmd)
            cmds.append(cmd)

    print(f"{ZSH_HISTORY_PATH} {cnt} -> {len(cmds)}")
    with open(ZSH_HISTORY_PATH, "w", encoding="utf-8") as f:
        f.write("".join(cmds))


if __name__ == "__main__":
    if os.path.exists(BASH_HISTORY_PATH):
        cmd_history(BASH_HISTORY_PATH)
    if os.path.exists(ZSH_HISTORY_PATH):
        zsh_history()
    if os.path.exists(CMDER_HISTORY_PATH):
        cmd_history(CMDER_HISTORY_PATH)
