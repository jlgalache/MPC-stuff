#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os
import sys
import textwrap



# Set up the arguments to be supplied to the routine:
#parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,description=textwrap.dedent('''
The options file will list the arguments. Here are some examples of valid files:

 * Listing all valid arguments:
 
  flat_filename: any_name.txt
  output_filename: any_other_name.json
  col_type: 'str' 'int' 'int' 'int' 'flt'
  col_names: 'Col_A' 'Col_B' 'Col_C' 'Col_D' 'Col_E'
  num_header_lines: 
  col_name_line: 
  separator: 
  col_start: 0 8 12 17 20
  col_width: 7 3 4 2 4
  num_rows: 10
  verbose: yes
  
 * Ommiting unnecessary arguments:
 
  flat_filename: any_name.txt
  col_start: 0 8 12 17 20
  col_width: 7 3 4 2 4
  col_type: 'str' 'int' 'int' 'int' 'flt'
  num_header_lines: 5
  col_name_line: 3
  
NOTES
=====

Order of the arguments is not important, and if any arguments are not 
specified, they can be ommited. Command line arguments shouldn't be 
mixed with arguments in the options file; use one or the other. 
The one exception is the 'verbose' option, which can be ommited from 
the options file but provided on the command line without affecting 
the correct functioning of the program.

Empty values are ommited from the JSON output. In the future there may
be an option to specify how they should be treated (e.g., as NaN), but
for now the particular keyword for the row will not be listed.

 - output_filename: If not provided, the output file will be named like 
       the input file with the extension changed.
 - separator: This capability is not yet implemented, so it can be left 
       blank or ommited.
 - col_type: If not provided, all data will be read in as strings.
 - verbose: If empty or 0, verbose is turned OFF; if any other symbol is 
       given, verbose will be turned ON.
