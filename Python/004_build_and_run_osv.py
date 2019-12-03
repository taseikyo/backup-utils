#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2019/10/11 15:50:30
# @Author  : Lewis Tian (taseikyo@gmail.com)
# @Link    : https://github.com/taseikyo
# @Version : Python3.7
# @Desc    : build and run osv

import os
from optparse import OptionParser


def main():
    usage = " python3 run.py -i [image_name] -m [mem_size(GB)]\n\tpython3 run.py -i python3x -m 4G"
    parser = OptionParser(usage)
    parser.add_option(
        "-i",
        "--image_name",
        dest="image_name",
        help="build image name",
        action="store",
        type="string",
        default="native-example",
    )
    parser.add_option(
        "-m",
        "--mem_size",
        dest="mem_size",
        help="initial dram memory size",
        type="string",
        default="2G",
    )
    parser.add_option(
        "--nvmsize",
        dest="nvm_size",
        help="initial nvm memory size",
        type="string",
        default="",
    )
    options, args = parser.parse_args()

    image_name = options.image_name or "native-example"
    mem_size = options.mem_size or "2G"
    if options.nvm_size:
        nvm_cmd = f"--nvmsize {options.nvm_size}"
    else:
        nvm_cmd = ""

    print(f"[buiding config: image: {image_name} mem: {mem_size}]\n")

    print(f"********\nbuild {image_name}....\n********")
    os.system(f"sudo ./scripts/build image={image_name}")

    print("********\nrunning.....\n********")
    os.system(f"sudo ./scripts/run.py -m {mem_size} {nvm_cmd}")


if __name__ == "__main__":
    main()
