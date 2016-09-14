#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This script reads in any the MPC's file of closest observed flybys and outputs an extended JSON version.
#
# The extended data are flyby distances in several other units in addition to the original AU.

import argparse
import urllib.request
from itertools import islice
import sys
import os
import time
from time import strftime
import json
import shutil
import gzip
import math

time_stamp = time.time()
start_time = time_stamp

# Get the name of the directory where the output file and log file will be located:
parser = argparse.ArgumentParser()
parser.add_argument('-v','--verbose', action='store_true', help='Prints run status messages to screen')
parser.add_argument('--directory', default='', type=str, help='Name of the directory to place the output files in')
args = parser.parse_args()

if args.directory != '':
  args.directory = args.directory.rstrip('/')+'/'

# Open logfile and set starting time:
sys.stderr = open(args.directory+'make_non-text_files.log', 'a')
localtime = time.localtime(time.time())
#sys.stderr.write(strftime('%Y/%m/%d\n  %H:%M:%S - Run started (file: ObsCodes.txt)\n  ', localtime))

# Get the file with the observing site ObsCodes:
try:
  #urllib.request.urlretrieve('http://www.minorplanetcenter.net/iau/lists/ObsCodes.html', 'ObsCodes.txt')
  shutil.copyfile('iau/lists/ObsCodes.html', 'ObsCodes.txt')
except Exception as the_error:
  localtime = time.localtime(time.time())
  sys.stderr.write(strftime('%H:%M:%S - Problem downloading file: \n  http://www.minorplanetcenter.net/iau/lists/ObsCodes.html\n  Error type: '+str(the_error)+'\n', localtime))
  sys.exit(1)


# Find length of header:
num_header_lines = 0
with open('ObsCodes.txt', 'r') as data_file:
  c = 0
  break_flag = 0
  for  line in data_file:
    if break_flag:
      break
    c = c + 1
    if line.strip() == '<pre>':
      for line in data_file:
        c = c + 1
        if line[:3].isnumeric():
          num_header_lines = c - 1
          break_flag = 1
          break

# Start reading the file:

obscode_dic = {}
with open('ObsCodes.txt', 'r') as data_file:
  head = list(islice(data_file, num_header_lines))
  for line in data_file:
    if line.strip() == '</pre>':
      break
    line_dic = {}
    key = line[:3]
    if line[4:30].strip() != '':
      if line[4:30].strip() != '0.000000.000000 0.000000':
        line_dic['Longitude'] = float(line[4:13].strip())
        cos = float(line[13:21].strip())
        line_dic['cos'] = cos
        sin = float(line[21:30].strip())
        line_dic['sin'] = sin
        lat = math.atan(sin/cos)
# Number of significant digits for the latitude is set to be the same as for the longitude:
        #line_dic['Latitude'] = "{value:9.{dec_places}f}".format(dec_places=len(line[4:13].strip().split('.')[1]), value=lat).strip()
        line_dic['Latitude'] = round(lat,len(line[4:13].strip().split('.')[1]))
        geo_dist = cos/math.cos(lat)
        line_dic['Geocentric_dist'] = round(cos/math.cos(lat),7)
      else:
        line_dic['Longitude'] = float(line[4:13].strip())
        line_dic['cos'] = float(line[13:21].strip())
        line_dic['sin'] = float(line[21:30].strip())
    line_dic['Name'] = line[30:151].strip()
    obscode_dic[key] = line_dic
    


with open('obscodes_extended.json', 'w') as output_json_file:
  json.dump(obscode_dic, output_json_file, indent=0)

with open('obscodes_extended.json', 'rb') as input_file:
  with gzip.open(args.directory+'obscodes_extended.json.gz', 'wb', compresslevel=5) as output_file:
    shutil.copyfileobj(input_file, output_file)

os.remove('ObsCodes.txt')
os.remove('obscodes_extended.json')

os.chmod(args.directory+'obscodes_extended.json.gz', 0o774)

sys.stderr.close()
sys.stderr = sys.__stderr__



