#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#   Author          : Viacheslav Zamaraev
#   email           : zamaraev@gmail.com
#   Script Name     : 01_shp2pg.py
#   Created         : 21th Oktober 2019
#   Last Modified	: 21th Oktober 2019
#   Version		    : 1.0
#
# Modifications	: 1.1 -
#               : 1.2 -
#
# Description   : This script will search any *.shp files in the given directory by list (in file_list_shp.txt ) and convert to EPSG:SRID 4326 and load to postgresql+postgis
# converting by using this utility : ogr2ogr -t_srs EPSG:4326 input_4236.shp input.shp
#  ogr2ogr  -lco ENCODING=UTF-8  -skipfailures -s_srs "EPSG:7683" -t_srs "EPSG:4326"   -f "ESRI Shapefile"  C:\GIS\test\qwe.shp  C:\GIS\test\lu_plan.shp
# https://trac.osgeo.org/postgis/wiki/UsersWikiOGR
# https://gdal.org/drivers/vector/pg.html#configuration-options

# from sridentify import Sridentify
# from time import strftime   # Load just the strftime Module from Time
# import logging
# from sys import platform as _platform
import logging
import os  # Load the Library Module
import os.path
from datetime import datetime
import os
import cfg  # some global configurations
import subprocess

# program_ogr2ogr = "ogr2ogr"
# shp2pg_program = "shp2pg"
# program_shp2pgsql = 'shp2pgsql'

# def dir_clear(dir_out =''):
#     if len(str(dir_out)) == 0:
#         dir_out = os.getcwd()
#     filelist = [f for f in os.listdir(dir_out)]
#     for f in filelist:
#         os.remove(os.path.join(dir_out, f))


# os.environ['PROJ_LIB'] = 'C:\\Program Files\\PostgreSQL\\13\\share\\contrib\\postgis-3.1\\proj'

os.environ['PROJ_LIB'] ='C:\\Apps\\QGIS 3.20.3\\share\\proj'

os.environ['GDAL_DATA'] = 'C:\\Program Files\\PostgreSQL\\13\\gdal-data'
# GDAL_DATA=C:\Program Files\PostgreSQL\13\gdal-data
# PROJ_LIB=C:\Program Files\PostgreSQL\13\share\contrib\postgis-3.1\proj


for handler in logging.root.handlers[:]:  # Remove all handlers associated with the root logger object.
    logging.root.removeHandler(handler)
file_log = str(os.path.join(os.getcwd(), cfg.FILE_LOG))
logging.basicConfig(filename=file_log, format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG,
                    filemode='w')  #
logging.info(file_log)


