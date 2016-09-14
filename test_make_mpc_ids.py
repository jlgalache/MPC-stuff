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

unpacked_file = open('mpc_ids.json', 'r')
packed_file = open('mpc_ids_packed.json', 'r')

unpacked = json.load(unpacked_file)
packed = json.load(packed_file)

print(' unpacked length is '+str(len(unpacked)))
print(' packed length is '+str(len(packed)))

with open('test_make_mpc_ids.txt', 'w') as output_file:    
  for keyp in packed:
    if me.packed_to_unpacked_desig(keyp).lstrip('(').rstrip(')') in unpacked:
      output_file.write(keyp+'   '+me.packed_to_unpacked_desig(keyp)+'\n')
    
output_file.close()
