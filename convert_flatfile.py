#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-in','--flat_filename', help='Name of the file you want to convert')
parser.add_argument('-out','--output_filename', help='Name of the output file')
parser.add_argument('-s','--separator', help='Column separator')
parser.add_argument('-cs','--col_start', help='Column start')
parser.add_argument('-cw','--col_width', help='Column width')
parser.add_argument('-ct','--col_type', help='Column data type')
parser.add_argument('-cn','--col_names', help='Column names if you don\'t want to use the header or it\'s missing')
args = parser.parse_args()

print(' Input file: '+args.flat_filename)
print(' Output file: '+args.output_filename)

input_file = open(args.flat_filename, 'r')

for line in input_file:
  headings = []
  for count, i in enumerate(args.col_start):
    headings.append(line[i:i+args.col_width[count]])
    
print(headings)