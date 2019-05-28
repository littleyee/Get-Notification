## This is a quick test of monkeyrunner
## monkeyrunner is apparently difficult when it comes to paths, so full paths are needed to files (I can show how it works in person on Wed.)
## the monkeyrunner.bat file actually has errors in it, and needs to be edited to even run without error

from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

device = MonkeyRunner.waitForConnection()

device.installPackage('C:/Users/jthie/Desktop/SPARTALabRepos/Get-Notification/GetNotification/app/build/outputs/apk/debug/app-debug.apk')

package = "com.example.MyGetNotificationApp"
activity = "com.example.MyGetNotificationApp.MainActivity"

runComponent = package + "/" + activity

## This line doesn't seem to actually launch anything?
device.startActivity(component=runComponent)

result = device.takeSnapshot()

result.writeToFile("C:/Users/jthie/Desktop/SPARTALabRepos/test.png", "png")