import subprocess
import os

def destroy_vm(name):
    subprocess.run(["/usr/bin/pkexec", "/usr/lib/xen-4.16/bin/xl", "destroy" , name], stdout=subprocess.PIPE)