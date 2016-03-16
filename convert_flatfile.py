#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse



parser = argparse.ArgumentParser()
parser.add_argument('flat_filename', help='Name of the file you want to convert')
parser.add_argument('output_filename', help='Name of the output file')
parser.add_argument('separator', help='Column separator')
parser.add_argument('col_start', help='Column start')
parser.add_argument('col_width', help='Column width')
parser.add_argument('col_type', help='Column data type')
parser.add_argument('col_names', help='Column names if you don\'t want to use the header or it\'s missing')
args = parser.parse_args()


input_file = open(args.flat_filename, 'r')

for line in input_file
  headings = line.split(args.separator)