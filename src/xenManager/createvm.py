#!/usr/bin/python
# -*- coding: utf-8 -*-

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
  
import sys
import os
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from utils.system_info import * 
from utils.create_image import *
from utils.create_cfg import *

############
# CONTANTS #
############

DIST_DEBIAN_BUSTER = "Debian 10.0 -- Buster"
DIST_DEBIAN_BULLSEYE = "Debian 11.0 -- Bullseye"
DIST_UBUNTU_COSMIC = "Ubuntu 18.10 -- Comic"
DIST_UBUNTU_EOAN = "Ubuntu 19.10 -- Eoan"

class VmCreate():
    
    window = None
    builder = None
    header_pagenum = None
    notebook = None
    mirror_combobox = None
    txt_uri_file = None
    ram_label = None
    cpu_label = None
    memory_label = None
    
    #user selection/input
    method = 'deboostrap'
    tar_file_path = None
    dist = DIST_DEBIAN_BULLSEYE
    ram = None
    cpus = None
    disk = None
    swap = None
    ip = None
    mac = None
    vif_name = None
    name = None
    root_passwd = None
    
    
    def __init__(self):
        
        self.builder = Gtk.Builder()
        self.builder.add_from_file(os.getcwd() + "/src/interface/createvm.glade")
        
        self.window = self.builder.get_object("vm-create")  
        
        self.header_pagenum = self.builder.get_object("header-pagenum") 
        
        self.notebook = self.builder.get_object("create-pages")
        
        self.header_pagenum.set_label("Step " + str(self.notebook.get_current_page() + 1) + " of " + str(self.notebook.get_n_pages()))
        
        self.txt_uri_file = self.builder.get_object("uri-file")
        
        self.dom0_root_passwd_entry = self.builder.get_object("dom0-root-pass")
        
        self.mirror_combobox = self.builder.get_object("install-url-combo")
        liststore = Gtk.ListStore(str)
        liststore.append([DIST_DEBIAN_BULLSEYE])
        liststore.append([DIST_DEBIAN_BUSTER])
        liststore.append([DIST_UBUNTU_EOAN])
        liststore.append([DIST_UBUNTU_COSMIC])
        self.mirror_combobox.set_model(liststore)
        self.mirror_combobox.set_entry_text_column(0)
        self.mirror_combobox.set_active(0)
        
        self.ram_label = self.builder.get_object("ram-label")
        self.cpu_label = self.builder.get_object("cpu-label")
        self.memory_label = self.builder.get_object("memory-label")
        
        self.ram_label.set_text("Dom0 free RAM memory: " + str(get_ram_mb()) + " MB")
        self.cpu_label.set_text("Dom0 number of cpus: " + str(get_cpus()))
        self.memory_label.set_text("Dom0 disk memory: " + str(get_disk_memory_gb()) + " GB")
                
        self.show()    

        self.builder.connect_signals({
            "on_vmm_newcreate_delete_event": Gtk.main_quit,
            
            "on_inst_method_changed": self.on_inst_method_changed,
            
            "on_create_finish_clicked": self.on_create_finish_clicked,
            "on_create_forward_clicked": self.on_create_forward_clicked,
            "on_create_back_clicked": self.on_create_back_clicked,
            "on_create_cancel_clicked": self.close,
            "on_create_pages_switch_page": self.on_create_pages_switch_page,
            
            "on_tar_file_set": self.on_tar_file_set,
            "on_combobox_changed": self.on_combobox_changed,
            
            "on_ram_spin_number_change": self.on_ram_spin_number_change,
            "on_cpus_spin_number_change": self.on_cpus_spin_number_change,
            "on_disk_spin_number_change": self.on_disk_spin_number_change,
            "on_swap_spin_number_change": self.on_swap_spin_number_change,
            
            "on_change_ip_entry": self.on_change_ip_entry,
            "on_change_mac_entry": self.on_change_mac_entry,
            "on_change_vif_entry": self.on_change_vif_entry,
            
            "on_change_name_entry": self.on_change_name_entry,
            "on_change_rootpasswd_entry": self.on_change_rootpasswd_entry,
        })

################
# UI LISTENERS #
################

    def show(self):
        self.window.show_all()
        
    def close(self, widget):
        self.window.close()

    def on_inst_method_changed(self, widget):
        if widget.get_active():
            self.method = widget.get_label()
            
    def on_create_pages_switch_page(self, notebook, widget, page_num):
        self.header_pagenum.set_label("Step " + str(page_num + 1) + " of " + str(notebook.get_n_pages()))
    
    def on_create_back_clicked(self, widget):
        current_page = self.notebook.get_current_page()
        if(current_page > 0):
            self.notebook.set_current_page(current_page - 1)
    
    def on_create_forward_clicked(self, widget):
        current_page = self.notebook.get_current_page()
        if(current_page < self.notebook.get_n_pages() - 1):
            self.notebook.set_current_page(current_page + 1)
    
    def on_tar_file_set(self, widget):
        self.tar_file_path = widget.get_uri()
        self.txt_uri_file.set_text(self.tar_file_path)

    def on_combobox_changed(self, combobox):
        treeiter = combobox.get_active_iter()
        model = combobox.get_model()
        if(model[treeiter][0] == DIST_DEBIAN_BULLSEYE):
            self.dist = 'bullseye'
        if(model[treeiter][0] == DIST_DEBIAN_BUSTER):
            self.dist = 'buster'
        if(model[treeiter][0] == DIST_UBUNTU_COSMIC):
            self.dist = 'cosmic'
        if(model[treeiter][0] == DIST_UBUNTU_EOAN):
            self.dist = 'eoan'

    def on_ram_spin_number_change(self, widget):
        self.ram = str(int(widget.get_value())) 
        
    def on_cpus_spin_number_change(self, widget):
        self.cpus = str(int(widget.get_value())) 
        
    def on_disk_spin_number_change(self, widget):
        self.disk = str(int(widget.get_value())) 
        
    def on_swap_spin_number_change(self, widget):
        self.swap = str(int(widget.get_value())) 

    def on_change_ip_entry(self, widget): 
        self.ip = widget.get_text()
        
    def on_change_mac_entry(self, widget): 
        self.mac = widget.get_text()
        
    def on_change_vif_entry(self, widget): 
        self.vif = widget.get_text()
        
    def on_change_name_entry(self, widget):
        self.name = widget.get_text()

    def on_change_rootpasswd_entry(self, widget):
        self.root_passwd = widget.get_text()

    def on_create_finish_clicked(self, widget):
        from messageDialogCreateVm import crateVmMessageDialog
        dialog = crateVmMessageDialog(self.name)
        start_vm("pruebaxen")
        dialog.update_message("Virtual machine created.")
        
        

