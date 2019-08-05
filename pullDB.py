#!/usr/bin/python

# Code to pull the databases from running Android VMs
# Input1: File defining the virtual machines for the test (same as one used for VM creation)
# Input2: Path to save the .sql file to
# Output: A .sql file w/ entries from all tables


import subprocess
import sqlite3
import time
import json
import telnetlib
import datetime
import os
import sys
import time

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
path = sys.argv[2]

date = datetime.date.today()

listConnected = ['adb', 'devices']
devices = subprocess.Popen(listConnected, stdout=subprocess.PIPE).communicate()[0].decode("utf-8")
deviceList = devices.split()
filteredList = list(filter(lambda x : "emulator" in x, deviceList))

if (len(filteredList) == 0):
    print("There are no VMs running")
    exit

with open(path + "/" + str(date) + ".sql", 'w+') as f:
    f.write('BEGIN TRANSACTION;\nCREATE TABLE Notification_Table ( Package VARCHAR(255), Title VARCHAR(255), Content VARCHAR(255), TimeStamp VARCHAR(255), Location VARCHAR(255) );\n')
    for dev in filteredList:
        adbRoot = ['adb', '-s', str(dev), 'root']
        subprocess.Popen(adbRoot).communicate()
        devName = getName(str(dev))
        devLoc = getLocation(testFile, devName)
        # if not os.path.exists('./' + str(devName)):
        #     os.mkdir('./' + str(devName))
        # adbPull = ['adb', '-s', dev, 'pull', 'data/data/com.example.GetNotificationService/databases/Notification_Record.db',  './' + str(devName) + '/' + str(devName) + '_' + str(date) + '.db']
        adbPull = ['adb', '-s', dev, 'pull', 'data/data/com.example.GetNotificationService/databases/Notification_Record.db']
        subprocess.Popen(adbPull).communicate()
        conn = sqlite3.connect('Notification_Record.db')

        dump = str(date) + ".sql"
        
    
        for line in conn.iterdump():
            if ('INSERT INTO \"Notification_Table\"' in line):
                timestamp = int(line.split(',')[-1].replace(');', '').replace('\'', ''))
                if(timestamp > (time.time() * 1000) - 86400000):
                    f.write(line.replace(');', ',\'' + str(devLoc))+ '\');\n')  
        conn.close()

        #Remove this file (it isn't needed)
        subprocess.Popen(['rm', 'Notification_Record.db'])
    f.write("COMMIT;")




