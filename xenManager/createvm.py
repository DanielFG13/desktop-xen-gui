#!/usr/bin/python
# -*- coding: utf-8 -*-

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
  
############
# CONTANTS #
############

(DEBOOSTRAP,
 CDEBOOSTRAP,
 RINSE,
 TAR) = range(4)


#class Handler:
#    def button_1clicked(self, button):
#      print("Hello GeeksForGeeks using Glade")
  
#builder = Gtk.Builder()
#builder.add_from_file("/home/josefuentes/finalProjectGenome/interface/createvm.glade")
  
#ournewbutton = builder.get_object("inst-method-deb")

#print(ournewbutton.get_active())
  
#window = builder.get_object("vm-create")
  
#window.connect("delete-event", Gtk.main_quit)
#window.show_all()
#Gtk.main()


class VmCreate():
    
    builder = None
    window = None
    
    def __init__(self):
        
        self.builder = Gtk.Builder()
        self.builder.add_from_file("/home/josefuentes/finalProjectGenome/interface/createvm.glade")
        
        self.window = self.builder.get_object("vm-create")    
        self.show()    

        self.builder.connect_signals({
            "on_vmm_newcreate_delete_event": Gtk.main_quit,
            "on_inst_method_changed": self.on_inst_method_changed,
            "on_create_finish_clicked": self.nothing,
            "on_create_forward_clicked": self.nothing,
            "on_create_back_clicked": self.nothing,
            "on_create_cancel_clicked": self.nothing,
            "on_create_pages_switch_page": self.nothing,
            "on_create_pages_switch_page": self.nothing,
            "on_create_vm_name_changed": self.nothing,
        })

################
# UI LISTENERS #
################
    def show(self):
        self.window.show_all()
        
    def close(self):
        self.window.close()


    def on_inst_method_changed(self, widget):
        print(widget)
        is_deboostrap = self.widget("inst-method-deb").get_active()
        is_cdeboostrap = self.widget("inst-method-cdeb").get_active()
        is_rinse = self.widget("inst-method-rinse").get_active()
        is_tar = self.widget("inst-method-tar").get_active()
        if is_deboostrap:
            #set deboostrap method variable
            print(DEBOOSTRAP)
        if is_cdeboostrap:
            #set cdeboostrap method variable
            print(CDEBOOSTRAP)
        if is_rinse:
            #set rinse method variable
            print(RINSE)
        if is_tar:
            #set TAR method variable
            print(TAR)

    def nothing(self, widget):
        print("hello")

