import time

file_csv = str(time.strftime("%Y-%m-%d") + "_shp_info_in_folder_" + ".csv")
folder_win = 'c:\\test'
folder_linux = '/mnt/gisdata'
folder_out_win = 'C:\\Glory\\Projects\\Python\\SHP2PG\\out\\'
folder_out_linux = '/usr/zsniigg/shp_info/out'
schema = 'GISDATA'
host = 'r48-vapp-geos01'
user = 'gisdata'
user_password = 'gisdata'
database_gis = 'gisdb'
csv_delimiter = ';'
value_yes = 'YES'
value_no = 'NO'
value_error = 'ERROR'

server_mail = "r57-vex01.zsniigg.local"
server_mail_port = 25
send_from = 'ZamaraevVV@zsniigg.ru'
send_to = 'ZamaraevVV@zsniigg.ru'
