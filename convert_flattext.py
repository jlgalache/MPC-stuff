#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse



parser = argparse.ArgumentParser()
parser.add_argument('flat_filename', help='Name of the file you want to convert')
parser.add_argument('output_filename', help='Name of the output file')
parser.add_argument('separator', help='Column separator')
args = parser.parse_args()


input_file = open(args.flat_filename, 'r')

for line in input_file