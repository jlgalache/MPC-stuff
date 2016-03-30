#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os
import sys

# Set up the arguments to be supplied to the routine:
parser = argparse.ArgumentParser()
#parser.add_argument('-in','--flat_filename', help='Name of the file you want to convert')
#parser.add_argument('-out','--output_filename', help='Name of the output file')
parser.add_argument('-of','--options_file', action='store_true', default=False, dest='boolean_switch', help='Inputs provided through convert_flatfile_options.txt')
parser.add_argument('-in','--flat_filename', default='', type=str, help='Name of the file you want to convert')
parser.add_argument('-out','--output_filename', default='-1', type=str, help='Name of the output file; if missing, input filename will be used with a JSON extension')
parser.add_argument('-hl','--header_lines', default=0, type=int, help='Number of header lines')
parser.add_argument('-cnl','--col_name_line', default=-1, type=int, help='Line number where column names are found')
parser.add_argument('-s','--separator', default='', help='Column separator')
parser.add_argument('-cs','--col_start', nargs='*', default=-1, type=int, help='Column start')
parser.add_argument('-cw','--col_width', nargs='*', default=-1, type=int, help='Column width')
parser.add_argument('-ct','--col_type', nargs='*', default='', help='Column data type')
parser.add_argument('-cn','--col_names', nargs='*', default='', type=str, help='Column names if you don\'t want to use the header or it\'s missing')
parser.add_argument('-nr','--num_rows', default=-1, type=int, help='Number of data rows to read')
args = parser.parse_args()

if args.options_file:
  with open('convert_flatfile_options.txt','r') as options_file:
    for line in options_file:
      if line.startswith('flat_filename'):
        args.flat_filename = line.split(':')[1].strip().strip('\'"')
      elif line.startswith('output_filename'):
        args.output_filename = line.split(':')[1].strip().strip('\'"')
      elif line.startswith('header_lines'):
        args.header_lines = int(line.split(':')[1].strip().strip('\'"'))
      elif line.startswith('col_name_line'):
        args.col_name_line = int(line.split(':')[1].strip().strip('\'"'))
      elif line.startswith('separator'):
        args.separator = line.split(':')[1].strip()strip('\'"')
      elif line.startswith('col_start'):
        args.col_start = list(map(int, line.split(':')[1].strip().split(' ')))
      elif line.startswith('col_width'):
        args.col_width = list(map(int, line.split(':')[1].strip().split(' ')))
      elif line.startswith('col_type'):
        args.col_type = [i.strip('\'"') for i in line.split(':')[1].strip().split(' ')] # Get rid of spurious ' or "
      elif line.startswith('col_names'):
        args.col_names = [i.strip('\'"') for i in line.split(':')[1].strip().split(' ')] # Get rid of spurious ' or "
      elif line.startswith('num_rows'):
        args.num_rows = int(line.split(':')[1].strip().strip('\'"'))

# Catch errors that will be caused by missing arguments:
if args.flat_filename == '':
  print(' ERROR: No input file is supplied; a file name must be supplied via the -in option.')

if args.header_lines == 0 and args.col_names == '':
  print(' ERROR: If the file has no header, column names must be supplied via the -cn option.')
  sys.exit(1)
  
if args.separator == '' and (args.col_start == -1 or args.col_width == -1):
  print(' ERROR: If no separator is supplied, then the column start points and widths must be supplied via the -cs and -cw options.')
  sys.exit(1)

if args.separator != '' and args.col_type == '':
  print(' ERROR: If you define a separator, you must also supply column data types via the -cn option.')
  sys.exit(1)

if args.col_name_line != -1 and args.col_names == '':
  print(' ERROR: No column names are supplied; column names must be supplied via the -cn option or read from the file header via the -cnl option.')
  sys.exit(1)

if args.col_type == '':
  print(' WARNING: No column data type was supplied; all columns will be imported as strings.')
  args.col_type = ['str' for i in range(0, len(args.col_names))]



# Make filename for the JSON file if user doesn't specify a name:
if args.output_filename == '-1':
  args.output_filename = os.path.splitext(args.flat_filename)[0]+'.json'

input_file = open(args.flat_filename, 'r')

# Get column names from the appropriate line in the file or from the names provided via argument:
if args.col_name_line != -1:
  for read_count, line in enumerate(input_file):
    if (read_count+1) == args.col_name_line:
      headings = []
      for i, j in enumerate(args.col_start):
        headings.append(str.strip(line[j:j+args.col_width[i]]))
      break
else:
  headings = args.col_names
  read_count = 0

# Debugging prinouts:
print(' Input file: '+args.flat_filename)
print(' New Input file: '+args.flat_filename)
print(' Output file: '+args.output_filename)
print(' Column starts: '+str(args.col_start)+' and length is: '+str(len(args.col_start)))
print(' Column width: '+str(args.col_width)+' and length is: '+str(len(args.col_width)))
print(' Column type: '+str(args.col_type)+' and length is: '+str(len(args.col_type)))
print(' Column names: '+str(args.col_names)+' and length is: '+str(len(args.col_names)))
print(' CNL: '+str(args.col_name_line))




# Get to the line where the data starts:
if args.header_lines > read_count:
  for i, line in enumerate(input_file): 
    if i == (args.header_lines - read_count - 2):
      break

output_json_file = open(args.output_filename, 'w')
output_json = []

# Start reading in data:
for count, line in enumerate(input_file):
  if count == args.num_rows:
    break # Read only specified number of rows if -rn option is set
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
