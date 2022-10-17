from concurrent.futures import process
import threading
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GdkPixbuf

import sys
import os
import signal
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from utils.getVms import *
from utils.xentop import *

class AppWindow(Gtk.ApplicationWindow):
    
    builder = None
    main_window = None
    virtualMachines = None
    real_time_info = None
    is_thread_xentop_running = True

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
                                      "on_vm_run_clicked": self.init_vm_list,
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
        
        self.show()
    
    ################
    # UI LISTENERS #
    ################
      
    def show(self):
        self.main_window.show_all()
        Gtk.main()
        
    def close(self):
        self.main_window.close()
        sys.exit()
    
    def on_menu_help_about_activate(self, widget):
        from about import vmAbout
        vmAbout()
        
    def on_vm_new_clicked(self, widget):
        from createvm import VmCreate
        VmCreate()
        self.is_thread_xentop_running = False
        
    def init_vm_list(self, widget):
        def callback():
            process_xentop = real_time_data() 
            for line in iter(process_xentop.stdout.readline, b''):
                print(line)
                if not self.is_thread_xentop_running:
                    os.killpg(os.getpgid(process_xentop.pid), signal.SIGTERM)
                    break
        thread_xentop = threading.Thread(target=callback)
        thread_xentop.start()

        
    def nothing(self, widget):
        print("hello")
            
AppWindow()