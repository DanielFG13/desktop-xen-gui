#!/usr/bin/python
# -*- coding: utf-8 -*-

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
  
############
# CONTANTS #
############

DEBIAN_MIRROR = "http://httpredir.debian.org/debian/"
UBUNTU_MIRROR = "http://archive.ubuntu.com/ubuntu/"

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
    url_mirror = DEBIAN_MIRROR
    ram = None
    cpus = None
    disk = None
    swap = None
    
    def __init__(self):
        
        self.builder = Gtk.Builder()
        self.builder.add_from_file("/home/josefuentes/finalProjectGenome/interface/createvm.glade")
        
        self.window = self.builder.get_object("vm-create")  
        
        self.header_pagenum = self.builder.get_object("header-pagenum") 
        
        self.notebook = self.builder.get_object("create-pages")
        
        self.header_pagenum.set_label("Step " + str(self.notebook.get_current_page() + 1) + " of " + str(self.notebook.get_n_pages()))
        
        self.txt_uri_file = self.builder.get_object("uri-file")
        
        self.mirror_combobox = self.builder.get_object("install-url-combo")
        liststore = Gtk.ListStore(str)
        liststore.append([DEBIAN_MIRROR])
        liststore.append([UBUNTU_MIRROR])
        self.mirror_combobox.set_model(liststore)
        self.mirror_combobox.set_entry_text_column(0)
        self.mirror_combobox.set_active(0)
        
        self.ram_label = self.builder.get_object("ram-label")
        self.cpu_label = self.builder.get_object("cpu-label")
        self.memory_label = self.builder.get_object("memory-label")
        
        #IMPORTS
        #self.ram_label.set_text("Dom0 free RAM memory: " + SystemInfo.get_ram_mb() + " MB")
        #self.cpu-label.set_text("Dom0 number of cpus: " + SystemInfo.get_cpus())
        #self.cpu-label.set_text("Dom0 disk memory: " + SystemInfo.get_disk_memory() + " GB")
        
        self.show()    

        self.builder.connect_signals({
            "on_vmm_newcreate_delete_event": Gtk.main_quit,
            "on_inst_method_changed": self.on_inst_method_changed,
            "on_create_finish_clicked": self.nothing,
            "on_create_forward_clicked": self.on_create_forward_clicked,
            "on_create_back_clicked": self.on_create_back_clicked,
            "on_create_cancel_clicked": self.close,
            "on_create_pages_switch_page": self.on_create_pages_switch_page,
            "on_create_vm_name_changed": self.nothing,
            "on_tar_file_set": self.on_tar_file_set,
            "on_combobox_changed": self.on_combobox_changed,
            "on_ram_spin_number_change": self.on_ram_spin_number_change,
            "on_cpus_spin_number_change": self.on_cpus_spin_number_change,
            "on_disk_spin_number_change": self.on_disk_spin_number_change,
            "on_swap_spin_number_change": self.on_swap_spin_number_change
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
        if(model[treeiter][0] == DEBIAN_MIRROR):
            self.url_mirror = DEBIAN_MIRROR
        if(model[treeiter][0] == UBUNTU_MIRROR):
            self.url_mirror = UBUNTU_MIRROR

    def on_ram_spin_number_change(self, widget):
        self.ram = str(int(widget.get_value())) 
        
    def on_cpus_spin_number_change(self, widget):
        self.cpus = str(int(widget.get_value())) 
        
    def on_disk_spin_number_change(self, widget):
        self.disk = str(int(widget.get_value())) 
        
    def on_swap_spin_number_change(self, widget):
        self.swap = str(int(widget.get_value())) 

    def nothing(self, widget):
        print('hello')