def shp_to_4326(dir_in=''):
    if len(str(dir_in)) == 0:
        dir_in = os.getcwd()
    # if len(str(dir_out)) == 0:
    #     dir_out = os.getcwd()

    # r=root, d=directories, f = files
    for r, d, f in os.walk(dir_in):
        for file in f:
            file_in = str(os.path.join(r, file))
            # file_name = file_in.split('.')[0]
            # table_name = file.split('.')[0]
            ext = '.'.join(file.split('.')[1:]).lower()
            if ext == "shp":
                ff = file.split(".")[0] + f"_" + str(cfg.DEFAULT_EPSG) + ".shp"
                file_out = str(os.path.join(cfg.FOLDER_OUT, ff.upper()))
                # logging.info(f"{file_out}")
                cmd_line = f"{cfg.APP_OGR} -t_srs EPSG:{cfg.DEFAULT_EPSG} -overwrite -skipfailures -lco ENCODING={cfg.DEFAULT_LOCALE} {file_out} {file_in}"
                # os.system(cmd_line)
                logging.info(f"{cmd_line}")

                process = subprocess.Popen(cmd_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                # logging.error(process.stderr.read())
                stde = str(process.stderr.read().decode("utf-8"))
                # stdout, stderr = process.communicate()
                # stdout = [x for x in stdout.split("\n") if x != ""]
                stderr = set([x for x in stde.split("\r\n") if x != ""])
                for qq in stderr:
                    logging.error(f"{file_out} : {qq}")

                # "C:\Apps\QGIS 3.16\bin\ogr2ogr.exe" -t_srs  "EPSG:4326" -lco ENCODING=UTF-8  c:\gis\out\test.shp  c:\gis\test\лу\Lu_Plan.shp
                # ogr2ogr - overwrite - f "PostgreSQL" PG: "host=localhost dbname=mydb user=postgres password=xxxxx"  F:\xxx\test\quj.shp
                # os.system('ogr2ogr ' + '-overwrite ' + '-f ' + '"' + "PostgreSQL" + '"' + ' PG:' + '"' + "host=localhost user=postgres dbname=mydb password=xxxx" + '"' + ' ' + '"' + "F:\xxx\test\quj.shp" + '"')

                # cmd_line = program_shp2pgsql + ' -d -I -W ' + cfg.default_locale + srid_source + ' ' + file_in + ' \"' + schema + '\".\"' + table_name + "\"" + ' |psql ' + ' -h ' + cfg.host + ' -u ' + cfg.user +' -d ' + cfg.database_gis + ' -U ' + cfg.user
                print(cmd_line)


def shp_to_pg(dir_in=''):
    if len(str(dir_in)) == 0:
        dir_in = os.getcwd()

    for r, d, f in os.walk(dir_in): # r=root, d=directories, f = files
        for file in f:
            file_in = str(os.path.join(r, file))
            file_name = file_in.split('.')[0]
            table_name = file.split('.')[0]
            ext = '.'.join(file.split('.')[1:]).lower()
            if ext == "shp":
                ff = file.split(".")[0] + f"_" + str(cfg.DEFAULT_EPSG) + ".shp"
                file_out = str(os.path.join(cfg.FOLDER_OUT, ff.upper()))
                # logging.info(f"{file_out}")
                cmd_line = f"{cfg.APP_OGR} -overwrite -skipfailures  -f \"PostgreSQL\" PG:\"host={cfg.DB_HOST} user={cfg.DB_USER} dbname={cfg.DB_DATABASE} password={cfg.DB_PASSWORD}\"  -nln {table_name} {file_in}"
                # "c:\Apps\QGIS 3.20.3\bin\ogr2ogr.exe"  -overwrite -skipfailures -f "PostgreSQL" PG:"host=r48-vapp-geos01.zsniigg.local user=gisdata dbname=gisdata password=gisdata"  -nln LOV_ZS_4326 C:\GIS\out\LOV_ZS_4326.shp
                # os.system(cmd_line)
                logging.info(f"{cmd_line}")

                process = subprocess.Popen(cmd_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stde = str(process.stderr.read().decode("utf-8"))
                stderr = set([x for x in stde.split("\r\n") if x != ""])
                for qq in stderr:
                    logging.error(f"{file_in} : {qq}")

                # ogr2ogr - overwrite - f "PostgreSQL" PG: "host=localhost dbname=mydb user=postgres password=xxxxx"  F:\xxx\test\quj.shp
                # os.system('ogr2ogr ' + '-overwrite ' + '-f ' + '"' + "PostgreSQL" + '"' + ' PG:' + '"' + "host=localhost user=postgres dbname=mydb password=xxxx" + '"' + ' ' + '"' + "F:\xxx\test\quj.shp" + '"')
                # cmd_line = program_shp2pgsql + ' -d -I -W ' + cfg.default_locale + srid_source + ' ' + file_in + ' \"' + schema + '\".\"' + table_name + "\"" + ' |psql ' + ' -h ' + cfg.host + ' -u ' + cfg.user +' -d ' + cfg.database_gis + ' -U ' + cfg.user

                print(cmd_line)



def main():
    time1 = datetime.now()
    print('Starting at :' + str(time1))

    # dir_clear(dir_shp_out)
    shp_to_4326(cfg.FOLDER_IN)
    shp_to_pg(cfg.FOLDER_OUT)

    # os.system(program_ogr2ogr + " -t_srs EPSG:4326 " +  file_in +" "+ file_out)

    time2 = datetime.now()
    print('Finishing at :' + str(time2))
    print('Total time : ' + str(time2 - time1))
    print('DONE !!!!')


if __name__ == '__main__':
    main()

# # Prj file exist
# file_prj = file_name + '.prj'
# if os.path.isfile(file_prj):
#     ident = Sridentify(mode='cli', call_remote_api=False)
#     ident.from_file(file_prj)
#     srid = ident.get_epsg()
#     print(srid)
#
#     if srid:
#         srid_source = ' -s ' + str(srid) + ':4326 '
#     else:
#         srid_source = ' -s ' + cfg.DEFAULT_EPSG
#

# print(os.path.join(r, file))
# print(file_in)
