#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
import mpc_db

# Don't forget to add path to mpc_db:
# export PYTHONPATH=/home/mpc/mpcops/lib


root_filename = 'mpcorb_extended_dev'

# Open logfile and set starting time
sys.stderr = open(root_filename+'.log', 'a')
localtime = time.localtime(time.time())
sys.stderr.write(strftime('%Y/%m/%d\n  %H:%M:%S - Run started\n  ', localtime))

# Get MPCORB.DAT over the internet or locally from /base/public/iau/:
try:
#  urllib.request.urlretrieve ('http://www.minorplanetcenter.net/iau/MPCORB/MPCORB.DAT', 'mpcorb.dat')
#  shutil.copyfile('iau/MPCORB/MPCORB.DAT', 'mpcorb.dat')
  shutil.copyfile('mpcorb_test.dat', 'mpcorb.dat')
except Exception as the_error:
  localtime = time.localtime(time.time())
  sys.stderr.write(strftime('%H:%M:%S - Problem downloading file: \n  http://www.minorplanetcenter.net/iau/MPCORB/MPCORB.DAT\n  Error type: '+str(the_error)+'\n', localtime))
  sys.exit(1)

# Find length of header:
with open('mpcorb.dat', 'r') as data_file:
  c = 0
  for  line in data_file:
    c = c + 1
    if line[:2] == '--':
      num_header_lines = c
      break

try:
#  urllib.request.urlretrieve ('http://www.minorplanetcenter.net/iau/ECS/MPCAT/ids.txt', 'ids.txt')
  shutil.copyfile('iau/ECS/MPCAT/ids.txt', 'ids.txt')
except Exception as the_error:
  localtime = time.localtime(time.time())
  sys.stderr.write(strftime('%H:%M:%S - Problem downloading file: \n  http://www.minorplanetcenter.net/iau/ECS/MPCAT/ids.txt\n  Error type: '+str(the_error)+'\n', localtime))
  sys.exit(1)

try:
#  urllib.request.urlretrieve ('http://www.minorplanetcenter.net/iau/ECS/MPCAT/dbl.txt', 'dbl.txt')
  shutil.copyfile('iau/ECS/MPCAT/dbl.txt', 'dbl.txt')
except Exception as the_error:
  localtime = time.localtime(time.time())
  sys.stderr.write(strftime('%H:%M:%S - Problem downloading file: \n  http://www.minorplanetcenter.net/iau/ECS/MPCAT/dbl.txt\n  Error type: '+str(the_error)+'\n', localtime))
  sys.exit(1)

try:
#  urllib.request.urlretrieve ('http://www.minorplanetcenter.net/iau/ECS/MPCAT/numids.txt', 'numids.txt')
  shutil.copyfile('iau/ECS/MPCAT/numids.txt', 'numids.txt')
except Exception as the_error:
  localtime = time.localtime(time.time())
  sys.stderr.write(strftime('%H:%M:%S - Problem downloading file: \n  http://www.minorplanetcenter.net/iau/ECS/MPCAT/numids.txt\n  Error type: '+str(the_error)+'\n', localtime))
  sys.exit(1)


ids_file = open('ids.txt', 'r')
dbl_file = open('dbl.txt', 'r')
numids_file = open('numids.txt', 'r')

numids = numids_file.readlines()
ids = ids_file.readlines()
# Deal with the dbl file having a different format to numids and ids files, then combine it with ids:
dbl_in = dbl_file.readlines()
dbl=[]
for item in dbl_in:
  dbl.append(item.replace(" ", ""))
ids = ids + dbl

try:
  data_file = open('mpcorb.dat', 'rb')
except IOError:
  localtime = time.localtime(time.time())
  sys.stderr.write(strftime('%H:%M:%S - Problem opening file: \n  '+str(os.getcwd())+'/mpcorb.dat\n'), localtime)
  sys.exit(1)

output_file = open(root_filename+'.dat', 'w')         
with open('mpcorb.dat', 'r') as data_file:
  head = list(islice(data_file, num_header_lines))
  for item in head:
    output_file.write(item)
  for line in data_file:
    if not line.strip():
      output_file.write('\n')
    else:
      p_desig = line[:7] # Principal Designation
      epoch = line[20:25]
      epoch = me.convert_packed_date_to_jd(epoch)
      M = float(line[26:35])
      n = float(line[81:90])
