#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
from itertools import islice
import os
import mpc_essentials as me
from subprocess import call

# Set this variable so appropriate number of characters are removed when removing newline characters.
# The value should be 2 for Windows and 1 for Linux and OS:
remove_chars = len(os.linesep)

urllib.request.urlretrieve ('http://www.minorplanetcenter.net/iau/MPCORB/MPCORB.DAT', 'mpcorb.dat')
urllib.request.urlretrieve ('http://www.minorplanetcenter.net/iau/ECS/MPCAT/ids.txt', 'ids.txt')
urllib.request.urlretrieve ('http://www.minorplanetcenter.net/iau/ECS/MPCAT/dbl.txt', 'dbl.txt')
urllib.request.urlretrieve ('http://www.minorplanetcenter.net/iau/ECS/MPCAT/numids.txt', 'numids.txt')


num_header_lines = 41

ids_file = open('ids.txt', 'r')
dbl_file = open('dbl.txt', 'r')
numids_file = open('numids.txt', 'r')

numids = numids_file.readlines()
ids = ids_file.readlines()
# Deal with the dbl file having a different format to numids and ids files:
dbl_in = dbl_file.readlines()
dbl=[]
for item in dbl_in:
  dbl.append(item.replace(" ", ""))
ids = ids + dbl

output_file = open('mpcorb_extended.dat', 'w')         
with open('mpcorb.dat', 'r') as data_file:
  head = list(islice(data_file, num_header_lines))
  for item in head:
    output_file.write(item)
  for line in data_file:
    if line[:2] == '\n':
      output_file.write('\n')
    else:
      p_desig = line[:7]
      epoch = line[20:25]
      epoch = me.convert_packed_date_to_jd(epoch)
      M = float(line[26:35])
      n = float(line[81:90])
# Calculate Time of Periastron
      if M >= 180.0:
        Tp = epoch + (360.0-M)/n
      else:
        Tp = epoch - M/n
      if len(p_desig.strip()) == 5:
        discovery_flag = 0
        #for line2 in numids:
        for count, line2 in enumerate(numids):
          #print(item)
          if line2[:6] == p_desig[:6]:
            discovery_flag = 1
            line2 = line2[6:]
            if line2[0] == ' ':
              line20 = ''
              line2 = line2[7:].rstrip()
            elif line2[0].isnumeric():
              line20 = "{0:11s}".format(line2[0:7])
              line2 = line2[7:].rstrip()
            else:
              line20 = ''
              line2 = line2.rstrip()
            line2 = [line2[i:i+7] for i in range(0, len(line2), 7)]
            line3 = []
            for d in line2:
              unpacked = me.packed_to_unpacked_desig(d)
              line3.append("{0:10s}".format(unpacked))
            output_file.write(line.rstrip()+' '+"{0:13.5f}".format(Tp)+' '+line20+" ".join(line3)+'\n')
            del numids[count]
            break
        if discovery_flag == 0:
          output_file.write(line.rstrip()+' '+"{0:13.5f}".format(Tp)+'\n')
      else:
        discovery_flag = 0
        for count, line2 in enumerate(ids):
          if line2[:7] == p_desig:
            discovery_flag = 1
            line2 = line2[7:].rstrip()
            line2 = [line2[i:i+7] for i in range(0, len(line2), 7)]
            line3 = []
            for d in line2:
              unpacked = me.packed_to_unpacked_desig(d)
              line3.append("{0:10s}".format(unpacked))
            output_file.write(line.rstrip()+' '+"{0:13.5f}".format(Tp)+' '+" ".join(line3)+'\n')
            del ids[count]
            break
        if discovery_flag == 0:
          output_file.write(line.rstrip()+' '+"{0:13.5f}".format(Tp)+'\n')
output_file.close()

