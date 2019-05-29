# This is another quick test of some monkeyrunner functionality
# Wanted to see how feasible it was to use the device.touch commands to simulate traffic
# It works generally (since we can use the same device/dimmensions the coordinates should be the same), but will become unwieldly when dealing with dynamic webpages
# To make it so you're not just guessing at pixel coordinates, enable Developer Mode and specify the option to display coordinates
# (In Android 9+ this is difficult to find: Go to settings -> advanced -> then quickly tap "Build Number" until a notice pops up stating "you are now a developer")
import subprocess
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

du = MonkeyDevice.DOWN_AND_UP

listConnected = ['adb', 'devices']
devices = subprocess.Popen(listConnected, stdout=subprocess.PIPE).communicate()[0].decode("utf-8")

deviceList = devices.split()
filteredList = list(filter(lambda x : "emulator" in x, deviceList))
print(filteredList)
for deviceID in filteredList:
    device = MonkeyRunner.waitForConnection('', deviceID)
    result = device.takeSnapshot()
    result.writeToFile("C:/Users/jthie/Desktop/SPARTALabRepos/test.png", "png")
    #device.press('KEYCODE_MENU', MonkeyDevice.DOWN_AND_UP)
    device.touch(733, 1409, du)

