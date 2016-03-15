#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import os
import json
import re

# Set this variable so appropriate number of characters are removed when taking care of the newline issue for the CSV
# file. The value should be 2 for Windows and 1 for Linux and OS:
remove_chars = len(os.linesep)

surveys_all = {'G45':'SST','W84':'DECam','C51':'WISE','F51':'Pan-STARRS','F52':'Pan-STARRS','566':'NEAT','644':'NEAT','699':'LONEOS','691':'Spacewatch','291':'Spacewatch','E12':'Siding Spring','703':'Catalina','G96':'Mt. Lemmon','704':'LINEAR','T05':'ATLAS','T08':'ATLAS'}
# The surveys to be used for the plot:
surveys = {'G45':'SST','W84':'DECam','C51':'WISE','F51':'Pan-STARRS','566':'NEAT','699':'LONEOS','691':'Spacewatch','E12':'Siding Spring','703':'Catalina','G96':'Mt. Lemmon','704':'LINEAR','other':'Other'}

magnitudes = {'bin_1':[17.75,'> 1km'],'bin_2':[20.0,'350m - 1km'],'bin_3':[22.0,'140m - 350m'],'bin_4':[22.0,'< 140m']}

# Instead of using an ordered dictionary to establish the plotting order, I'm creating a
# list to establish that order. This should make it simpler to change the order in the future,
# or when adding new surveys to the plot. The order of the list is how surveys will be plotted
# from top to bottom. I would recommend always keeping 'Other' as the top-most plotted bar.
plot_order = ['other','C51','W84','699','F51','566','691','E12','703','G96','704','G45']
plot_order_bins = ['bin_4','bin_3','bin_2','bin_1']

group_names = ['atiras','atens','apollos','amors']
for i in group_names:
  urllib.request.urlretrieve ('http://minorplanetcenter.net/unusual/'+i+'.json', i+'.json')
  data_file = open(i+'.json', 'r')
  if (i == 'atiras'):
    atiras = json.load(data_file)
  elif (i == 'atens'):
    atens = json.load(data_file)
  elif (i == 'apollos'):
    apollos = json.load(data_file)
  elif (i == 'amors'):
    amors = json.load(data_file)
  data_file.close()
  
NEAs = atiras+atens+apollos+amors

# Replace some keys for the ObsCodes of surveys with more than one telescope
# that you want to group together; namely: Pan-STARRS, NEAT and Spacewatch:

for i in NEAs:
  if i['obs_code'] == 'F52': # Pan-STARRS
    i['obs_code'] = 'F51'
  elif i['obs_code'] == '644': # NEAT
    i['obs_code'] = '566'
  elif i['obs_code'] == '291': # Spacewatch
    i['obs_code'] = '691'
  elif i['obs_code'] == 'T08': # ATLAS
    i['obs_code'] = 'T05'

years = list(map(str, list(range(1985, 2016))))
counts_dict = {}
counts_dict_140m = {}
counts_dict_1km = {}
counts_dict_bins = {}

a = []
e = []
i = []
H = []
MOID = []

for j in NEAs:
  a.append(j['a'])
  e.append(j['e'])
  i.append(j['i'])
  H.append(j['h'])
  MOID.append(j['emoid'])


with open('nea_e_vs_a.csv', 'w') as out_file:
  out_file.write('a,e\n')
  for j,k in zip(a,e):
    out_file.write(str(j)+','+str(k)+'\n')
out_file.close()

with open('nea_e_vs_a_2.csv', 'w') as out_file:
  out_file.write('[')
  for j,k in zip(a,e):
    out_file.write('['+str(j)+','+str(k)+'],')
  out_file.write(']')
out_file.close()

# Uncomment to print CSV to terminal:
# print('Categories', end="")
# for y in years:
#   print(','+y, end="")
# print('')
# for oc in plot_order:
#   print(surveys[oc], end="")
#   for y in years:
#     print(','+str(counts_dict[oc][y]), end="")
#   print('')

