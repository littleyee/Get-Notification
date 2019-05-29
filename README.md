# NotificationListener


An Android application which we are using to log information about notifications (of particular interest are push notifications from advertisers) and store them for later analysis.

## Current Features:

1. Prompts user to give the app necessary elevated privileges. 
2. Captures notifications posted to the phone from any source.
3. Stores the relevant details (name of the apps that sending notification, timestamp of posting, title and content) about the notification in an SQLite database for future extraction.

## Next Steps:

1. We will need to find some method of extracting the data from the virtual phones to a real device at some point.
2. We will need to start looking into methods for simulating/automating user input to carry out the tests. monkeyrunner, espresso, JUnit

## install.py:

This is a Python script that launches a VM and installs a specified app via its .apk file.
It is in an early stage at this point, but it should be a good example for the groundwork:

Usage: from the command line: python install.py "Path to APK to install" Or:  python3 install.py "Path to APK to install" (It is written in Python 3)

1. Be sure to run the build command in Android Studio if there is no .apk file for the app in your local version. Should be in a location like "..\app\build\outputs\apk" or "..\app\build\outputs\apk\debug"
2. On launch/install of the Get-Notification app, the user is prompted to give the correct permissions to listen to notifications: we will need to find some way to automate the action of giving that access.
3. There are a few assumptions about what is in your PATH enviornmental variable in order to run the console commands: I can clarify this when we meet in person. (Paths to the emulator and adb binaries in the Android SDK)
4. The VM is launching w/ the GUI for now just for ease of verifying the installation: will eventually need to revise to launch in headless mode.


## monkeyrunnerTest.py
https://developer.android.com/studio/test/monkeyrunner/index.html This is closer to what we will eventually want for event simulation. 
This is a test Python script using the monkeyrunner tool that is part of the Android SDK.  
We can use it to load and launch apps on a VM, as well as use it to simulate keypresses/user interaction. 
(We can decide whether we want to try to use monkeyrunner to launch and install, or the install.py depending on what will be simpler in the long run.)


