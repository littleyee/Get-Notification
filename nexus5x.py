import sys
import subprocess
import time

listConnected = ['adb', 'devices']
devices = subprocess.Popen(listConnected, stdout=subprocess.PIPE).communicate()[0].decode("utf-8")
deviceList = devices.split()
filteredList = list(filter(lambda x : "emulator" in x, deviceList))

for dev in filteredList:
    install = ['adb', '-s', dev, 'install', './GetNotification/app/build/outputs/apk/debug/app-debug.apk']
    start = ['adb', '-s', dev, 'shell', 'monkey', '-p', 'com.example.GetNotificationService', '-c', 'android.intent.category.LAUNCHER', '1']
    tap1 = ['adb', '-s', dev, 'shell', 'input', 'tap', '950', '550']
    tap2 = ['adb', '-s', dev, 'shell', 'input', 'tap', '880', '1260']
    tap3 = ['adb', '-s', dev, 'shell', 'input', 'tap', '270', '1840']

    subprocess.Popen(install)
    time.sleep(2)
    subprocess.Popen(start)
    time.sleep(5)
    subprocess.Popen(tap1)
    time.sleep(2)
    subprocess.Popen(tap2)
    time.sleep(2)
    subprocess.Popen(tap3)
    


