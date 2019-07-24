import sys
import subprocess
import time
import json
from geopy.geocoders import Nominatim


# Script to create VMs as specified by  
# usage: python install.py <Path to .json file>
# IMPORTANT: For simplicity,script assumes that the path leading to the "emulator", "platform-tools", and "avdmanager" folders within the Android SDK have been added to PATH variable
# These should be in locations like: C:\Users\<UserNameHere>\AppData\Local\Android\Sdk\emulator, C:\Users\<UserNameHere>\AppData\Local\Android\Sdk\platform-tools, and C:\Users\<User>\AppData\Local\Android\Sdk\tools\bin on Windows
# OSX locations /Users/<User>/Library/Android/sdk/...

# Right now, assumes no other emulators are running
# It's been harder than expected to keep track of emulators by name
# (Makes it difficult to assign the right apks, location, etc. to the correct VM)
# When I moved things to the server, the command I was using to extract the name didn't return any output to the terminal like it did on my machine
# The current workaround is to just create and launch the VMs one by one, but this assumes it is the only VM running
# TODO: Find a better solution for keeping track of what emulators are which

# Input of path to a .json file specifying a list of vms
inp = sys.argv[1]

#Initialize geopy geocoder
locator = Nominatim(user_agent="PushNotifications")


# Open and read the content of the file, and load it as a python object
with open(inp) as f:
    jsonList = json.loads(f.read())

# For each device in the list, build and run the avdmanager creation command
for device in jsonList:
    
    create = ['avdmanager', 'create', 'avd',  '-n', device['name'], '-k', device['version'], '-d', device['deviceId']]
    bootStatus = ['adb', 'shell', 'getprop', 'sys.boot_completed']
    stop = ['adb', 'emu', 'kill']
    launch = ['emulator-headless', '-avd', str(device['name']), '-gpu', 'off']
    
    location = locator.geocode(device['location'])
    lat = location.latitude
    long = location.longitude
    setCoords = ['adb', 'emu', 'geo', 'fix', str(long), str(lat)]

    subprocess.Popen(create)
    time.sleep(5)
    subprocess.Popen(launch)
    while True:
        booted = subprocess.Popen(bootStatus, stdout=subprocess.PIPE).communicate()[0].decode("utf-8")
        time.sleep(1)
        if booted.strip() == "1":
            break
    
    subprocess.Popen(setCoords)

    for apk in device['apks']:
        install = ['adb', 'install', apk]
        subprocess.Popen(install)
        time.sleep(5)

    subprocess.Popen(stop)

    time.sleep(5)

## The below will be moved to separate scripts/functions to launch all emulators
##
##
# # Form console command to list installed vms
# listAvds = ['emulator', '-list-avds']

# # Send command to console and save output in stdout to variable
# avds = subprocess.Popen(listAvds, stdout=subprocess.PIPE).communicate()[0].decode("utf-8")
# avdList = avds.split()
# print(str(avdList))

# # launch each emulator from the avd list
# # Be sure to have enough RAM to actually run this (the vms are very RAM and CPU hungry)


# for avd in avdList:
#     # Launch VM(s)
#     # Launch in "headless" mode 
#     launch = ['emulator-headless', '-avd', str(avd), '-gpu', 'off']
#     # Launch w/ GUI 
#     #launch = ['emulator', '-avd', str(avd)]
#     subprocess.Popen(launch)
#     time.sleep(2)
   
# # Get a list of the connected devices
# # These are in a different format than the names used to launch (emulator id), hence the different command
# # Emulator ids look something like "emulator-port#" i.e. "emulator-5554"
# listConnected = ['adb', 'devices']
# devices = subprocess.Popen(listConnected, stdout=subprocess.PIPE).communicate()[0].decode("utf-8")


# print(devices)

# # Split input into a list, filter list to only have emulator ids 
# deviceList = devices.split()
# filteredList = list(filter(lambda x : "emulator" in x, deviceList))
# print(filteredList)


# time.sleep(10)
# # Wait for devices to boot up fully before executing further commands, then do some more configuration
# for device in filteredList:
#     # command to get status of its boot
#     bootStatus = ['adb', '-s', device, 'shell', 'getprop', 'sys.boot_completed']
#     print("Checking if " + device + " has booted")
#     # Check that the boot is completed on a loop until it is true, then break
#     while True:
#         booted = subprocess.Popen(bootStatus, stdout=subprocess.PIPE).communicate()[0].decode("utf-8")
#         time.sleep(1)
#         if booted.strip() == "1":
#             print(device + " booted")
#             break
    
#     # For each device, do some configuration
#     # install apks, set location
#     # Need to get the assigned name of the emulators and compare them to names in json file
#     # Have to do this since adb use serial numbers instead of vm names, so we need to jump through some hoops to get the names back
#     getDevName = ['adb', '-s', device, 'emu', 'avd', 'name']
#     out = (subprocess.Popen(getDevName, stdout=subprocess.PIPE).communicate()[0].decode("utf-8")).split()
#     name = (list(filter(lambda x: not("OK" in x), out)))[0]

#     for dev in jsonList:
#         if dev['name'] == name:
#             for apk in dev['apks']:
#                 install = ['adb', '-s', device, 'install', apk]
#                 subprocess.Popen(install)
#             location = locator.geocode(dev['location'])
#             lat = location.latitude
#             long = location.longitude
#             setCoords = ['adb', '-s', device, 'emu', 'geo', 'fix', str(long), str(lat)]
#             subprocess.Popen(setCoords)
#         else:
#             continue
#     time.sleep(5)


   

        
   


