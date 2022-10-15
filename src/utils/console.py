import subprocess

def open_vm(name):
    proccess = subprocess.Popen(["gnome-terminal", "--", "sudo", "xl", "console", "pruebaxen"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    streamdata = proccess.communicate()
    print(proccess.returncode, streamdata)
    return [proccess.returncode, streamdata]