# Script to install, start, and accept proper permissions for the Notification Listener
# Using the coordinates extracted from AndroidViewClient dump, it should work for any given device model/screen sizes
# Depends on the tool "AndroidViewClient" (https://github.com/dtmilano/AndroidViewClient)
# Assumes the above is installed/downloaded, and have /path/to/AndroidViewClient/tools in PATH
# Also requires /path/to/Android/Sdk/platform-tools be in the PATH
import sys
import subprocess
import time
import re

# Get a list of the currently connected devices to iterate over
listConnected = ['adb', 'devices']
devices = subprocess.Popen(listConnected, stdout=subprocess.PIPE).communicate()[0].decode("utf-8")
deviceList = devices.split()
filteredList = list(filter(lambda x : "emulator" in x, deviceList))

# Function to invoke a tap event on a given UI element given the line output from AVC dump and the device
def tapElement(line, dev):
    coords = re.search(r"\(\d+,\d+\)", line.replace(" ", "").strip()).group(0)
    coords = coords.replace("(", "").replace(")", "").split(",")
    tap = ['adb', '-s', dev, 'shell', 'input', 'tap', str(coords[0]), str(coords[1])]
    subprocess.Popen(tap)

for dev in filteredList:
    install = ['adb', '-s', dev, 'install', './APKS/app-debug.apk']
    start = ['adb', '-s', dev, 'shell', 'monkey', '-p', 'com.example.GetNotificationService', '-c', 'android.intent.category.LAUNCHER', '1']
    dump = ['dump', '-c', dev]
    back = ['adb', '-s', dev, 'shell', 'input', 'keyevent', 'KEYCODE_BACK']

    #Install and Start
    #Sleeps may or may not be necessary: I have them in just to ensure the events don't go faster than the emulator can process/complete
    subprocess.Popen(install)
    time.sleep(2)
    subprocess.Popen(start)
    time.sleep(2)

    #Once app starts, it will open on the notification access permission screen
    #Dump the UI elements and split them into a list
    dumpOut = subprocess.Popen(dump, stdout=subprocess.PIPE).communicate()[0].decode("utf-8")
    dumpOut = dumpOut.split("\n")

    # If we find a TextView w/ "GetNotification", we know that the next line will correspond to the associated toggle switch
    # Then tap that toggle switch
    for i in range(0,len(dumpOut)):
        if "GetNotification" in dumpOut[i]:
            tapElement(dumpOut[i+1], dev)
            break
    # When toggle switch is tapped, a confirmation popup is presented
    # Now, dump the screen UI once more to get this popup's coords
    time.sleep(1)
    dumpOut = subprocess.Popen(dump, stdout=subprocess.PIPE).communicate()[0].decode("utf-8")
    dumpOut = dumpOut.split("\n")
    time.sleep(1)
    # Find and tap the ALLOW/Allow option 
    # If line/element is not a button, we can skip 
    # (This lets us ignore any random text w/ the word Allow in it)   
    for line in dumpOut:
        print(line)
        if not "Button" in line:
            continue
        else:
            if "ALLOW" in line or "Allow" in line:
                tapElement(line, dev)
                break
    # Return to the Notification Listener app screen
    time.sleep(1)
    subprocess.Popen(back)