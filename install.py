import sys
import subprocess
import time
import json

def filterDevices(var):
    if ("emulator" in var):
        return True
    else:
        return False
    


# Script to launch emulator and install the GetNotification 
# usage: python install.py <Path to .json file>
# IMPORTANT: For simplicity,script assumes that the path leading to the "emulator", "platform-tools", and "avdmanager" folders within the Android SDK have been added to PATH variable
# These should be in locations like: C:\Users\<UserNameHere>\AppData\Local\Android\Sdk\emulator, C:\Users\<UserNameHere>\AppData\Local\Android\Sdk\platform-tools, and C:\Users\<User>\AppData\Local\Android\Sdk\tools\bin on Windows
# OSX locations /Users/<User>/Library/Android/sdk/...


# Input of path to a .json file specifying a list of vms
inp = sys.argv[1]

# Open and read the content of the file, and load it as a python object
with open(inp) as f:
    jsonList = json.loads(f.read())

# For each device in the list, build and run the avdmanager creation command
for device in jsonList:
    create = ['avdmanager', 'create', 'avd',  '-n', device['name'], '-k', device['version'], '-d', device['deviceId']]
    subprocess.Popen(create, shell=True)
    time.sleep(10)

# Form console command to list installed vms
listAvds = ['emulator', '-list-avds']
# Send command to console and save output in stdout to variable
avds = subprocess.Popen(listAvds, stdout=subprocess.PIPE).communicate()[0].decode("utf-8")
avdList = avds.split()


# launch each emulator from the avd list
# Be sure to have enough RAM to actually run this (the vms are very RAM and CPU hungry)


for avd in avdList:
    # Launch VM(s)
    if (avd == "Nexus_5X_API_28_x86"):
        continue
    #launch = ['emulator', '-avd', str(avd), '-no-audio', '-no-window']
    launch = ['emulator', '-avd', str(avd)]
    subprocess.Popen(launch, shell=True)
    time.sleep(10)
   
# Get a list of the connected devices
# These are in a different format than the names used to launch (emulator id), hence the different command
# Emulator ids look something like "emulator-port#" i.e. "emulator-5554"
listConnected = ['adb', 'devices']
devices = subprocess.Popen(listConnected, stdout=subprocess.PIPE).communicate()[0].decode("utf-8")


print(devices)

# Split input into a list, filter list to only have emulator ids 
deviceList = devices.split()
filteredList = list(filter(lambda x : "emulator" in x, deviceList))
print(filteredList)


time.sleep(10)
# Wait for devices to boot up fully before executing further commands
for device in filteredList:
    bootStatus = ['adb', '-s', device, 'shell', 'getprop', 'sys.boot_completed']
    print("Waiting for " + device + " to boot")
    while True:
        booted = subprocess.Popen(bootStatus, stdout=subprocess.PIPE).communicate()[0].decode("utf-8")
        time.sleep(5)
        if booted.strip() == "1":
            print(device + " booted")
            break

# TODO: the code below will need to be changed once we have apk paths in the json file to use
# For each device, install the Get-Notification APK
#for device in filteredList:
#    install = ['adb', '-s', device, 'install', pathToAppApk]
#    subprocess.Popen(install, shell=True)


