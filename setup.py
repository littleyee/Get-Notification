import sys
import subprocess
import json
import re
import time

inp = sys.argv[1]

with open(inp) as f:
    jsonList = json.loads(f.read())

def tapElement(line, dev):
    coords = re.search(r"\(\d+,\d+\)", line.replace(" ", "").strip()).group(0)
    coords = coords.replace("(", "").replace(")", "").split(",")
    tap = ['adb', '-s', dev, 'shell', 'input', 'tap', str(coords[0]), str(coords[1])]
    subprocess.Popen(tap).communicate()
    return

def tap(target, dev):
    dump = ['dump', '-c', str(dev)]
    dumpOut = subprocess.Popen(dump, stdout=subprocess.PIPE).communicate()[0].decode("utf-8")
    dumpOut = dumpOut.split("\n")
    for line in dumpOut:
        if (target in line):
            tapElement(line, dev)
            break
    return

def tapCoords(x, y, dev):
    command = ['adb', '-s', str(dev), 'shell', 'input', 'tap', str(x), str(y) ]
    subprocess.Popen(command).communicate()
    return

def swipe(dir, dev):
    if (dir == 'r' or dir == 'right'):
        command = ['adb', '-s', str(dev), 'shell', 'input', 'swipe', '0', '100', '500', '100']
    elif (dir == 'l' or dir == 'left'):
        command = ['adb', '-s', str(dev), 'shell', 'input', 'swipe', '500', '100', '0', '100']
    elif (dir == 'u' or dir == 'up'):
        command = ['adb', '-s', str(dev), 'shell', 'input', 'swipe', '100', '500', '100', '0']
    elif (dir == 'd' or dir == 'down'):
        command = ['adb', '-s', str(dev), 'shell', 'input', 'swipe', '100', '300', '100', '800']
    
    subprocess.Popen(command).communicate()
    return

def launch(package, dev):
    command = ['adb', '-s', str(dev), 'shell', 'monkey', '-p', str(package), '-c', 'android.intent.category.LAUNCHER', '1']
    subprocess.Popen(command).communicate()
    return

def key(keycode, dev):
    command = ['adb', '-s', str(dev), 'shell', 'input', 'keyevent', str(keycode)]
    subprocess.Popen(command).communicate()
    return

def text(text, dev):
    command = ['adb', '-s', str(dev), 'shell', 'input', 'text', str(text)]
    subprocess.Popen(command).communicate()
    return

def stop(package, dev):
    command = ['adb', '-s', str(dev), 'shell', 'am', 'force-stop', str(package)]
    subprocess.Popen(command).communicate()

def dismissApp(dev):
    switch = ['adb', '-s', str(dev), 'shell', 'input', 'keyevent', 'KEYCODE_APP_SWITCH']
    swipe = ['adb', '-s', str(dev), 'shell', 'input', 'swipe', '500', '800', '500', '100']
    home = ['adb', '-s', str(dev), 'shell', 'input', 'keyevent', 'KEYCODE_HOME']

    subprocess.Popen(switch).communicate()
    time.sleep(1)
    subprocess.Popen(swipe).communicate()
    time.sleep(1)
    subprocess.Popen(home).communicate()


# Get a list of the currently connected devices to iterate over
listConnected = ['adb', 'devices']
devices = subprocess.Popen(listConnected, stdout=subprocess.PIPE).communicate()[0].decode("utf-8")
deviceList = devices.split()
filteredList = list(filter(lambda x : "emulator" in x, deviceList))

for dev in filteredList:
    for command in jsonList:
        if(command['action'] == "click"):
            tap(command['text'], dev)

        elif(command['action'] == "swipe"):
            swipe(command['direction'], dev)

        elif(command['action'] == "start"):
            launch(command['package'], dev)

        elif(command['action'] == "stop"):
            stop(command['package'], dev)

        elif(command['action'] == "text"):
            text(command['text'], dev)

        elif(command['action'] == "key"):
            key(command['key'], dev)
        
        elif(command['action'] == "close"):
            dismissApp(dev)
        
        elif(command['action'] == "clickCoords"):
            tapCoords(command['x'], command['y'], dev)
        time.sleep(2)
        
