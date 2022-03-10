#思科系统备份


import os
import time
import xlrd
from netmiko import ConnectHandler
import threading


#创建文件夹
BASE_DIR = os.path.dirname(__file__)
BACKUP_TIME = time.strftime("%Y-%m-%d",time.localtime())
BACKUP_FILE = os.path.join(BASE_DIR,BACKUP_TIME)
#os.rmdir(BACKUP_FILE)
os.mkdir(BACKUP_FILE)
print("备份文件夹已创建")
print()



wb = xlrd.open_workbook(filename=BASE_DIR+'\\driver.xlsx') #打开excle文件
driver = wb.sheet_by_index(0) #打开设备表格
commond = wb.sheet_by_index(1) #打开命令表格
#表格数据处理
device_infor_all = []
title_rows = driver.row_values(0)#

def get_data():
    for i in range(1,driver.nrows):
        cisco1 = { 
        "device_type": "cisco_ios" if driver.row_values(i)[6] == "ssh" else "cisco_ios_telnet",
        "host": driver.row_values(i)[1],
        "username": driver.row_values(i)[2],
        "password": driver.row_values(i)[3],
        'port' : 22 if driver.row_values(i)[6] == "ssh" else 23,
        "secret": None if driver.row_values(i)[4] == '' else driver.row_values(i)[4],
        }
      
        try:
            netconnect = ConnectHandler(**cisco1)
            if driver.row_values(i)[5] == '思科':
                netconnect.enable()
                for j in range(1,commond.nrows):
                    output = netconnect.send_command(commond.row_values(j)[0])
                    os.chdir(BACKUP_FILE)
                    with open(driver.row_values(i)[0]+ '.txt', 'wt') as f:
                        f.write(output)
                        print(driver.row_values(i)[0] +" backup successful!")
                                               
            else:
                for j in range(1,commond.nrows):
                    output = netconnect.send_command(commond.row_values(j)[0])
                    os.chdir(BACKUP_FILE)
                    with open(driver.row_values(i)[0]+ '.txt', 'wt') as f:
                        f.write(output)
                        print(driver.row_values(i)[0] +" backup successful!")
                        

            netconnect.disconnect()
        except :
            print((driver.row_values(i)[0])+" bankup faild")
                        
get_data()

