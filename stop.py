import sys
import subprocess
import json
import telnetlib
import time

def listConnected():
    listConnected = ['adb', 'devices']
    devices = subprocess.Popen(listConnected, stdout=subprocess.PIPE).communicate()[0].decode("utf-8")
    deviceList = devices.split()
    filteredList = list(filter(lambda x : "emulator" in x, deviceList))
    return filteredList

def getName(dev):
    port = str(dev).split('-')[1]
    HOST = 'localhost'
    # AUTH = 'NwhG3frGXDUGGYBz'
    AUTH = '555KjfyUBwIiO+h4'
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

inp = sys.argv[1]

with open(inp) as f:
    jsonList = json.loads(f.read())

nameList = []

for device in jsonList:
    nameList.append(device['name'])

devices = listConnected()

if (len(devices) == 0):
    exit()


for dev in devices:
    stop = ['adb', '-s', str(dev), 'emu', 'kill']
    devName = getName(dev)
    if (devName in nameList):
        subprocess.Popen(stop).communicate()

