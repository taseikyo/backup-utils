#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-11-19 09:43:27
# @Author  : Lewis Tian (taseikyo@gmail.com)
# @Link    : https://github.com/taseikyo
# @Version : python3.8

'''
convert qq lyric (.qrc) fromat to lrc format
'''

import os
import sys


def qrc_to_lrc(qrc: str):
    '''@qrc: .qrc file path
    '''
    print(f'start to convert [{qrc}]...')

    if not os.path.exists(qrc):
        print(f'[{qrc}] does not exist...')
        return False

    with open(qrc, encoding='utf-8') as fp:
        qrc_str = fp.read()

    escape_table = {
        '&#58;': ':',
        '&#10;': '\n',
        '&#46;': '.',
        '&#32;': ' ',
        '&#45;': '-',
        '&#40;': '(',
        '&#41;': ')'
    }

    for key, value in escape_table.items():
        qrc_str = qrc_str.replace(key, value)

    with open(f'{qrc}.lrc', 'w', encoding='utf-8') as fp:
        fp.write(qrc_str)

    print(f'[{qrc}] is converted to [{qrc}.lrc]...\n')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('You should input your .qrc file path!')
        print(f'[example] python {__file__} 0039MnYb0qxYhV.qrc')
    else:
        any(map(qrc_to_lrc, sys.argv[1:]))
