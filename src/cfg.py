import time

FILE_CSV = str(time.strftime("%Y-%m-%d") + "_shp" + ".csv")
# FOLDER_IN = 'C:\\GIS\\TEST'  # FOLDER_LINUX = '/mnt/gisdata'
FOLDER_IN = 'Z:\\'  # FOLDER_LINUX = '/mnt/gisdata'
FOLDER_OUT = 'C:\\GIS\\out\\' #FOLDER_OUT_LINUX = '/usr/zsniigg/shp_info/out'

FILE_LOG = str(time.strftime("%Y-%m-%d") + "_shp2pg.log")

APP_OGR = '\"C:\\Program Files\\PostgreSQL\\13\\bin\\ogr2ogr.exe\"'

DEFAULT_LOCALE = 'UTF-8'

# 'cp1251'
DEFAULT_EPSG = 'EPSG:4326'


SCHEMA = 'public'
HOST = 'r48-vapp-geos01.zsniigg.local'
USER = 'gisdata'
USER_PASSWORD = 'gisdata'
DATABASE_GIS = 'gisdata'

