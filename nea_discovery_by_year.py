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
counts_dict_pha = {}
counts_dict_bins = {}

# Initialise the dictionary of dictionaries that will contain the counts for each ObsCode and each year:
for i in surveys:
  counts_dict[i]={}
  counts_dict_140m[i]={}
  counts_dict_1km[i]={}
  counts_dict_pha[i] = {}
  for y in years:
    counts_dict[i].update({y:0})
    counts_dict_140m[i].update({y:0})
    counts_dict_1km[i].update({y:0})
    counts_dict_pha[i].update({y:0})

# Initialise the dictionary of dictionaries that will contain the counts for each size range and each year:
for i in magnitudes:
  counts_dict_bins[i]={}
  for y in years:
    counts_dict_bins[i].update({y:0})


for i in NEAs:
  found_flag = 0
  for j in surveys:
    if (j in i['obs_code']):
      found_flag = 1
      for y in years:
        if y == i['disc_date'][:4]:
          counts_dict[j][y] = counts_dict[j][y] + 1
          if float(i['h']) <= 22.0:
            counts_dict_140m[j][y] = counts_dict_140m[j][y] + 1
            if float(i['emoid']) <= 0.05:
              counts_dict_pha[j][y] = counts_dict_pha[j][y] + 1
            if float(i['h']) <= 17.75:
              counts_dict_1km[j][y] = counts_dict_1km[j][y] + 1
  if found_flag == 0:
    for y in years:
      if y == i['disc_date'][:4]:
        counts_dict['other'][y] = counts_dict['other'][y] + 1
        if float(i['h']) <= 22.0:
          counts_dict_140m['other'][y] = counts_dict_140m['other'][y] + 1
          if float(i['emoid']) <= 0.05:
            counts_dict_pha['other'][y] = counts_dict_pha['other'][y] + 1
          if float(i['h']) <= 17.75:
            counts_dict_1km['other'][y] = counts_dict_1km['other'][y] + 1

# Get the discoveries by magnitude bin:

for i in NEAs:
  if (i['disc_date'][:4] >= min(years) and i['disc_date'][:4] <= max(years)):
    if float(i['h']) <= magnitudes['bin_1'][0]:
      counts_dict_bins['bin_1'][i['disc_date'][:4]] = counts_dict_bins['bin_1'][i['disc_date'][:4]] + 1
    elif (float(i['h']) > magnitudes['bin_1'][0] and float(i['h']) <= magnitudes['bin_2'][0]):
      counts_dict_bins['bin_2'][i['disc_date'][:4]] = counts_dict_bins['bin_2'][i['disc_date'][:4]] + 1
    elif (float(i['h']) > magnitudes['bin_2'][0] and float(i['h']) <= magnitudes['bin_3'][0]):
      counts_dict_bins['bin_3'][i['disc_date'][:4]] = counts_dict_bins['bin_3'][i['disc_date'][:4]] + 1
    elif float(i['h']) > magnitudes['bin_3'][0]:
      counts_dict_bins['bin_4'][i['disc_date'][:4]] = counts_dict_bins['bin_4'][i['disc_date'][:4]] + 1

import pprint
pp = pprint.PrettyPrinter(indent=4)

with open('nea_disc_by_year_obscode.csv', 'w') as out_file:
  out_file.write('Categories,'+(','.join(map(str,years)))+'\n')
  for oc in plot_order:
    count_list = []
    for y in years:
      count_list.append(str(counts_dict[oc][y]))
    out_file.write(surveys[oc]+','+(','.join(map(str,count_list)))+'\n')
  out_file.truncate(out_file.tell() - remove_chars)
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

with open('nea_140m_disc_by_year_obscode.csv', 'w') as out_file:
  out_file.write('Categories,'+(','.join(map(str,years)))+'\n')
  for oc in plot_order:
    count_list = []
    for y in years:
      count_list.append(str(counts_dict_140m[oc][y]))
    out_file.write(surveys[oc]+','+(','.join(map(str,count_list)))+'\n')
  out_file.truncate(out_file.tell() - remove_chars) # Remove the linebreak from the last line so Highcharts doesn't barf
out_file.close()

with open('nea_1km_disc_by_year_obscode.csv', 'w') as out_file:
  out_file.write('Categories,'+(','.join(map(str,years)))+'\n')
  for oc in plot_order:
    count_list = []
    for y in years:
      count_list.append(str(counts_dict_1km[oc][y]))
    out_file.write(surveys[oc]+','+(','.join(map(str,count_list)))+'\n')
  out_file.truncate(out_file.tell() - remove_chars) # Remove the linebreak from the last line so Highcharts doesn't barf
out_file.close()

# Uncomment to print CSV to terminal:
#print('Categories', end="")
#for y in years:
  #print(','+y, end="")
#print('')
#for oc in plot_order:
  #print(surveys[oc], end="")
  #for y in years:
    #print(','+str(counts_dict_1km[oc][y]), end="")
  #print('')

with open('nea_pha_disc_by_year_obscode.csv', 'w') as out_file:
  out_file.write('Categories,'+(','.join(map(str,years)))+'\n')
  for oc in plot_order:
    count_list = []
    for y in years:
      count_list.append(str(counts_dict_pha[oc][y]))
    out_file.write(surveys[oc]+','+(','.join(map(str,count_list)))+'\n')
  out_file.truncate(out_file.tell() - remove_chars) # Remove the linebreak from the last line so Highcharts doesn't barf
out_file.close()

with open('nea_size_bin_disc_by_year_obscode.csv', 'w') as out_file:
  out_file.write('Categories,'+(','.join(map(str,years)))+'\n')
  for bin in plot_order_bins:
    count_list = []
    for y in years:
      count_list.append(str(counts_dict_bins[bin][y]))
    out_file.write(magnitudes[bin][1]+','+(','.join(map(str,count_list)))+'\n')
  out_file.truncate(out_file.tell() - remove_chars) # Remove the linebreak from the last line so Highcharts doesn't barf
out_file.close()


# Uncomment to print CSV to terminal:
#print('Categories', end="")
#for y in years:
  #print(','+y, end="")
#print('')
#for bin in plot_order_bins:
  #print(magnitudes[bin][1], end="")
  #for y in years:
    #print(','+str(counts_dict_bins[bin][y]), end="")
  #print('')


