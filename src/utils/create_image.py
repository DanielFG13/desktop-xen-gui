#!/usr/bin/python3

import netifaces
from gi.repository import Gio


gws = netifaces.gateways()

gateway = gws['default'][netifaces.AF_INET][0]
netmask = netifaces.ifaddresses('xenbr0')[netifaces.AF_INET][0]['netmask']

def create_vm(hostname, disk, ram, swap, vcpus, ip, mac, rootpass, inst_method, dist, vifname):
    return Gio.Subprocess.new(["/usr/bin/pkexec",
                               "/usr/bin/xen-create-image", 
                                "--hostname=" + hostname, 
                                "--size=" + disk + "GB", 
                                "--memory="+ ram + "MB", 
                                "--swap="+ swap + "MB",
                                "--ip=" + ip, 
                                "--vcpus="+ vcpus, 
                                "--mac="+ mac, 
                                "--vifname="+ vifname,
                                "--password=" + rootpass,
                                "--install-method="+ inst_method,
                                "--dist="+ dist,
                                "--gateway="+ gateway,
                                "--netmask="+ netmask,
                                "--force"], 0)

