from concurrent.futures import process
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GdkPixbuf

import sys
import os
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from utils.getVms import *

class AppWindow(Gtk.ApplicationWindow):
    
    builder = None
    main_window = None
    virtualMachines = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Here all the widgets and a button to open the second window
        self.builder = Gtk.Builder()
        self.builder.add_from_file(os.getcwd() + "/src/interface/vmPanel.glade")
        self.main_window = self.builder.get_object("vm-manager")
        
        self.vm_list = self.builder.get_object("vm-list")
  
        self.builder.connect_signals({
                                      "on_menu_help_about_activate": self.on_menu_help_about_activate,
                                      "on_vm_manager_configure_event": self.nothing,
                                      "on_menu_file_add_connection_activate": self.nothing,
                                      "on_vm_manager_delete_event": Gtk.main_quit,
                                      "on_vm_list_button_press_event": self.nothing,
                                      "on_vm_list_key_press_event": self.nothing,
                                      "on_vm_list_row_activated": self.nothing,
                                      "on_vm_shutdown_clicked": self.nothing,
                                      "on_vm_pause_clicked": self.nothing,
                                      "on_vm_run_clicked": self.nothing,
                                      "on_vm_open_clicked": self.nothing,
                                      "on_vm_new_clicked": self.on_vm_new_clicked,
                                      
                                      "on_menu_view_network_traffic_activate": self.nothing,
                                      "on_menu_view_disk_io_activate": self.nothing,
                                      "on_menu_view_memory_usage_activate": self.nothing,
                                      "on_menu_view_host_cpu_usage_activate": self.nothing,
                                      
                                      "on_menu_view_guest_cpu_usage_activate": self.nothing,
                                      "on_menu_edit_preferences_activate": self.nothing,
                                      "on_menu_edit_delete_activate": self.nothing,
                                      "on_menu_edit_details_activate": self.nothing,
                                      
                                      "on_menu_host_details_activate": self.nothing,
                                      "on_menu_file_quit_activate": self.nothing,
                                      "on_menu_file_close_activate": self.nothing,
                                      "on_menu_new_vm_activate": self.nothing,
                                    })
        
        self.init_vm_list()
        self.show()
    
    ################
    # UI LISTENERS #
    ################
      
    def show(self):
        self.main_window.show_all()
        Gtk.main()
        
    def close(self):
        self.main_window.close()
    
    def on_menu_help_about_activate(self, widget):
        from about import vmAbout
        vmAbout()
        
    def on_vm_new_clicked(self, widget):
        from createvm import VmCreate
        VmCreate()
        
    def init_vm_list(self):
        self.get_vms_list()
        print(self.virtualMachines)
   
    def get_vms_list(self): 
        process = getVirtualMachineList() 
        stdout = process.communicate()[1].get_data()
        cadena = str(stdout)
        data = " ".join(cadena.split()).split("\\n")[1:-1]
        all_vms = getAllVirtualMachinesName()
        active_vms = []
        self.virtualMachines = []
        for i in data:
            vmInfo = i.split(" ")
            state = ''
            if('r' in vmInfo[4]):
                state = 'running'
            if('b' in vmInfo[4]):
                state = 'blocked'
            if('p' in vmInfo[4]):
                state = 'paused'
            if('s' in vmInfo[4]):
                state = 'shutdown'
            if('c' in vmInfo[4]):
                state = 'crashed'
            if('d' in vmInfo[4]):
                state = 'dying'
            active_vms.append([ vmInfo[0] ])
            self.virtualMachines.append([ vmInfo[0], state ])
            
        for vm in all_vms:
            if(vm not in active_vms):
                self.virtualMachines.append([vm, "shutdown"])
              
    def nothing(self, widget):
        print("hello")
            
AppWindow()