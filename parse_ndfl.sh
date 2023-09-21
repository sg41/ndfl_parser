#!/bin/bash
SOURCE_FILES_MASK=~/Documents/Trading/BCS/*2-ндфл*.pdf
IFS=$'\n'; for file  in $(ls $SOURCE_FILES_MASK); do echo $file;  python ndfl_parser.py -f  "$file"; done