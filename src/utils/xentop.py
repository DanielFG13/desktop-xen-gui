import subprocess
from gi.repository import Gio

def real_time_data():
    process = subprocess.Popen(["/usr/bin/pkexec", "/usr/lib/xen-4.16/bin/xentop", "--delay=3", "-b"], stdout=subprocess.PIPE, bufsize=0)
    return process

