#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This script reads in any the MPC's three ID files and combines them into one single JSON file.
#
# Unlike with the ID files, the JSON file uses only unpacked designations

import argparse
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

# Get the 3 identification files:
# ids.txt lists the multi-opposition unnumbered objects:
try:
  #urllib.request.urlretrieve('http://www.minorplanetcenter.net/iau/ECS/MPCAT/ids.txt', 'ids.txt')
  shutil.copyfile('iau/ECS/MPCAT/ids.txt', 'ids.txt')
except Exception as the_error:
  localtime = time.localtime(time.time())
  sys.stderr.write(strftime('%H:%M:%S - Problem downloading file: \n  http://www.minorplanetcenter.net/iau/ECS/MPCAT/ids.txt\n  Error type: '+str(the_error)+'\n', localtime))
  sys.exit(1)

# dbl.txt lists the 1-opposition unnumbered objects:
try:
  #urllib.request.urlretrieve('http://www.minorplanetcenter.net/iau/ECS/MPCAT/dbl.txt', 'dbl.txt')
  shutil.copyfile('iau/ECS/MPCAT/dbl.txt', 'dbl.txt')
except Exception as the_error:
  localtime = time.localtime(time.time())
  sys.stderr.write(strftime('%H:%M:%S - Problem downloading file: \n  http://www.minorplanetcenter.net/iau/ECS/MPCAT/dbl.txt\n  Error type: '+str(the_error)+'\n', localtime))
  sys.exit(1)

# numids.txt lists the numbered objects:
try:
  #urllib.request.urlretrieve('http://www.minorplanetcenter.net/iau/ECS/MPCAT/numids.txt', 'numids.txt')
  shutil.copyfile('iau/ECS/MPCAT/numids.txt', 'numids.txt')
except Exception as the_error:
  localtime = time.localtime(time.time())
  sys.stderr.write(strftime('%H:%M:%S - Problem downloading file: \n  http://www.minorplanetcenter.net/iau/ECS/MPCAT/numids.txt\n  Error type: '+str(the_error)+'\n', localtime))
  sys.exit(1)

ids_file = open('ids.txt', 'r')
dbl_file = open('dbl.txt', 'r')
numids_file = open('numids.txt', 'r')

# Make a dictionary combining all the ID files:
id_dic = {}
id_dic_packed = {}
for item in numids_file:
  item = item.rstrip()
  packed_key = item[:5]
  key = me.packed_to_unpacked_desig(item[:5]).lstrip('(').rstrip(')')
  dic_item_packed = [item[i:i+7] for i in range(6, len(item), 7)]
  dic_item_unpacked = []
  for i in dic_item_packed:
    if i != '       ':
      if i[0].isnumeric():
        dic_item_unpacked.append(i)
      else:
        unpacked = me.packed_to_unpacked_desig(i)
        dic_item_unpacked.append(unpacked)
  id_dic[key] = dic_item_unpacked
  id_dic_packed[packed_key] = dic_item_packed
for item in dbl_file:
  packed_key = item[:7]
  key = me.packed_to_unpacked_desig(item[:7])
  dic_item_packed = item[7:].rstrip().split()
  dic_item_unpacked = list(map(me.packed_to_unpacked_desig,dic_item_packed))
  id_dic[key] = dic_item_unpacked
  id_dic_packed[packed_key] = dic_item_packed
for item in ids_file:
  item = item.rstrip()
  if len(item) > 7: # leave out objects for which there is only a single designation
    packed_key = item[:7]
    key = me.packed_to_unpacked_desig(item[:7])
    dic_item_packed = [item[i:i+7] for i in range(6, len(item), 7)]
    dic_item_unpacked = list(map(me.packed_to_unpacked_desig,dic_item_packed))
    id_dic[key] = dic_item_unpacked
    id_dic_packed[packed_key] = dic_item_packed



# Create new ID JSON files:

with open('mpc_ids.json', 'w') as output_json_file:
  json.dump(id_dic, output_json_file, indent=0)

with open('mpc_ids.json', 'rb') as input_file:
  with gzip.open(args.directory+'mpc_ids.json.gz', 'wb', compresslevel=5) as output_file:
    shutil.copyfileobj(input_file, output_file)

with open('mpc_ids_packed.json', 'w') as output_json_file:
  json.dump(id_dic_packed, output_json_file, indent=0)

with open('mpc_ids_packed.json', 'rb') as input_file:
  with gzip.open(args.directory+'mpc_ids_packed.json.gz', 'wb', compresslevel=5) as output_file:
    shutil.copyfileobj(input_file, output_file)

os.remove('mpc_ids.json')
os.remove('mpc_ids_packed.json')
os.remove('numids.txt')
os.remove('ids.txt')
os.remove('dbl.txt')

os.chmod(args.directory+'mpc_ids.json.gz', 0o774)
os.chmod(args.directory+'mpc_ids_packed.json.gz', 0o774)

localtime = time.localtime(time.time())
#sys.stderr.write(strftime('%H:%M:%S - Program finished without known errors\n', localtime))
sys.stderr.close()
sys.stderr = sys.__stderr__

