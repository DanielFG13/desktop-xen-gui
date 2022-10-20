#!/usr/bin/python3
import subprocess
import os
import signal

def getAllVirtualMachinesName():
    process = subprocess.Popen(['ls', '/etc/xen'], stdout=subprocess.PIPE)
    print(process.pid)
    stdout = str(process.communicate()[0])[1:].split('\\n')
    process.terminate()
    vms = []
    for file in stdout:
        if '.cfg' in file:
            vms.append(file[0:-4])
    return vms