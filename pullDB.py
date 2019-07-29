# Code to pull the databases from running Android VMs
# Input: File defining the virtual machines for the test (same as one used for VM creation)
# Output: A .sql file w/ entries from all tables

# TODO: Filter out any entry whose timestamp is > 24 hours ago

import subprocess
import sqlite3
import time
import json
import telnetlib
import datetime
import os
import sys

def getName(dev):

    port = str(dev).split('-')[1]
    HOST = 'localhost'
    AUTH = 'NwhG3frGXDUGGYBz'
    tel = telnetlib.Telnet(HOST, port)
    time.sleep(1)
    output = tel.read_very_eager()
    # print(str(output))
    tel.write('auth ' + AUTH + '\n')
    time.sleep(1)
    tel.write("avd name + \n")
    time.sleep(1)
    output =  tel.read_very_eager()
    # print(str(output))

    output = output.split("OK")
    return str(output[1].strip())

def getLocation(file, name):
    with open(file) as f:
        jsonList = json.loads(f.read())

    for device in jsonList:
        if (device['name'] == name):
            return device['location']

testFile = sys.argv[1]

date = datetime.date.today()

listConnected = ['adb', 'devices']
devices = subprocess.Popen(listConnected, stdout=subprocess.PIPE).communicate()[0].decode("utf-8")
deviceList = devices.split()
filteredList = list(filter(lambda x : "emulator" in x, deviceList))



with open(str(date) + ".sql", 'w') as f:
    f.write('BEGIN TRANSACTION;\nCREATE TABLE Notification_Table ( Package VARCHAR(255), Title VARCHAR(255), Content VARCHAR(255), TimeStamp VARCHAR(255), Location VARCHAR(255) );\n')
    for dev in filteredList:
        adbRoot = ['adb', '-s', str(dev), 'root']
        subprocess.Popen(adbRoot)
        time.sleep(3)
        
        devName = getName(dev)
        devLoc = getLocation(testFile, devName)
        # if not os.path.exists('./' + str(devName)):
        #     os.mkdir('./' + str(devName))
        # adbPull = ['adb', '-s', dev, 'pull', 'data/data/com.example.GetNotificationService/databases/Notification_Record.db',  './' + str(devName) + '/' + str(devName) + '_' + str(date) + '.db']
        adbPull = ['adb', '-s', dev, 'pull', 'data/data/com.example.GetNotificationService/databases/Notification_Record.db']
        subprocess.Popen(adbPull)
        time.sleep(1)
        conn = sqlite3.connect('Notification_Record.db')

        dump = str(date) + ".sql"
        
    
        for line in conn.iterdump():
            if ('INSERT INTO \"Notification_Table\"' in line):
                f.write(line.replace(');', ',\'' + str(devLoc))+ '\');\n')  
        conn.close()
    f.write("COMMIT;")




