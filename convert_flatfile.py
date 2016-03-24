#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json


parser = argparse.ArgumentParser()
#parser.add_argument('-in','--flat_filename', help='Name of the file you want to convert')
#parser.add_argument('-out','--output_filename', help='Name of the output file')
parser.add_argument('flat_filename', help='Name of the file you want to convert')
parser.add_argument('output_filename', help='Name of the output file')
parser.add_argument('-hl','--header_lines', default=-1, type=int, help='Number of header lines')
parser.add_argument('-cnl','--col_name_line', default=-1, type=int, help='Line number where column names are found')
parser.add_argument('-nl','--num_rows', default=-1, type=int, help='Number of data rows to read')
parser.add_argument('-s','--separator', default='', help='Column separator')
parser.add_argument('-cs','--col_start', nargs='*', type=int, help='Column start')
parser.add_argument('-cw','--col_width', nargs='*', type=int, help='Column width')
parser.add_argument('-ct','--col_type', nargs='*', help='Column data type')
parser.add_argument('-cn','--col_names', nargs='*', default='', type=str, help='Column names if you don\'t want to use the header or it\'s missing')
args = parser.parse_args()

print(' Input file: '+args.flat_filename)
print(' Output file: '+args.output_filename)
print(' Column starts: '+str(args.col_start)+' and length is: '+str(len(args.col_start)))
print(' Column width: '+str(args.col_width)+' and length is: '+str(len(args.col_width)))
print(' Column type: '+str(args.col_type)+' and length is: '+str(len(args.col_type)))
print(' Column names: '+str(args.col_names)+' and length is: '+str(len(args.col_names)))
print(' CNL: '+str(args.col_name_line))

input_file = open(args.flat_filename, 'r')

# Get column names from the appropriate line or from the provided names
if args.col_name_line != -1:
  for read_count, line in enumerate(input_file):
    if (read_count+1) == args.col_name_line:
      headings = []
      for i, j in enumerate(args.col_start):
        headings.append(str.strip(line[j:j+args.col_width[i]]))
      break
else:
  if args.col_names == '':
    print('\n You\'re missing -cnl *and* -cn. You need one or the other to define the column names.\n')
    sys.exit(1)
  headings = args.col_names
  read_count = 0

# Get to the line where the data starts
if args.header_lines > read_count:
  for i, line in enumerate(input_file): 
    if i == (args.header_lines - read_count - 2):
      break

output_json_file = open(args.output_filename, 'w')
output_json = []

# Start reading in data
for line in input_file:
  line_dict = {}
  for  i, j in enumerate(args.col_start):
    if str.strip(line[j:j+args.col_width[i]]) != '':
      if args.col_type[i] == 'int':
        line_dict[headings[i]] = int(str.strip(line[j:j+args.col_width[i]]))
      elif args.col_type[i] == 'flt':
        line_dict[headings[i]] = float(str.strip(line[j:j+args.col_width[i]]))
      elif args.col_type[i] == 'str':
        line_dict[headings[i]] = str.strip(line[j:j+args.col_width[i]])
  output_json.append(line_dict)


json.dump(output_json, output_json_file, indent=0)
output_json_file.close()
input_file.close()
