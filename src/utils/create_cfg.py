import subprocess

def start_vm(name):
    process = subprocess.Popen(["/usr/bin/pkexec", "/usr/lib/xen-4.16/bin/xl", "create" , "/etc/xen/" + name + ".cfg"], stdout=subprocess.PIPE)
    process.communicate()[0]
    return process.returncode
    