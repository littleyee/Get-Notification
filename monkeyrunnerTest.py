## This is a quick test of monkeyrunner
## monkeyrunner is apparently difficult when it comes to paths, so full paths are needed to files (I can show how it works in person on Wed.)
## the monkeyrunner.bat file actually has errors in it, and needs to be edited to even run without error


## If you are editing this code in an IDE with autocomplete/linting/etc. the IDE probably wont find the com.android.monkeyrunner import and will give you warnings/errors
## It does still run despite this, since it goes through the monkeyrunner application which interprets it using Jython instead (and it correctly resolves this import)
## I'll look into if there's any way to get regular Python to recognize it
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

device = MonkeyRunner.waitForConnection()

device.installPackage('C:/Users/jthie/Desktop/SPARTALabRepos/Get-Notification/GetNotification/app/build/outputs/apk/debug/app-debug.apk')

## IMPORTANT: Google/Android Devs' example is wrong: this is NOT supposed to be the package, it is supposed to be the ApplicationID (found in the build.gradle file) 
package = "com.example.GetNotificationService"
activity = "com.example.MyGetNotificationApp.MainActivity"

runComponent = package + '/' + activity


device.startActivity(component=runComponent)

result = device.takeSnapshot()

result.writeToFile("C:/Users/jthie/Desktop/SPARTALabRepos/test.png", "png")

## Things we need to figure out:
## This now installs and launches the notification listener
## On startup, user is automatically redirected to notification privleges screen
## We need to find out how to programatically find our app in the list and toggle the permissions to on
## From there we can open browser and send the machines to visit pages
## I know that there is a way to send psuedo random events/actions to the vms, but I'll need to see if that's even what we want