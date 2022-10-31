#!/usr/bin/python3

import netifaces
from gi.repository import Gio


gws = netifaces.gateways()

gateway = gws['default'][netifaces.AF_INET][0]
netmask = netifaces.ifaddresses('xenbr0')[netifaces.AF_INET][0]['netmask']

nat_gateway = "10.0.0.1"
nat_netmask = "255.0.0.0"
nat_bridge = "br"

nameserver = "192.168.1.254"

def create_vm(hostname, disk, ram, vcpus, ip, rootpass, inst_method, dist, network_mode, ip_configutation):
    default = ["/usr/bin/pkexec",
               "/usr/bin/xen-create-image", 
               "--hostname=" + hostname, 
               "--size=" + disk + "GB", 
               "--memory="+ ram + "MB",  
               "--vcpus="+ vcpus, 
               "--password=" + rootpass,
               "--install-method="+ inst_method,
               "--dist="+ dist,
               "--force"]
    add = []
    
    if(ip_configutation == 'static' and network_mode == 'bridge'):
        add.append("--ip="+ ip)
        add.append("--gateway="+ gateway)
        add.append("--netmask="+ netmask)
        add.append("--nameserver="+ nameserver)
    elif(ip_configutation == 'static' and network_mode == 'NAT'):
        add.append("--ip="+ ip)
        add.append("--bridge="+ nat_bridge)
        add.append("--gateway="+ nat_gateway)
        add.append("--netmask="+ nat_netmask)
        add.append("--nameserver="+ nameserver)
    elif(ip_configutation == 'dhcp' and network_mode == 'bridge'): 
        add.append("--dhcp") 
    elif(ip_configutation == 'dhcp' and network_mode == 'NAT'): 
        add.append("--dhcp") 
        add.append("--bridge="+ nat_bridge)
    
    return Gio.Subprocess.new(default + add, 0)