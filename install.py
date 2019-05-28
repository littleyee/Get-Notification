import sys
import subprocess
import time

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
avd = subprocess.Popen(listAvds, stdout=subprocess.PIPE).communicate()[0].decode("utf-8")
print(avd)

# Launch VM(s)
launch = ['emulator', '-avd', str(avd)]
subprocess.Popen(launch, shell=True)

# Give some time for VMs to launch
time.sleep(30)

# Install the Get-Notification APK
install = ['adb', 'install', pathToAppApk]
subprocess.Popen(install, shell=True)


