from gi.repository import Gio

def start_vm(name):
    return Gio.Subprocess.new(["/usr/bin/pkexec", "/usr/lib/xen-4.16/bin/xl", "create" , "/etc/xen/pruebaxen.cfg"], 0)
    