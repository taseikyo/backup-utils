#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-04-26 11:38:54
# @Author  : Lewis Tian (taseikyo@gmail.com)
# @Link    : https://github.com/taseikyo
# @Version : Python3.7

import os
import sys

'''
clear netease-cloud-music cache
    for `load music failed` error

cache default path:
    `c:/users/xyz/appdata/local/netease/cloudmusic/cache`
'''


def clear_netease_cloud_music_cache(path: str):
    '''@path: music cache path
    '''
    for file in os.listdir(path):
        if os.path.isdir(f'{path}/{file}'):
            clear_netease_cloud_music_cache(f'{path}/{file}')
        else:
            try:
                os.remove(f'{path}/{file}')
            except:
                print(f'can not remove `{path}/{file}`')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        path = f"{os.environ['LOCALAPPDATA']}/netease/cloudmusic/cache"
    else:
        path = sys.argv[1]
    clear_netease_cloud_music_cache(path)
