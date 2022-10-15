import subprocess
import os

def start_vm(name):
    proccess = subprocess.Popen(["gnome-terminal", "--", "sudo", "xl", "create", "/etc/xen/pruebaxen.cfg"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    streamdata = proccess.communicate()
    return [proccess.returncode, streamdata]
