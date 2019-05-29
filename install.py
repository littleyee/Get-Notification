import sys
import subprocess
import time

def filterDevices(var):
    if ("emulator" in var):
        return True
    else:
        return False
    


# Script to launch emulator and install the GetNotification 
# usage: python install.py <Path to APK>
# IMPORTANT: For simplicity,script assumes that the path leading to the "emulator" and "platform-tools" folders within the Android SDK have been added to PATH variable
# These should be in locations like: C:\Users\<UserNameHere>\AppData\Local\Android\Sdk\emulator and C:\Users\<UserNameHere>\AppData\Local\Android\Sdk\platform-tools on Windows
# OSX locations /Users/<User>/Library/Android/sdk/...

# Takes as argument the path to the Get-Notification apk file
pathToAppApk = sys.argv[1]
# Form console command to list installed vms
listAvds = ['emulator', '-list-avds']
# Save result to variable
# Everything below right now only works for single VM
# TODO: Change to work with list of VMs
avds = subprocess.Popen(listAvds, stdout=subprocess.PIPE).communicate()[0].decode("utf-8")
avdList = avds.split()


# launch each emulator from the avd list
# This sometimes seems to crash a number of the vms when launching like this
for avd in avdList:
    # Launch VM(s)
    launch = ['emulator', '-avd', str(avd)]
    subprocess.Popen(launch, shell=True)
    time.sleep(60)

time.sleep(30)

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

# For each device, install the Get-Notification APK
for device in filteredList:
    install = ['adb', '-s', device, 'install', pathToAppApk]
    subprocess.Popen(install, shell=True)