'''))
parser.add_argument('-of','--options_file', default='', type=str, help='Arguments provided through a user-specified options file')
parser.add_argument('-in','--flat_filename', default='', type=str, help='Name of the file you want to convert')
parser.add_argument('-out','--output_filename', default='', type=str, help='Optional: Name of the output file; if missing, input filename will be used with a JSON extension')
parser.add_argument('-hl','--num_header_lines', default=0, type=int, help='Number of header lines')
parser.add_argument('-cnl','--col_name_line', default=-1, type=int, help='Line number where column names are found')
parser.add_argument('-s','--separator', default='', help='Column separator')
parser.add_argument('-cs','--col_start', nargs='*', default=-1, type=int, help='Column start')
parser.add_argument('-cw','--col_width', nargs='*', default=-1, type=int, help='Column width')
parser.add_argument('-ct','--col_type', nargs='*', default='', help='Column data type')
parser.add_argument('-cn','--col_names', nargs='*', default='', type=str, help='Column names if you don\'t want to use the header or it\'s missing')
parser.add_argument('-nr','--num_rows', default=-1, type=int, help='Number of data rows to read')
parser.add_argument("--verbose", help="Errors and warnings picked up by the script will be output to screen", action="store_true")
args = parser.parse_args()

# If options file was provided, read arguments into a dictionary...:
if args.options_file != '':
  options_dic = {}
  if args.options_file != '':
    with open(args.options_file,'r') as options_file:
      for line in options_file:
        options_dic[line.split(':')[0].strip()] = line.split(':')[1].strip()

# ...and set argument values:
  if 'flat_filename' in options_dic:
    args.flat_filename = options_dic['flat_filename'].strip('\'"')
  else:
    args.flat_filename = ''

  if 'output_filename' in options_dic:
    args.output_filename = options_dic['output_filename'].strip('\'"')
  else:
    args.output_filename = ''

  if 'num_header_lines' in options_dic:
    args.num_header_lines = options_dic['num_header_lines'].strip('\'"')
    if args.num_header_lines == '':
      args.num_header_lines = 0
    else:
      args.num_header_lines = int(args.num_header_lines)
  else:
    args.num_header_lines = 0

  if 'col_name_line' in options_dic:
    args.col_name_line = options_dic['col_name_line'].strip('\'"')
    if (args.col_name_line == '') or (args.col_name_line == '0'):
      args.col_name_line = -1
    else:
      args.col_name_line = int(args.col_name_line)
  else:
    args.col_name_line =  -1

  if 'separator' in options_dic:
    args.separator = options_dic['separator'].strip('\'"')
  else:
    args.separator = ''

  if 'col_start' in options_dic:
    if options_dic['col_start'] == '':
      args.col_start = -1
    else:
      args.col_start = list(map(int, options_dic['col_start'].split(' ')))
  else:
    args.col_start = -1

  if 'col_width' in options_dic:
    if options_dic['col_width'] == '':
      args.col_width = -1
    else:
      args.col_width = list(map(int, options_dic['col_width'].split(' ')))
  else:
    args.col_width = -1

  if 'col_type' in options_dic:
    if options_dic['col_type'] == '':
      args.col_type = ''
    else:
      args.col_type = [i.strip('\'"') for i in options_dic['col_type'].split(' ')] # Get rid of spurious ' or "
  else:
    args.col_type = ''

  if 'col_names' in options_dic:
    if options_dic['col_names'] == '':
      args.col_names = ''
    else:
      args.col_names = [i.strip('\'"') for i in options_dic['col_names'].split(' ')] # Get rid of spurious ' or "
  else:
    args.col_names = ''

  if 'num_rows' in options_dic:
    args.num_rows = options_dic['num_rows'].strip('\'"')
    if args.num_rows == '':
      args.num_rows = -1
    else:
      args.num_rows = int(args.num_rows)
  else:
    args.num_rows = -1 

  if 'verbose' in options_dic:
    if (str(options_dic['verbose']) == '') or (str(options_dic['verbose']) == '0'):
      args.verbose = bool(0)
    else:
      args.verbose = bool(1)


# Catch errors that will be caused by missing arguments or mismatched list lengths:
if args.flat_filename == '':
  if args.verbose:
    print(' ERROR: No input file is supplied; a file name must be supplied via the -in option.')
  sys.exit(1)

if args.num_header_lines == 0 and args.col_names == '':
  if args.verbose:
    print(' ERROR: If the file has no header, column names must be supplied via the -cn option.')
  sys.exit(1)
  
if args.separator == '' and (args.col_start == -1 or args.col_width == -1):
  if args.verbose:
    print(' ERROR: If no separator is supplied, then the column start points and widths must be supplied via the -cs and -cw options.')
  sys.exit(1)

if args.separator != '':
  if args.verbose:
    print(' ERROR: This feature is not currently implemented.')
  sys.exit(1)

if (args.col_name_line == -1) and (args.col_names == ''):
  if args.verbose:
    print(' ERROR: No column names are supplied; column names must be supplied via the -cn option or read from the file header via the -cnl option.')
  sys.exit(1)

if len(args.col_start) != len(args.col_width):
  if args.verbose:
    print(' ERROR: The number of arguments for the column start positions and the column widths do not match ('+str(len(args.col_start))+' vs '+str(len(args.col_width))+').')
  sys.exit(1)

if args.col_name_line == -1:
  if len(args.col_start) == len(args.col_width) and len(args.col_start) != len(args.col_names):
    if args.verbose:
      print(' ERROR: The number of arguments for the column names and the column start positions do not match ('+str(len(args.col_names))+' vs '+str(len(args.col_width))+').')
    sys.exit(1)

if args.col_type != '' and ((len(args.col_start) == len(args.col_width)) and (len(args.col_type) != len(args.col_start))):
  if args.verbose:
    print(' ERROR: The number of arguments for the column type and the column start positions do not match ('+str(len(args.col_type))+' vs '+str(len(args.col_start))+').')
  sys.exit(1)

if args.col_type == '':
  if args.verbose:
    print(' WARNING: No column data type was supplied; all columns will be imported as strings.')
  args.col_type = ['str' for i in range(0, len(args.col_names))]


# Make filename for the JSON file if user doesn't specify a name:
if args.output_filename == '':
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
#print(' Input file: '+args.flat_filename)
#print(' Output file: '+args.output_filename)
#print(' Column starts: '+str(args.col_start)+' and length is: '+str(len(args.col_start)))
#print(' Column width: '+str(args.col_width)+' and length is: '+str(len(args.col_width)))
#print(' Column type: '+str(args.col_type)+' and length is: '+str(len(args.col_type)))
#print(' Column names: '+str(args.col_names)+' and length is: '+str(len(args.col_names)))
#print(' Num rows to read: '+str(args.num_rows))
#print(' CNL: '+str(args.col_name_line))
#print(' Verbose: '+str(args.verbose))



# Get to the line where the data starts:
if args.num_header_lines > read_count:
  for i, line in enumerate(input_file): 
    if i == (args.num_header_lines - read_count - 2):
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

if args.verbose:
  print(' Your file \''+args.flat_filename+'\' was converted succesfully to \''+args.output_filename+'\'.')