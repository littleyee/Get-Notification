# NotificationListener


A framework consititing of an Android application which we are using to log information about notifications (of particular interest are push notifications from advertisers) and store them for later analysis, and a number of auxillary Python scripts to facilitate the automation of Android VMs.


## Get-Notification:

Android application which launches a NotificationListenerService to capture all notifications posted to the phone.
Notification title, content, sender, and timestamp are collected and stored in an SQLite database for later analysis.


## install.py:

This is a Python script that looks for a JSON file which specifies configurations for new VMs, then creates and launches them

Inputs: JSON file specifying the test configuration (see example files): Emulator names, locations, hardware profile, system image, .APK files to load. 

Results: VMs are created and initialized according to the configuration given.

Usage: python install.py <Path to JSON file> 


## launch.py:

Python script to launch all VMs associated with a specified configuration/test.

Inputs: JSON file used to initialize the test (same in as install.py)

Results: All VMs specified in the config file are launched. 

Usage: python launch.py <Path to JSON file>
  
  
## loadGN.py:

Script to install the Notificaiton listener app onto all currently running VMs and automates all necessary screen inputs to accept the necessary permissions for the app to collect notifications.

Results: The GetNotificaiton app is installed onto all VMs and is ready to collect notifications

Usage: python loadGN.py


## installCert.py

Script to correctly format and push the MITMProxy CA cert into the "System trusted" CA certs of all currently running VMs

Results: MITMProxy certificate is registered as system trusted on all VMs; MITMProxy can now observe HTTPS traffic.

Usage: python installCert.py

## pullDB.py

Script to pull the SQLite databases from running VMs and compile them into a single .sql file. Intended for use as a daily recurring job (Linux crontab job).

Inputs: Config file for current test (used to ID devices/get location), path to location to save .sql file to.

Outputs: .sql file compiling each notification posted to each VM in the past 24 hours.

Usage: N/A; (For usage as a crontab job. Ex: 59 23 * * * /usr/bin/python /path/to/pullDB.py /path/to/configfile /path/to/save/location)
