import sys
import subprocess
import time
import re

listConnected = ['adb', 'devices']
devices = subprocess.Popen(listConnected, stdout=subprocess.PIPE).communicate()[0].decode("utf-8")
deviceList = devices.split()
filteredList = list(filter(lambda x : "emulator" in x, deviceList))

def tapElement(line, dev):
    coords = re.search(r"\(\d+,\d+\)", line.replace(" ", "").strip()).group(0)
    coords = coords.replace("(", "").replace(")", "").split(",")
    tap = ['adb', '-s', dev, 'shell', 'input', 'tap', str(coords[0]), str(coords[1])]
    subprocess.Popen(tap)

for dev in filteredList:
    install = ['adb', '-s', dev, 'install', './GetNotification/app/build/outputs/apk/debug/app-debug.apk']
    start = ['adb', '-s', dev, 'shell', 'monkey', '-p', 'com.example.GetNotificationService', '-c', 'android.intent.category.LAUNCHER', '1']
    dump = ['dump', '-c', dev]
    back = ['adb', '-s', dev, 'shell', 'input', 'keyevent', 'KEYCODE_BACK']

    subprocess.Popen(install)
    time.sleep(2)
    subprocess.Popen(start)
    time.sleep(2)
    dumpOut = subprocess.Popen(dump, stdout=subprocess.PIPE).communicate()[0].decode("utf-8")
    dumpOut = dumpOut.split("\n")
    for i in range(0,len(dumpOut)):
        if "GetNotification" in dumpOut[i]:
            tapElement(dumpOut[i+1], dev)
            break
    time.sleep(1)
    dumpOut = subprocess.Popen(dump, stdout=subprocess.PIPE).communicate()[0].decode("utf-8")
    dumpOut = dumpOut.split("\n")
    time.sleep(1)   
    for line in dumpOut:
        if "ALLOW" in line:
            tapElement(line, dev)
            break
    time.sleep(1)
    subprocess.Popen(back)