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
localtime = time.localtime(time.time())
sys.stderr.write(strftime('%Y/%m/%d\n  %H:%M:%S - Run started (file: NumberedMPs.txt)\n  ', localtime))

# Get the file with the discovery circumstances of the numbered minor planets:
try:
  urllib.request.urlretrieve('http://www.minorplanetcenter.net/iau/lists/NumberedMPs.txt', 'NumberedMPs.txt')
  #shutil.copyfile('iau/lists/NumberedMPs.txt', 'NumberedMPs.txt')
except Exception as the_error:
  localtime = time.localtime(time.time())
  sys.stderr.write(strftime('%H:%M:%S - Problem downloading file: \n  http://www.minorplanetcenter.net/iau/lists/NumberedMPs.txt\n  Error type: '+str(the_error)+'\n', localtime))
  sys.exit(1)

numberedmps_dic = {}
with open('NumberedMPs.txt', 'r') as nummps_file:
  for line in nummps_file:
    line_dic = {}
    key = line[:8].lstrip(' (').rstrip(')')
    name = line[9:28].strip()
    if name != '':
      line_dic['Name'] = name
    p_desig = line[29:40].strip()
    if p_desig != '':
      line_dic['Principal_desig'] = p_desig
    line_dic['Discovery_date'] = '-'.join(line[41:51].split())
    discovery_asterisk = line[51].strip()
    if discovery_asterisk != '':
      line_dic['Discovery_rule'] = 'new'
    else:
      line_dic['Discovery_rule'] = 'old'
    line_dic['Discovery_site'] = line[53:71].strip()
    ref = line[71:76].strip()
    if ref != '':
      line_dic['Ref'] = ref
    line_dic['Discoverers'] = line[78:150].strip()
    numberedmps_dic[key] = line_dic

with open('NumberedMPs.json', 'w') as output_json_file:
  json.dump(numberedmps_dic, output_json_file, indent=0)

with open('NumberedMPs.json', 'rb') as input_file:
  with gzip.open(args.directory+'numberedmps.json.gz', 'wb', compresslevel=5) as output_file:
    shutil.copyfileobj(input_file, output_file)

os.remove('NumberedMPs.txt')
os.remove('NumberedMPs.json')


  
localtime = time.localtime(time.time())
sys.stderr.write(strftime('%H:%M:%S - Program finished without known errors\n', localtime))
sys.stderr.close()
sys.stderr = sys.__stderr__


