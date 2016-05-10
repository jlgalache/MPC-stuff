#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This script reads in any the MPC's three ID files and combines them into one single JSON file.
#
# Unlike with the ID files, the JSON file uses only unpacked designations

import argparse
import urllib.request
import sys
import os
import mpc_essentials as me
import time
from time import strftime
import urllib.request
import json
import shutil
import gzip

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
#localtime = time.localtime(time.time())
#sys.stderr.write(strftime('%Y/%m/%d\n  %H:%M:%S - Run started (file: MPC ID files)\n  ', localtime))

# Get the file with the discovery circumstances of the numbered minor planets:
try:
  urllib.request.urlretrieve('http://www.minorplanetcenter.net/iau/lists/NumberedMPs.txt', 'NumberedMPs.txt')
  #shutil.copyfile('iau/lists/NumberedMPs.txt', 'NumberedMPs.txt')
except Exception as the_error:
  localtime = time.localtime(time.time())
  sys.stderr.write(strftime('%H:%M:%S - Problem downloading file: \n  http://www.minorplanetcenter.net/iau/lists/NumberedMPs.txt\n  Error type: '+str(the_error)+'\n', localtime))
  sys.exit(1)

numberedmps_dic = {}
with open('NumberedMPs.txt', r) as nummps_file:
  for line in nummps_file:
    line_dic = {}
    key = line[:9].lstrip('(').rstrip(')')
    name = line[9:29].strip()
    p_desig = line[29:41].strip()
    line_dic['Discovery_date'] = '-'.join(line[41:52].split())
    line_dic['Discovery_site'] = line[53:71]
    ref = line[71:77]
    if ref != '':
      line_dic['Ref'] = ref
    line_dic['Discoverers'] = line[78:150]
    
  
  

