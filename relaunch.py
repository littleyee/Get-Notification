import sys
import subprocess
import json
import multiprocessing
import time


def launchGN(dev):
    bootStatus = ['adb', '-s', str(dev), 'shell', 'getprop', 'sys.boot_completed']
    back = ['adb', '-s', dev, 'shell', 'input', 'keyevent', 'KEYCODE_BACK']
    home = ['adb', '-s', str(dev), 'shell', 'input', 'keyevent', 'KEYCODE_HOME']
    
    while True:
        booted = subprocess.Popen(bootStatus, stdout=subprocess.PIPE).communicate()[0].decode("utf-8")
        time.sleep(1)
        if booted.strip() == "1":
            break
            
    start = ['adb', '-s', dev, 'shell', 'monkey', '-p', 'com.example.GetNotificationService', '-c', 'android.intent.category.LAUNCHER', '1']
    subprocess.Popen(start).communicate()
    time.sleep(2)
    subprocess.Popen(back).communicate()
    time.sleep(2)
    subprocess.Popen(home).communicate()

if __name__ == '__main__':
    # Take as input the JSON file used for installation
    # Using this just for the emulator names (for launching)
    inp = sys.argv[1]

    # Open and load JSON
    with open(inp) as f:
        jsonList = json.loads(f.read())

    # Iterate through JSON objects
    # Launch emulators by name
    for device in jsonList:
        print(str(device['name']))
        launch = ['emulator-headless', '-avd', str(device['name']), '-gpu', 'off', '-noaudio', '-writable-system']
        subprocess.Popen(launch)


    # Relaunch Notification Listener 
    listConnected = ['adb', 'devices']
    devices = subprocess.Popen(listConnected, stdout=subprocess.PIPE).communicate()[0].decode("utf-8")
    deviceList = devices.split()
    filteredList = list(filter(lambda x : "emulator" in x, deviceList))

    for dev in filteredList:
         multiprocessing.Process(target=launchGN, args=(dev,)).start()