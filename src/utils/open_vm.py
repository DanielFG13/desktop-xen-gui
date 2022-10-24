import subprocess

def open_vm(name):
    subprocess.run(["gnome-terminal", "--", "/usr/bin/pkexec", "/usr/lib/xen-4.16/bin/xl", "console" , name], stdout=subprocess.PIPE)