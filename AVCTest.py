import sys
import subprocess
import time
import re

listConnected = ['adb', 'devices']
devices = subprocess.Popen(listConnected, stdout=subprocess.PIPE).communicate()[0].decode("utf-8")
deviceList = devices.split()
filteredList = list(filter(lambda x : "emulator" in x, deviceList))

for dev in filteredList:
    start = ['adb', '-s', dev, 'shell', 'monkey', '-p', 'com.yahoo.mobile.client.android.yahoo', '-c', 'android.intent.category.LAUNCHER', '1']
    dump = ['dump', '-c', dev]

    subprocess.Popen(start)
    time.sleep(5)
    dumpOut = subprocess.Popen(dump, stdout=subprocess.PIPE).communicate()[0].decode("utf-8")
    
    dumpOut = dumpOut.split("\n")
    for line in dumpOut:
        try:
            coords = re.search(r"\(\d+,\d+\)", line.replace(" ", "").strip()).group(0)
        except:
            continue
        print("LINE = " + line)   
        print(str(coords))
        