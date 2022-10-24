import subprocess

def real_time_data():
    process = subprocess.Popen(["/usr/bin/pkexec", "/usr/lib/xen-4.16/bin/xentop", "--delay=5", "-b", "-f"], stdout=subprocess.PIPE)
    return process

