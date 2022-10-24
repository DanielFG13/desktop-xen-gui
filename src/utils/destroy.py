from gi.repository import Gio

def destroy_vm(name):
    return Gio.Subprocess.new(["/usr/bin/pkexec", "/usr/lib/xen-4.16/bin/xl", "destroy" , name], 0)