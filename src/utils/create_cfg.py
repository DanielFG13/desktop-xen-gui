from gi.repository import Gtk, Gio

#def start_vm(name):
#    proccess = subprocess.Popen(["/usr/bin/pkexec", "/usr/lib/xen-4.16/bin/xl", "create" , "/etc/xen/pruebaxen.cfg"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#    proccess.wait()
#    print(proccess.returncode)
#    return [proccess.returncode]



def start_vm(name):
    proccess = Gio.Subprocess.new(["/usr/bin/pkexec", "/usr/lib/xen-4.16/bin/xl", "create" , "/etc/xen/pruebaxen.cfg"], 0)
    proccess.wait_check_async(None, self._on_update_finished)
    print(proccess.returncode)
    return [proccess.returncode]