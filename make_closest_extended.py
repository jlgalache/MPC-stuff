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
#sys.stderr.write(strftime('%Y/%m/%d\n  %H:%M:%S - Run started (file: Closest.txt)\n  ', localtime))

# Get the file with the closest recorded flybys of asteroids:
try:
  #urllib.request.urlretrieve('http://www.minorplanetcenter.net/iau/lists/Closest.html', 'Closest.txt')
  shutil.copyfile('iau/lists/Closest.html', 'Closest.txt')
except Exception as the_error:
  localtime = time.localtime(time.time())
  sys.stderr.write(strftime('%H:%M:%S - Problem downloading file: \n  http://www.minorplanetcenter.net/iau/lists/Closest.html\n  Error type: '+str(the_error)+'\n', localtime))
  sys.exit(1)


# Find length of header:
num_header_lines = 0
with open('Closest.txt', 'r') as data_file:
  c = 0
  for  line in data_file:
    c = c + 1
    if line.strip() == '<pre>':
      for line in data_file:
        c = c + 1
        if line.strip() == '':
          num_header_lines = c
          break

closest_list = []
with open('Closest.txt', 'r') as data_file:
  head = list(islice(data_file, num_header_lines))
  for line in data_file:
    if line.strip() == '':
      break
    line_dic = {}
    if '!'in line[0:9]:
      line_dic['Impact_flag'] = 1
      line_dic['Distance_AU'] = float(line[0:9].rstrip('! '))
    elif '*'in line[0:9]:
      line_dic['Distance_AU'] = float(line[0:9].rstrip('* '))
    else:
      line_dic['Distance_AU'] = float(line[0:9].rstrip())
    line_dic['Distance_LD'] = round(line_dic['Distance_AU']*149597870.0/384400.0,4)
    line_dic['Distance_ER'] = round(line_dic['Distance_AU']*149597870.0/6387.0,2)
    line_dic['Distance_km'] = round(line_dic['Distance_AU']*149597870.0)
    if line[26:53].strip() != '':
      line_dic['Number'] = line[26:53].split()[0].strip('()')
      if len(line[26:53].split()) > 1:
        line_dic['Name'] = line[26:53].split(')')[1].strip()  # Doing it this way in case there are any multiword asteroid names
    line_dic['Provisional_desig'] = line[54:67].strip()
    if line[54:67].strip() == '1991 VG':
      line_dic['Note'] = '1991 VG may be a returning piece of man-made space debris.'
    elif line[54:67].strip() == '1988 TA':
      line_dic['Note'] = 'The ephemeris for 1988 TA on IAUC 4662 was very preliminary and should be disregarded.'
    line_dic['H'] = float(line[67:72].strip())
    ref = line[74:151].rstrip()
    if 'href' in ref:
      line_dic['Ref_URL'] = 'http://www.minorplanetcenter.net'+ref.split('\"')[1]
      if 'MPEC' in ref.split('\"')[2]:
        line_dic['Ref'] = 'MPEC '+ref.split('\"')[2].split('</i> ')[1].rstrip('</a>')
      elif 'IAUC' in ref.split('\"')[2]:
        line_dic['Ref'] = 'IAUC '+ref.split('\"')[2].split('</i> ')[1].rstrip('</a>')
    elif 'MPO' in ref:
      line_dic['Ref'] = 'MPO '+ref.split()[1]
    closest_list.append(line_dic)

with open('closest_extended.json', 'w') as output_json_file:
  json.dump(closest_list, output_json_file, indent=0)

with open('closest_extended.json', 'rb') as input_file:
  with gzip.open(args.directory+'closest_extended.json.gz', 'wb', compresslevel=5) as output_file:
    shutil.copyfileobj(input_file, output_file)

os.remove('Closest.txt')
os.remove('closest_extended.json')

os.chmod(args.directory+'closest_extended.json.gz', 0o774)

sys.stderr.close()
sys.stderr = sys.__stderr__



