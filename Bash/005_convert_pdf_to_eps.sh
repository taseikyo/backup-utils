#!/bin/bash
# @Date    : 2020-12-28 18:22:17
# @Author  : Lewis Tian (taseikyo@gmail.com)
# @Link    : github.com/taseikyo

# https://tex.stackexchange.com/questions/20883/how-to-convert-pdf-to-eps
# Convert PDF to eps (encapsulated PostScript)
# usage:
# pdf2eps <page number> <pdf file without ext> [<output eps filename without ext>]

[ $# -lt 2  ] &&  echo "$0 <page number> <pdf file without ext> [<output eps filename without ext>]" && exit 1
[ $# -eq 3 ] && output=$3 || output=$2

pdfcrop "$2.pdf" "$2-temp.pdf"
pdftops -f $1 -l $1 -eps "$2-temp.pdf" "$output.eps"
rm -rf "$2-temp.pdf"
