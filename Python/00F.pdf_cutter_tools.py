#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-09-25 16:03:14
# @Author  : Lewis Tian (taseikyo@gmail.com)
# @Link    : github.com/taseikyo
# @Version : python3.8

"""
cutting pdf!

ref：https://blog.csdn.net/Qin1999/article/details/90707609
"""

import os
from PyPDF2 import PdfFileReader, PdfFileWriter


def mkdir(folder):
    """
    new folder and return the final folder
    """
    cnt = 1
    while os.path.exists(folder):
        folder = f"{folder}_{cnt}"
        cnt += 1
    os.mkdir(folder)
    return folder


def cut_in_fixed_size(path: str, page_size: int = 10):
    """
    cut the pdf to a fixed size
    @path: the pdf file path
    @page_size: the cut size
    """
    assert os.path.exists(path) and page_size > 0

    file_folder, filename = os.path.split(path)
    # the output folder to save the cuting pdfs
    output_folder = f"{file_folder}/{os.path.splitext(filename)[0]}"
    output_folder = mkdir(output_folder)

    input_pdf = PdfFileReader(path, "rb")
    page_nums = input_pdf.getNumPages()
    print(f"{filename}: {page_nums}")
    output = PdfFileWriter()
    for index in range(page_nums):
        output.addPage(input_pdf.getPage(index))
        if (index + 1) % page_size == 0:
            output_filename = f"pages-{(index + 1) - page_size + 1}-{(index + 1)}.pdf"
            with open(f"{output_folder}/{output_filename}", "wb") as pdf:
                output.write(pdf)
            print(f"{output_folder}/{output_filename} has been saved!")
            output = PdfFileWriter()

    if page_nums % page_size:
        number = page_nums % page_size
        start = page_nums - number + 1
        end = page_nums
        output_filename = (
            f"pages-{start}.pdf" if start == end else f"pages-{start}-{end}.pdf"
        )
        with open(f"{output_folder}/{output_filename}", "wb") as pdf:
            output.write(pdf)
        print(f"{output_folder}/{output_filename} has been saved!")


def cut_in_range(path: str, page_start: int, page_end: int):
    """
    cut the pdf according to the range: [page_start, page_end)
    @path: the pdf file path
    @page_start: range start (including)
    @page_end: range start (excluding)

    note: page_start starts from 1!
    """
    assert os.path.exists(path) and page_end > page_start > 0

    file_folder, filename = os.path.split(path)
    # the output folder to save the cuting pdfs
    output_folder = f"{file_folder}/{os.path.splitext(filename)[0]}"
    output_folder = mkdir(output_folder)

    input_pdf = PdfFileReader(path, "rb")
    page_nums = input_pdf.getNumPages()
    print(f"{filename}: {page_nums}")

    assert page_end <= page_nums

    output = PdfFileWriter()
    for index in range(page_nums):
        if page_start <= index + 1 < page_end:
            output.addPage(input_pdf.getPage(index))
        elif index + 1 == page_end:
            output_filename = f"pages-{page_start}-{page_end-1}.pdf"
            with open(f"{output_folder}/{output_filename}", "wb") as pdf:
                output.write(pdf)
            break
    print(f"{output_folder}/{output_filename} has been saved!")


if __name__ == "__main__":
    PDF = "D:/Downloads/PDF/caspp.pdf"
    cut_in_fixed_size(PDF, 100)
    # [100, 120)
    cut_in_range(PDF, 100, 120)
