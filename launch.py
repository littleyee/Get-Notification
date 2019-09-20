import sys
import subprocess
import json

# Take as input the JSON file used for installation
# Using this just for the emulator names (for launching)
inp = sys.argv[1]

# Open and load JSON
with open(inp) as f:
    jsonList = json.loads(f.read())

# Iterate through JSON objects
# Launch emulators by name
for device in jsonList:
    launch = ['emulator-headless', '-avd', str(device['name']), '-gpu', 'off', -'noaudio', 'writable-system']
    subprocess.Popen(launch)





