import sys
import subprocess
import time
import itertools
import re
import json
import telnetlib
import datetime
import multiprocessing
import os

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

def tapElement(line, dev):
    coords = re.search(r"\(\d+,\d+\)", line.replace(" ", "").strip()).group(0)
    coords = coords.replace("(", "").replace(")", "").split(",")
    tap = ['adb', '-s', dev, 'shell', 'input', 'tap', str(coords[0]), str(coords[1])]
    subprocess.Popen(tap).communicate()
    return

def dump(dev):
    command = ['dump', '-c', str(dev)]
    out = subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0].decode("utf-8")
    out = out.split("\n")
    return out

def getPackNames(dev):
    command = "adb -s " + str(dev) + " shell pm list packages -f | grep data"
    output = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).communicate()[0].decode("utf-8")
    output = output.split('\n')
    packs = []
    for line in output:
        if (not(line == '')):
            pack = line.split("base.apk=")[-1]
            packs.append(pack)
    return packs

## KEYCODE_APP_SWITCH
## Swipe up
## Home
def dismissApp(dev):
    switch = ['adb', '-s', str(dev), 'shell', 'input', 'keyevent', 'KEYCODE_APP_SWITCH']
    swipe = ['adb', '-s', str(dev), 'shell', 'input', 'swipe', '360', '421', '360', '100']
    home = ['adb', '-s', str(dev), 'shell', 'input', 'keyevent', 'KEYCODE_HOME']

    subprocess.Popen(switch).communicate()
    time.sleep(5)
    subprocess.Popen(swipe).communicate()
    time.sleep(5)
    subprocess.Popen(home).communicate()
    time.sleep(3)

def listConnected():
    listConnected = ['adb', 'devices']
    devices = subprocess.Popen(listConnected, stdout=subprocess.PIPE).communicate()[0].decode("utf-8")
    deviceList = devices.split()
    filteredList = list(filter(lambda x : "emulator" in x, deviceList))
    return filteredList

def triggerNotifs(dev):
    openStatusBar = ['adb', '-s', str(dev), 'shell', 'input', 'swipe', '500', '0', '500', '900']
    home = ['adb', '-s', str(dev), 'shell', 'input', 'keyevent', 'KEYCODE_HOME']

    while(True):
        # Here's one cycle of targeting a notif.
        # Have to repeat this for each non system notification
        subprocess.Popen(openStatusBar).communicate()
        time.sleep(3)
        dumpOut = dump(dev)
        
        for i in range(0, len(dumpOut)):
            # print(str(line.encode('ascii', 'ignore')))
            if ("id/expand_button" in dumpOut[i]):
                # print(str(dumpOut[i].encode('ascii', 'ignore')))
                tapElement(dumpOut[i], str(dev))
                dumpOut2 = dump(dev)
                for line in dumpOut2:
                    if(("id/title" in line or "id/expanded_notification_title" in line) and not(("Android Setup" in line) or ("Preparing for setup" in line))):
                        # print(line.encode('ascii', 'ignore'))
                        tapElement(line, str(dev))
                        time.sleep(10)   
                        subprocess.Popen(home).communicate()
                        time.sleep(2)
                        dismissApp(str(dev))
                        time.sleep(2)
                        break
                break
            elif (not("id/expand_button" in dumpOut[i]) and i == len(dumpOut) - 1):
                subprocess.Popen(home).communicate()
                time.sleep(1)
               
                return


    return

def trigger (dev, port):
    openStatusBar = ['adb', '-s', str(dev), 'shell', 'input', 'swipe', '500', '0', '500', '900']
    home = ['adb', '-s', str(dev), 'shell', 'input', 'keyevent', 'KEYCODE_HOME']
    bootStatus = ['adb', '-s', str(dev), 'shell', 'getprop', 'sys.boot_completed']
    
    exit = ['adb', '-s', str(dev), 'emu', 'kill']
    

    
    time.sleep(2)
    print("Checking if booted")
    while True:
        booted = subprocess.Popen(bootStatus, stdout=subprocess.PIPE).communicate()[0].decode("utf-8")
        time.sleep(1)
        if booted.strip() == "1":
            break
    print("Boot complete")

    devName = getName(dev)
    print(devName)
    mitmdump = ['mitmdump', '--listen-host', '127.0.0.1', '--listen-port', str(port), '-w', path + '/' + date + '/' + devName + '_' + date + '.flow']
    relaunch = ['emulator-headless', '-avd', devName, '-noaudio', '-gpu', 'off', '-writable-system']
    proxy = subprocess.Popen(mitmdump)


    ## Do this twice to attempt to minimize fail rate
    ## The simulated swipe inputs will occasionally fail and mess up the whole process
    
    triggerNotifs(dev)
#     subprocess.Popen(home).communitcate()
#     time.sleep(1)
#     triggerNotifs(dev)

    
    
    proxy.terminate()
    
    ## TODO: Move this to outside of loop?
    ## Sometimes saving state takes minutes to actually complete
    ## Terminate proxy as before, but close/relaunch machines afterwards
    subprocess.Popen(exit).communicate()
   
    
    print("Waiting for state to save")
    while True:
        currentList = listConnected()
        if (not(dev in currentList)):
            break
                
    
    subprocess.Popen(relaunch)


if __name__ == '__main__':

    inp = sys.argv[1]
    path = sys.argv[2]

    date = str(datetime.date.today())

    if not os.path.exists(path + '/' + str(date)):
        os.mkdir(path + '/' + str(date))

    with open(inp) as f:
        jsonList = json.loads(f.read())

        
    stopList = listConnected()

    if (len(stopList) == 0):
        exit()
        
    for dev in stopList:
        stop = ['adb', '-s', str(dev), 'emu', 'kill']
        subprocess.Popen(stop).communicate()
        print("Waiting for state to save")
        while True:
            currentList = listConnected()
            if (not(dev in currentList)):
                break

    print("State saved")
    port = 8890
    for device in jsonList:
        launch = ['emulator-headless', '-avd', str(device['name']), '-noaudio', '-gpu', 'off', '-writable-system', '-http-proxy', '127.0.0.1:' + str(port)]
        subprocess.Popen(launch)
        port += 1

    

    time.sleep(5)
    filteredList = listConnected()
    print("Launched")

    port = 8890 
    for dev in filteredList:
        multiprocessing.Process(target=trigger, args=(dev, port)).start()
        port += 1
        
        
    



    
