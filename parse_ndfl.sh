#!/bin/bash
IFS=$'\n'; for file  in $(ls ~/Documents/Trading/BCS/*2-ндфл*.pdf); do echo $file;  python ndfl_parser.py -f  "$file"; done