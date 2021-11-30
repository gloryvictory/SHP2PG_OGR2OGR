# !/usr/bin/python3
# -*- coding: utf-8 -*-
#
#   Author          : Viacheslav Zamaraev
#   email           : zamaraev@gmail.com
#   Script Name     : 02_shp_pg_count_to_csv.py
#   Created         : 30th November 2021
#   Last Modified	: 30th November 2021
#   Version		    : 1.0
#   PIP             : pip install shapefile pyshp
#   RESULT          : csv file with columns: FILENAME;...
# Modifications	: 1.1 -
#               : 1.2 -
# Description   : This script will search some *.shp files in the given directory and makes CSV file with some information
# count features in shp and count in pg

import os  # Load the Library Module
import os.path
import sys
import time
from sys import platform as _platform
from time import strftime
from datetime import datetime
import csv

try:
    import shapefile
except Exception as e:
    print("Exception occurred " + str(e))
    print("try: pip install pyshp")



