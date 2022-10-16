#!/usr/bin/python3
print()

import subprocess
from gi.repository import Gio
import time

def getAllVirtualMachinesName():
    list_of_files = subprocess.run(['ls', '/etc/xen'], capture_output=True, text=True)
    vms = []
    for file in list_of_files.stdout.split('\n'):
        if '.cfg' in file:
            vms.append(file[0:-4])
    return vms

def getVirtualMachineList():
    flags = Gio.SubprocessFlags.STDOUT_PIPE
    return Gio.Subprocess.new(["/usr/bin/pkexec", "/usr/lib/xen-4.16/bin/xl", "list"], flags)
    
    
