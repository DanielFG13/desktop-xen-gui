from concurrent.futures import process
import subprocess
import os
import signal

def start_vm(name):
    process = subprocess.Popen(["/usr/bin/pkexec", "/usr/lib/xen-4.16/bin/xl", "create" , "/etc/xen/" + name + ".cfg"], stdout=subprocess.PIPE)
    print(process.pid)
    process.communicate()
    process.terminate()
    