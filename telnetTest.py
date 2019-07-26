import sys
import telnetlib
import time

# A somewhat roundabout way to get the emulator name back
# Unfortunately the command 'adb emu avd name' is not printing back output to console on the server, so this is the current workaround

HOST = 'localhost'
PORT = '5554'
# Change this to correct authentication token
AUTH = '555KjfyUBwIiO+h4'

tel = telnetlib.Telnet(HOST, PORT)

time.sleep(1)

output = tel.read_very_eager()

print(str(output))

tel.write('auth ' + AUTH + '\n')
time.sleep(1)
tel.write("avd name + \n")
time.sleep(1)
output =  tel.read_very_eager()

print(str(output))
