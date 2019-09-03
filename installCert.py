import sys
import subprocess

# Edit this value to reflect the correct file location for deployment
CERT = "/home/jthiede/.mitmproxy/mitmproxy-ca-cert.pem"

# getCert = ['charles', 'ssl', 'export', CERT]
getHash = ['openssl', 'x509', '-subject_hash_old', '-in', CERT, '-noout']


# subprocess.Popen(getCert).communicate()
hash = subprocess.Popen(getHash, stdout=subprocess.PIPE).communicate()[0].decode('utf')

hash = hash.strip() + '.0'

print(hash)

with open(hash, 'w+') as f:
    makeFile = ['cat', CERT]
    subprocess.Popen(makeFile, stdout=f)

append = "openssl x509 -in " + CERT + " -noout -text >> " + str(hash)
subprocess.Popen(append, shell=True).communicate()


# Get a list of the currently connected devices to iterate over
listConnected = ['adb', 'devices']
devices = subprocess.Popen(listConnected, stdout=subprocess.PIPE).communicate()[0].decode("utf-8")
deviceList = devices.split()
filteredList = list(filter(lambda x : "emulator" in x, deviceList))

for dev in filteredList:
    root = ['adb', '-s', str(dev), 'root']
    remount = ['adb', '-s', str(dev), 'remount']
    push = ['adb', '-s', str(dev), 'push', str(hash), '/system/etc/security/cacerts']

    subprocess.Popen(root).communicate()
    subprocess.Popen(remount).communicate()
    subprocess.Popen(push).communicate()

# remove1 = ['rm', CERT]
remove2 = ['rm', str(hash)]

# subprocess.Popen(remove1).communicate()
subprocess.Popen(remove2).communicate()

