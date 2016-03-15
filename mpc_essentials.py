#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Some useful routines from mpc_convert.py, mpc_lib.py and mpc_astro.py"""

import os
import re
import string
import itertools
import argparse


# Constants


PI = 3.1415926535897932384626433
TWO_PI = 6.2831853071795864769252866
HALF_PI = 1.5707963267948966192313216

DEG2RAD = 1.745329251994329576923691e-2
"""Multiplicative factor to convert from degrees to radians."""

RAD2DEG = 57.29577951308232087679815
"""Multiplicative factor to convert from radians to degrees"""

ONE_TWENTYFOURTH = 4.166666666666666666666667E-02
"""An hour as a decimal fraction of a day."""

ONE_SIXTIETH = 1.666666666666666666666667E-02
"""A minute as a deciaml fraction of an hour."""

ONE_THIRTY_SIX_HUNDRETH = 2.777777777777777777777778E-04
"""A second as a decimal fraction of an hour."""

VALID_CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
"""Valid Base62 characters"""

HI_BIT_SET_CHARS = "".join(map(chr,range(128,255)))



def convert_packed_date_to_jd(pdate):
  """Convert a 5- or 12-character packed date into a JD

  Parameters
  ----------
  pdate : str
    A 5- or 12-character packed date

  Returns
  -------
  jd : float
    The JD corresponding to the packed date.

  Note
  ----
  Works with all packed dates after the year -1500.
  If the length of the passed string is not 5 or 12, JD = 0 is returned.
  The old packed_date had two representations for dates in the year 0: "/00CV" and "000CV" both represent Dec. 31 in the year 0.
  For dates before 0, the characters "-", "." and "/" represent the years -200, -100 and 0, respectively.  And (year MOD 100) has
  be subtracted from those values.

  Examples
  --------
  >>> convert_packed_date_to_jd("K156R")
  2457200.5
  >>> convert_packed_date_to_jd("-395P1179600")
  1633907.61796

  """

  jd = 0.0
  l = len(pdate)
  d_frac = 0.0

  if l in [ 5, 12 ]:
    if pdate[0] >= "0":
      y = base62_to_int(pdate[0]) * 100 + int(pdate[1:3])

    else:
      y = (ord(pdate[0]) - 47) * 100 - int(pdate[1:3])

    m = base62_to_int(pdate[3])
    d = base62_to_int(pdate[4])

    if l == 12:
      d_frac = int(pdate[5:]) / 10000000.0

    d += d_frac
    jd = to_julian_date(y,m,d)

  return jd



def convert_packed_prov_desig(desig):
  """Convert a packed mp/cmt/sat provisional designation from old style to new style.

  Parameters
  ----------
  desig : str
    The old format packed designation string.  Mp designations should be the full 7 chars.
    Cmt and sat designations can either be 7 or the full 8 chars.
 
  Returns
  -------
  new_desig : str
    The new format packed designation string.

  Examples
  --------
  >>> convert_packed_prov_desig('K00A00A')
  'K00A00000A'
  >>> convert_packed_prov_desig('K00A01A')
  'K00A00001A'
  >>> convert_packed_prov_desig('K00A10A')
  'K00A00010A'
  >>> convert_packed_prov_desig('K00AA0A')
  'K00A00100A'
  >>> convert_packed_prov_desig('K00Aa5A')
  'K00A00365A'
  >>> convert_packed_prov_desig('K00A010')
  'K00A000010'
  >>> convert_packed_prov_desig('PK00A010')
  'PK00A000010'
  """

  new_desig = ""
  len_desig = len(desig)

  if ((desig[0] >= "P") and (len_desig == 7)):              # First catch mp survey designations
    new_desig = desig[0:3] + "000" + desig[3:] 


  else:                                                     # Deal with mp non-survey and non-mp designations
    if (desig[-1] >= "a"):           # Replace fragment ID with "0", there are no two-char fragment IDs among the provisional designations
      desig = desig[:-1] + "0"
 
    ptr = 4                         
    if (len(desig) == 8):
      ptr = 5

    new_desig = desig[0:ptr] + "000" + desig[ptr:]

    if desig[ptr] > "9":
      sequence_num = 10 * decode_base_62(desig[ptr]) + int(desig[ptr+1])
      t5 = str(sequence_num).zfill(5)
      new_desig = new_desig[0:ptr] + t5 + new_desig[ptr+5:]

  return new_desig


def convert_packed_perm_desig(desig):
  """"Convert a packed mp/cmt/sat permanent designation from old style to new style.

  Parameters
  ----------
  desig : str
    The old format packed designation string.  All old-style permanent designations
    are 5 chars.
 
  Returns
  -------
  new_desig : str
    The new format packed designation string.

  Examples
  --------

  """

  new_desig = ""
  if (len(desig) == 5):

    if desig[0] in [ 'J', 'S', 'U', 'N' ]:
      new_desig = desig[0] + "0000" + desig[1:]

    else:
      if desig[0] in VALID_CHARS[10:]:    # Is mp designation > 99999
        i = VALID_CHARS.find(desig[0])
        new_desig = "000" + str(i) + desig[1:]

      else:
        new_desig = "0000" + desig

  return new_desig



