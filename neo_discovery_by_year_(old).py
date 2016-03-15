#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import os
import json

surveys = {'G45':'SST','W84':'DECam','C51':'WISE','F51':'Pan-STARRS','566':'NEAT','699':'LONEOS','691':'Spacewatch','E12':'Siding Spring','703':'Catalina','G96':'Mt. Lemmon','704':'LINEAR','other':'Other'}
surveys_all = {'G45':'SST','W84':'DECam','C51':'WISE','F51':'Pan-STARRS','F52':'Pan-STARRS','566':'NEAT','644':'NEAT','699':'LONEOS','691':'Spacewatch','291':'Spacewatch','E12':'Siding Spring','703':'Catalina','G96':'Mt. Lemmon','704':'LINEAR'}


group_names = ['atens','apollos','amors']
for i in group_names:
  urllib.request.urlretrieve ('http://minorplanetcenter.net/unusual/'+i+'.json', i+'.json')
  data_file = open(i+'.json', 'r')
  if (i == 'atens'):
    atens = json.load(data_file)
  elif (i == 'apollos'):
    apollos = json.load(data_file)
  elif (i == 'amors'):
    amors = json.load(data_file)
  data_file.close()
  
NEOs = atens+apollos+amors

# Replace some keys for the ObsCodes of surveys with more than one telescope
# that I want to group together; namely: Pan-STARRS, NEAT and Spacewatch:

for i in NEOs:
  if i['obs_code'] == 'F52':
    i['obs_code'] = 'F51'
  elif i['obs_code'] == '644':
    i['obs_code'] = '566'
  elif i['obs_code'] == '291':
    i['obs_code'] = '691'


#urllib.request.urlretrieve ('http://minorplanetcenter.net/unusual/atens.json', 'atens.json')
#urllib.request.urlretrieve ('http://minorplanetcenter.net/unusual/apollos.json', 'apollos.json')
#urllib.request.urlretrieve ('http://minorplanetcenter.net/unusual/amors.json', 'amors.json')

#data_file = open('atens.json', 'r')
#atens = json.load(data_file)

#surveys = {'703':'CSS','W84':'DEcam'}  # For testing!
years=list(map(str, list(range(1985, 2016))))
counts_dict = {}
#for i in surveys:
  #counts_dict[i]={}
  #for y in years:
    #counts_dict[i].update({y:0})
  #for j in NEOs:
    #if i == 'other':
      #continue
    ##print(j['desig'])
    ##print(' ',j['disc_date'][:4])
    #if (i in j['obs_code']):
      #for y in years:
        #if y == j['disc_date'][:4]:
          ##print('  There is a match!')
          #counts_dict[i][y] = counts_dict[i][y] + 1

# Initialise the dictionary of dictionaries that will contain the counts for each ObsCode and each year:
for i in surveys:
  counts_dict[i]={}
  for y in years:
    counts_dict[i].update({y:0})

for i in NEOs:
  found_flag = 0
  for j in surveys:
    if (j in i['obs_code']):
      found_flag = 1
      for y in years:
        if y == i['disc_date'][:4]:
          #print('  There is a match!')
          counts_dict[j][y] = counts_dict[j][y] + 1
  if found_flag == 0:
    for y in years:
      if y == i['disc_date'][:4]:
        counts_dict['other'][y] = counts_dict['other'][y] + 1




#print(sum(counts_dict['703'].values))
#print(counts_dict['703'].values)

#counts_dict['other'][y] = counts_dict['other'][y] + 1

import pprint
pp = pprint.PrettyPrinter(indent=4)

#pp.pprint(counts_dict) 

print('Categories'+',', end="")
print(years)
for oc in counts_dict:
  print(surveys[oc], end="")
  for y in years:
    print(','+str(counts_dict[oc][y]), end="")
  #print(counts_dict[oc[sorted(years)]].values())
  print('')
#with open(NEA_disc_by_year_obscode.dat, 'w') as out_file:
  
  #for i in surveys:
    #neo_obscode_year = []
    #for j in NEOs:
      #if (i in j['obs_code']):
        #neo_obscode_year = neo_obscode_year + [x['disc_date'][:4]]
    #neo_obscode_year_count = Counter(neo_obscode_year)
    #output_line = [i]
    #for k in years:
      #output_line = output_line + neo_obscode_year_count[k]   
    #out_file.write(",".join(map(str,output_line))+'\n')
    
#out_file.close()

#neo_obscode_count = neo_obscode_count + [x['disc_date'][:4]]
