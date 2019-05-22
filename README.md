# NotificationListener


Here is the notification listener program Yiqing started; waits for notification to be posted into the status bar, grabs information, and stores in a SQLite database.

## Current Features:

1. Prompts user to give the app necessary elevated privileges. 
2. Captures notifications posted to the phone from any source.
3. Stores the relevant details (name of the apps that sending notification, timestamp of posting, title and content) about the notification in an SQLite database for future extraction.

## Next Steps:

1. We will need to find some method of extracting the data from the virtual phones to a real device at some point.
2. We will need to start looking into methods for simulating/automating user input to carry out the tests.

## install.py:

This is a Python script that launches a VM and installs a specified app via its .apk file.
It is in an early stage at this point, but it should be a good example for the groundwork:

Usage: python install.py <Path to APK to install>
  Or:  python3 install.py <Path to APK to install> (It is written in Python 3)

1. It currently only finds a single VM to launch and install onto: I will need to do a bit more digging to find out how it needs to be updated for multiple VMs.
2. On launch/install of the Get-Notification app, the user is prompted to give the correct permissions to listen to notifications: we will need to find some way to automate the action of giving that access.
3. There are a few assumptions about what is in your PATH enviornmental variable in order to run the console commands: I can clarify this when we meet in person.
4. The VM is launching w/ the GUI for now just for ease of verifying the installation: will eventually need to revise to launch in headless mode.