# Calculate Time of Periastron:
      if M >= 180.0:
        Tp = epoch + (360.0-M)/n
      else:
        Tp = epoch - M/n
      if len(p_desig.strip()) == 5:
        discovery_flag = 0
        for count, line2 in enumerate(numids):
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

output_json_file = open(root_filename+'.json', 'w')
output_json = []

cnx = mpc_db.connect_to_mpc_development()


with open(root_filename+'.dat', 'r') as data_file:
  head = list(islice(data_file, num_header_lines))
  for line in data_file:
    line_dict = {}
    if line.strip():
      p_desig = line[:7].strip()
      if len(p_desig) == 5:
        number = me.packed_to_unpacked_desig(p_desig)
        name = line[175:193].rstrip()
        desig = line[217:227].rstrip()
        if name[:2].isnumeric():
          desig = name
          name = ''
      else:
        number = ''
        name = ''
        desig = line[175:193].rstrip()
      other_desig = line[228:449].rstrip()
      other_desig = [other_desig[i:i+11] for i in range(0, len(other_desig), 11)]
      other_desig = [x.strip() for x in other_desig]
      epoch = me.convert_packed_date_to_jd(line[20:25])
      a = float(line[92:103].strip())
      e = float(line[70:79].strip())
      q_small = a*(1.0 - e)
      Q_big = a*(1.0 + e)
      semilatus = (a/2.0)*(1.0 - e**2.0)
      period = math.sqrt(a**3.0)
      synodic = 1.0/(abs((1.0)-(1.0/period)))
      last_obs = line[194:198]+'-'+line[198:200]+'-'+line[200:202]
      hex_flags = line[161:165].strip()
      if hex_flags[3] == '0':
        orbit_type = 'MBA'
      elif hex_flags[3] == '1':
        orbit_type = 'Atira'
      elif hex_flags[3] == '2':
        orbit_type = 'Aten'
      elif hex_flags[3] == '3':
        orbit_type = 'Apollo'
      elif hex_flags[3] == '4':
        orbit_type = 'Amor'
      elif hex_flags[3] == '5':
        orbit_type = 'Object with perihelion distance < 1.665 AU'
      elif hex_flags[3] == '6':
        orbit_type = 'Hungaria'
      elif hex_flags[3] == '7':
        orbit_type = 'Phocaea'
      elif hex_flags[3] == '8':
        orbit_type = 'Hilda'
      elif hex_flags[3] == '9':
        orbit_type = 'Jupiter Trojan'
      elif hex_flags[3] == 'A':
        orbit_type = 'Distant Object'
      else:
        sys.stderr.write('  Unknown orbit type, '+hex_flags[3]+' for object: '+desig+'\n')
        sys.stderr.close()
        break
        
      if int(hex_flags[1],16) == (8 or 9 or 10 or 12):
        line_dict['NEO_flag'] = 1

      if int(hex_flags[0],16) == 1:
        line_dict['One_km_NEO_flag'] = 1
      elif int(hex_flags[0],16) == 2:
        line_dict['One_opposition_object_flag'] = 1
      elif int(hex_flags[0],16) == 3:
        line_dict['One_km_NEO_flag'] = 1
        line_dict['One_opposition_object_flag'] = 1
      elif int(hex_flags[0],16) == 4:
        line_dict['Critical_list_numbered_object_flag'] = 1
      elif int(hex_flags[0],16) == 5:
        line_dict['One_km_NEO_flag'] = 1
        line_dict['Critical_list_numbered_object_flag'] = 1
      elif int(hex_flags[0],16) == 6:
        line_dict['One_opposition_object_flag'] = 1
        line_dict['Critical_list_numbered_object_flag'] = 1
      elif int(hex_flags[0],16) == 7:
        line_dict['One_km_NEO_flag'] = 1
        line_dict['One_opposition_object_flag'] = 1
        line_dict['Critical_list_numbered_object_flag'] = 1
      elif int(hex_flags[0],16) == 8:
        line_dict['PHA_flag'] = 1
      elif int(hex_flags[0],16) == 9:
        line_dict['One_km_NEO_flag'] = 1
        line_dict['PHA_flag'] = 1
      elif int(hex_flags[0],16) == 10:
        line_dict['One_opposition_object_flag'] = 1
        line_dict['PHA_flag'] = 1
      elif int(hex_flags[0],16) == 11:
        line_dict['One_km_NEO_flag'] = 1
        line_dict['One_opposition_object_flag'] = 1
        line_dict['PHA_flag'] = 1
      elif int(hex_flags[0],16) == 12:
        line_dict['Critical_list_numbered_object_flag'] = 1
        line_dict['PHA_flag'] = 1
      elif int(hex_flags[0],16) == 13:
        line_dict['One_km_NEO_flag'] = 1
        line_dict['Critical_list_numbered_object_flag'] = 1
        line_dict['PHA_flag'] = 1
      elif int(hex_flags[0],16) == 14:
        line_dict['One_opposition_object_flag'] = 1
        line_dict['Critical_list_numbered_object_flag'] = 1
        line_dict['PHA_flag'] = 1
      elif int(hex_flags[0],16) == 15:
        line_dict['One_km_NEO_flag'] = 1
        line_dict['One_opposition_object_flag'] = 1
        line_dict['Critical_list_numbered_object_flag'] = 1
        line_dict['PHA_flag'] = 1
      
      H = line[8:13].strip()
      if H != '':
        line_dict['H'] = float(H)
      G = line[14:19].strip()
      if G != '':
        line_dict['G'] = float(G)
      num_obs = line[117:122].strip()
      if num_obs != '':
        line_dict['Num_obs'] = int(num_obs)
      rms = line[137:141].strip()
      if rms != '':
        line_dict['rms'] = float(rms)
      U = line[105].strip()
      if U != '':
        line_dict['U'] = U
      arc = line[127:136]
      if 'days' in arc:
        line_dict['Arc_length'] = int(arc[:4].strip())
      else:
        line_dict['Arc_years'] = arc
      if number != '':
        line_dict['Number'] = number
      if name != '':
        line_dict['Name'] = name
      if other_desig != []:
        line_dict['Other_desigs'] = other_desig
        
      line_dict2 = {'Designation':desig,'Epoch':round(epoch,7),'M':float(line[26:35].strip()),'Peri':float(line[37:46].strip()),'Node':float(line[48:57].strip()),'i':float(line[59:68].strip()),'e':float(line[70:79].strip()),'n':float(line[80:91].strip()),'a':float(line[92:103].strip()),'Ref':line[107:116].strip(),'Num_opps':int(line[123:126].strip()),'Perturbers':line[142:145].strip(),'Perturbers_2':line[146:149].strip(),'Computer':line[150:160].strip(),'Hex_flags':hex_flags,'Last_obs':last_obs,'Tp':float(line[203:216].strip()),'Orbital_period':round(period,7),'Perihelion_dist':round(q_small,7),'Aphelion_dist':round(Q_big,7),'Semilatus_rectum':round(semilatus,7),'Synodic_period':round(synodic,7)}  
      
      line_dict.update(line_dict2)
      output_json.append(line_dict)