def packed_to_unpacked_desig(desig):
  """Convert old-style packed designation to unpacked designation

  Convert old-style packed provisional or permanent designation to unpacked designation

  Parameters
  ----------
  desig : str
    A packed provisional or permanent designation for a minor planet,
    comet or nat sat

  Returns
  -------
  A string containing the unpacked designation corresponding to the
  given packed provdes/permdes.
  If the offered designation is not valid, an empty string is returned.
    
  """

  new_desig = ""
  t10 = ""
  t10a = ""

  l = len(desig)

  if l == 5:
    tags = [ ('J', 'Jupiter'), ('S', 'Saturn'), ('U', 'Uranus'), ('N', 'Neptune') ]
    for tag in tags:
      if tag[0] in desig[0]:
        new_desig = tag[1] + " " + to_roman(int(desig[1:4]))

    if new_desig == "":
      if desig[4] in [ 'P', 'D' ]:
        new_desig = str(int(desig[0:4])) + desig[4]

      else:
        if desig[0] >= "A":
          new_desig = "(" + str(base62_to_int(desig[0])) + desig[1:5] + ")"
        else:
          new_desig = "(" + str(int(desig)) + ")"

  else:
    if l == 7:
      t10 = desig

    elif l == 8:
      if desig[0] in ['P', 'C', 'D']:
        new_desig = desig[0] + "/"
        t10 = desig[1:]

      elif desig[0] == "S":
        new_desig = desig[0] + "/"
        t10 = desig[1:]

    #print("t10 = ", t10)
    if t10 != "":
      tags = [ ("PLS", "P-L"), ("T1S", "T-1"), ("T2S", "T-2"), ("T3S", "T-3") ]

      for tag in tags:            # Deal with survey designations
        if tag[0] in t10[:3]:
          t10a = str(int(t10[3:])) + " " + tag[1]

      if t10a == "":              # Deal with non-survey designations
        t10a = str(base62_to_int(t10[0])) + t10[1:3]+ " " + t10[3]
        if new_desig == "" and t10[0:3] < "J25":
          t10a = "A" + t10a[1:]

        if t10[-1] != "0": t10a += t10[-1]

        if t10[4:6] != "00":
          if t10[4:6] <= "99":
            t10a += str(int(t10[4:-1]))
          else:
            t10a += str(int(base62_to_int(t10[4]))) + t10[5]
            
      new_desig += t10a

  return new_desig
  
  

def base62_to_int(string_value):
  """Convert a base62-string into an integer

  Convert a base62-string into an integer.

  Parameters
  ----------
  string_value : string.
    A valid base-62 string of any length.

  Returns
  -------
  The integer value corresponding to the base62 representation.

  Notes
  -----
  A blank base-62 string returns 0.
  An invalid base-62 string (containing invalid character or that
  overflows the integer) returns -1.

  Examples
  --------
  >>> base62_to_int('y0g6Y')
  886742014
  >>> base62_to_int('')
  0
  >>> base62_to_int('l:0')
  -1

  """

  int_value = 0
  try:

    if string_value != "":
      l = len(string_value)

      for j in range(0, l):
        c = string_value[j]
        i = VALID_CHARS.index(c)

        if i > -1:
          int_value = int_value * 62 + i

  except Exception as e:
    int_value = -1

  return int_value


def decode_base_62(base_62_string):
  """Decode a base 62 string into its numeric value.

  Parameters
  ----------
  base_62_string : The base 62 string to decode

  Returns
  -------
  int
    The integer value of the string.

  Examples
  --------
  >>> decode_base_62('0')
  0
  >>> decode_base_62('A')
  10
  >>> decode_base_62('Z')
  35
  >>> decode_base_62("a")
  36
  >>> decode_base_62("z")
  61
  >>> decode_base_62("17")
  69
  >>> decode_base_62("A0")
  620
  """
  BASE_62_CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
  BASE_62_DICT = dict((c, v) for v, c in enumerate(BASE_62_CHARS))
  num = 0
  for char in base_62_string:
    num = num * 62 + BASE_62_DICT[char]
  return num


def to_roman(i):
  """Convert integer to Roman numerals

  Convert integer in range 1-3999 into the equivalent Roman numeral.

  Parameters
  ----------
  i : integer
    Integer value to be converted

  Returns
  -------
  Roman numeral corresponding to i : str

  Notes
  -----
  Returns null string if i < 1 or i > 3999.

  """

  values = []
  values.append([ '', 'M', 'MM', 'MMM' ])
  values.append([ '', 'C', 'CC', 'CCC', 'CD', 'D', 'DC', 'DCC', 'DCCC', 'CM' ])
  values.append([ '', 'X', 'XX', 'XXX', 'XL', 'L', 'LX', 'LXX', 'LXXX', 'XC' ])
  values.append([ '', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX' ])

  roman = ""

  if i > 0 and i < 4000:
    t4 = "{0:04d}".format(i)
    for j in range(0,4):
      k = int(t4[j])
      roman += values[j][k]

  return roman


def to_julian_date(year, month, day):
  """Generate Julian Date

  Convert year,month,day to Julian Date

  Parameters
  ----------
  year : integer
    Calendar year.
  month : integer
    Calendar month.
  day : float
    Calender day and decimal of day.

  Returns
  -------
  A float containing the equivalent Julian Date.

  Notes
  -----
  Algorithm for Astronomical Algorithms (Meeus) p. 60-61.
  Works for negative years, but not negative JDs.

  >>> to_julian_date(1957,10,4.81)
  2436116.31
  >>> to_julian_date(333,1,27.5)
  1842713.0
  >>> to_julian_date(-4712,1,1.5)
  0.0
  >>> to_julian_date(-1001,8,17.9)
  1355671.4
  >>> to_julian_date(2000,1,1.5)  
  2451545.0
  >>> to_julian_date(1582,10,4.9)
  2299160.4
  >>> to_julian_date(1582,10,15.0)
  2299160.5

  """

  y = year
  m = month
  if m < 3:
    y = y -1
    m = m + 12
  yr = year * 10000.0 + m * 100.0 + day
  if (yr < 15821015.0):
    b = 0
  else:
    a = int(y / 100.0)
    b = 2 - a + int(a / 4)

  jd = int(365.25 * (y + 4716)) + int(30.6001 * (m + 1)) + day + b - 1524.5

  return jd



