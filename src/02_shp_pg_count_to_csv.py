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
# import sys
import time
# from sys import platform as _platform
# from time import strftime
from datetime import datetime
import csv

import cfg  # some global configurations

try:
    import shapefile
except Exception as e:
    print("Exception occurred " + str(e))
    print("try: pip install pyshp")

try:
    import psycopg2
except Exception as e:
    print("Exception occurred " + str(e))
    print("try: pip install psycopg2")


# Получаем кол-во объектов из шейп-файла
def shp_get_records_count(shp_file_in=''):
    file_dbf = shp_file_in.replace('.shp', '.dbf')
    print(file_dbf)
    if os.path.isfile(file_dbf):
        sf = shapefile.Reader(file_dbf)
        _count = len(sf.records())
        return _count
    else:
        return 0


# Получаем кол-во объектов из шейп-файла в выходной папке
def shp_out_get_records_count(shp_file_in=''):
    ff = shp_file_in.split(".")[0] + f"_" + str(cfg.DEFAULT_EPSG) + ".shp"
    file_out = str(os.path.join(cfg.FOLDER_OUT, ff.upper()))
    return shp_get_records_count(file_out)


# Получаем кол-во объектов в слое постгрес
def pg_get_records_count(shp_file_in=''):
    count = 0
    ff = shp_file_in.split(".")[0] + f"_" + str(cfg.DEFAULT_EPSG)
    table_name = ff.upper()
    print(table_name)
    db_conn = psycopg2.connect(host=cfg.DB_HOST, port=cfg.DB_PORT, dbname=cfg.DB_DATABASE, user=cfg.DB_USER, password=cfg.DB_PASSWORD)
    db_cursor = db_conn.cursor()
    s = f"SELECT COUNT(*) FROM {table_name}"
    # Error trapping
    try:
        # Execute the SQL
        db_cursor.execute(s)
        # Retrieve records from Postgres into a Python List
        counts = db_cursor.fetchall()
        count = counts[0][0]
    except psycopg2.Error as e:
        t_message = "Database error: " + e + "/n SQL: " + s
        return 0
    # Close the database cursor and connection
    db_cursor.close()
    db_conn.close()
    return count


def shp_pg_layers_get_count(dir_in='', dir_out=''):
    if len(str(dir_in)) == 0:
        dir_in = os.getcwd()
    if len(str(dir_out)) == 0:
        dir_out = os.getcwd()

    file_csv = str(os.path.join(dir_out, cfg.FILE_CSV))
    if os.path.isfile(file_csv):
        os.remove(file_csv)

    csv_dict = {'DATA': '',
                'FILENAME': '',
                'SHPIN': '',
                'SHPOUT': '',
                'PG': '',
                'DIFF': ''}

    for key in csv_dict:
        csv_dict[key] = ''

    with open(file_csv, 'w', newline='', encoding='utf-8') as csv_file:  # Just use 'w' mode in 3.x

        csv_file_open = csv.DictWriter(csv_file, csv_dict.keys(), delimiter=cfg.CSV_DELIMITER)
        csv_file_open.writeheader()
        for root, subdirs, files in os.walk(dir_in):
            for file in os.listdir(root):

                file_path = str(os.path.join(root, file)).lower()
                ext = '.'.join(file.split('.')[1:]).lower()
                if file_path.endswith('shp'):  # ext == "shp":
                    # print(file)
                    csv_dict['DATA'] = str(time.strftime("%Y-%m-%d"))
                    csv_dict['FILENAME'] = file_path
                    shp_in_count = shp_get_records_count(file_path)
                    shp_out_count = shp_out_get_records_count(file)
                    pg_count = pg_get_records_count(file)
                    diff = shp_out_count - pg_count

                    csv_dict['SHPIN'] = shp_in_count
                    csv_dict['SHPOUT'] = shp_out_count
                    csv_dict['PG'] = pg_count
                    csv_dict['DIFF'] = diff
                    csv_file_open.writerow(csv_dict)
                    # print(str(csv_dict.values()))

        csv_file.close()


def main():
    time1 = datetime.now()
    print('Starting at :' + str(time1))

    # dir_clear(dir_shp_out)
    shp_pg_layers_get_count(cfg.FOLDER_IN, cfg.FOLDER_OUT)

    time2 = datetime.now()
    print('Finishing at :' + str(time2))
    print('Total time : ' + str(time2 - time1))
    print('DONE !!!!')


if __name__ == '__main__':
    main()