json.dump(output_json, output_json_file, indent=0)
output_json_file.close()

with open(root_filename+'.dat', 'rb') as input_file:
  with gzip.open(root_filename+'.dat.gz', 'wb') as output_file:
    shutil.copyfileobj(input_file, output_file)

with open(root_filename+'.json', 'rb') as input_file:
  with gzip.open(root_filename+'.json.gz', 'wb') as output_file:
    shutil.copyfileobj(input_file, output_file)

os.remove('mpcorb.dat')
os.remove(root_filename+'.dat')
os.remove(root_filename+'.json')
os.remove('numids.txt')
os.remove('ids.txt')
os.remove('dbl.txt')

localtime = time.localtime(time.time())
sys.stderr.write(strftime('%H:%M:%S - Program finished without known errors\n', localtime))
sys.stderr.close()
sys.stderr = sys.__stderr__



def fetch_disc_info(desig,cnx):
  query = "select original_record from observations where discovery_flag = '*' and designation = binary('{}') or number = '{}'".format(desig,desig)
  rows = mpc_db.mysql_execute_query(cnx, query)
  return(rows)
  
def fetch_desig_info(number,cnx):
  query = "select designation from numbered_mps where number = '{}'".format(number)
  rows = mpc_db.mysql_execute_query(cnx, query)
  return(rows)
