#!/usr/bin/python3
print()

import subprocess
from gi.repository import Gio

def getAllVirtualMachinesName():
    list_of_files = subprocess.run(['ls', '/etc/xen'], capture_output=True, text=True)
    vms = []
    for file in list_of_files.stdout.split('\n'):
        if '.cfg' in file:
            vms.append(file[0:-4])
    return vms

    
    
