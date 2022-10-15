#!/usr/bin/python3

import subprocess
import netifaces

gws = netifaces.gateways()

gateway = gws['default'][netifaces.AF_INET][0]
netmask = netifaces.ifaddresses('xenbr0')[netifaces.AF_INET][0]['netmask']

def create_vm(hostname, disk, ram, swap, vcpus, ip, mac, rootpass, inst_method, dist, vifname):
    proccess = subprocess.Popen(["sudo", "xen-create-image", 
                         "--hostname=" + hostname, 
                         "--size=" + disk + "GB", 
                         "--memory="+ ram + "MB", 
                         "--swap="+ swap + "MB",
                         "--ip=" + ip, 
                         "--vcpus="+vcpus, 
                         "--mac="+mac, 
                         "--vifname="+vifname,
                         "--password=" + rootpass,
                         "--force"])
    streamdata = proccess.communicate()[1]
    print(proccess.returncode, streamdata)
    return [proccess.returncode, streamdata] 

#create_vm("test1", "5", "1024", "20", "1", "192.168.1.151", "00:00:5e:00:53:af", "0", "cdebootstrap", "bullseye", "testvif") 