#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ABORTED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


import argparse
import urllib.request
from itertools import islice
import sys
import os
import mpc_essentials as me
import math
import time
from time import strftime
import urllib.request
import json
import shutil
import gzip


time_stamp = time.time()
start_time = time_stamp

# Get the name of the file to be converted:
parser = argparse.ArgumentParser()
#parser.add_argument('infile', default='', type=str, help='Name of the file to be converted to JSON')
parser.add_argument('-v','--verbose', action='store_true', help='Prints run status messages to screen')
parser.add_argument('--directory', default='', type=str, help='Name of the directory to place the output files in')
args = parser.parse_args()

infile_soul = 'CometEls'

if args.directory != '':
  args.directory = args.directory.rstrip('/')+'/'

# Open logfile and set starting time:
sys.stderr = open(args.directory+'make_mpcorb_extended.log', 'a')
localtime = time.localtime(time.time())
sys.stderr.write(strftime('%Y/%m/%d\n  %H:%M:%S - Run started (file: '+args.infile+')\n  ', localtime))

# Get the input file over the internet or locally from /base/public/iau/:
try:
  #urllib.request.urlretrieve('http://www.minorplanetcenter.net/iau/MPCORB/'+args.infile, infile_soul+'_infile.dat')
  shutil.copyfile('/base/public/iau/MPCORB/CometEls.txt', infile_soul+'_infile.dat')
except Exception as the_error:
  localtime = time.localtime(time.time())
  sys.stderr.write(strftime('%H:%M:%S - Problem downloading file: \n  http://www.minorplanetcenter.net/iau/MPCORB/'+args.infile+'\n  Error type: '+str(the_error)+'\n', localtime))
  sys.exit(1)

# Find length of header, if there is one (assumes header less than 100 lines long):
num_header_lines = 0
with open(infile_soul+'_infile.dat', 'r') as data_file:
  c = 0
  for  line in data_file:
    c = c + 1
    if line[:2] == '--':
      num_header_lines = c
      break
    if c > 100:
      break
