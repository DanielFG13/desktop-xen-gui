import threading
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

import sys
import os
import signal
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from utils.getVms import *
from utils.xentop import *
from utils.create_cfg import *
from utils.destroy import *
from utils.open_vm import *

class AppWindow(Gtk.ApplicationWindow):
    
    builder = None
    main_window = None
    virtualMachines = None
    real_time_info = None
    is_thread_xentop_running = True
    vm_list = None
    list_store = None
    selected_vm = None
    tree_iterations = {}
    vms = None
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Here all the widgets and a button to open the second window
        self.builder = Gtk.Builder()
        self.builder.add_from_file(os.getcwd() + "/src/interface/vmPanel.glade")
        self.main_window = self.builder.get_object("vm-manager")
        
        self.vm_list = self.builder.get_object("vm-list")
        
        self.list_store = Gtk.ListStore(str, str, str, str, str, str)
        self.vms = getAllVirtualMachinesName()
        self.vms.insert(0, 'Domain-0')
        
        self.vm_list.set_model(self.list_store)

        for vm in self.vms:
            state = ''
            if(vm == 'Domain-0'):
                state = 'running'
            else:
                state = 'shutdown'    
            treeiter = self.list_store.append([vm, state, 'N/A', 'N/A', 'N/A', 'N/A'])
            self.tree_iterations[vm] = treeiter
        
        for i, column_title in enumerate(
            ["Domains", "STATE", "CPU(sec)", "CPU(%)",  "Memory(kb)", "Memory(%)"]
        ):
            if column_title == "Domains":
                renderer = Gtk.CellRendererText()
                column = Gtk.TreeViewColumn(column_title, renderer, text=i)
                column.set_fixed_width(200)
            else:
                renderer = Gtk.CellRendererText()
                column = Gtk.TreeViewColumn(column_title, renderer, text=i)
                column.set_fixed_width(100)
            self.vm_list.append_column(column)
        
  
        self.builder.connect_signals({
                                      "on_menu_help_about_activate": self.on_menu_help_about_activate,
                                      "on_vm_manager_configure_event": self.nothing,
                                      "on_menu_file_add_connection_activate": self.nothing,
                                      "on_vm_manager_delete_event": self.on_vm_manager_delete_event,
                                      "on_vm_list_button_press_event": self.nothing,
                                      "on_vm_list_key_press_event": self.nothing,
                                      "on_vm_list_row_activated": self.on_vm_list_row_activated,
                                      "on_vm_shutdown_clicked": self.stop_virtual_machine,
                                      "on_vm_run_clicked": self.start_virtual_machine,
                                      "on_vm_open_clicked": self.open_virtual_machine,
                                      "on_vm_new_clicked": self.on_vm_new_clicked,
                                      "on_vm_monitor_clicked": self.monitor_vm_list,
                                      
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
      
    def on_vm_manager_delete_event(self, widget, event):
        self.is_thread_xentop_running = False
        Gtk.main_quit()  
        
    def close(self):
        self.main_window.close()
        sys.exit(0)
    
    def on_menu_help_about_activate(self, widget):
        from about import vmAbout
        vmAbout()
        
    def on_vm_new_clicked(self, widget):
        from createvm import VmCreate
        VmCreate()
                
    def on_vm_list_row_activated(self, treeview, path, column):
        model = treeview.get_model()
        treeiter = model.get_iter(path)
        self.selected_vm = model.get_value(treeiter, 0)
        print(self.selected_vm)
    
    def start_virtual_machine(self, widget):
        vm = self.selected_vm
        if(vm == None):
            return
        if(not(vm == 'Domain-0') and (self.list_store.get_value(self.tree_iterations[vm], 1) == 'shutdown')):
            start_vm(self.selected_vm)
            
    def stop_virtual_machine(self, widget):
        vm = self.selected_vm
        if(vm == None):
            return
        if(not(vm == 'Domain-0') and not(self.list_store.get_value(self.tree_iterations[vm], 1) == 'shutdown')):
            process = destroy_vm(self.selected_vm)
            process.wait_check_async(None, self._on_destroy_finished)
    
    def _on_destroy_finished(self, subprocess, result):
        subprocess.wait_check_finish(result)
        self.list_store.set_row(self.tree_iterations[self.selected_vm], [self.selected_vm, 'shutdown', 'N/A', 'N/A', 'N/A', 'N/A'])
        
    def open_virtual_machine(self, widget):
        vm = self.selected_vm
        if(vm == None):
            return
        if(not(vm == 'Domain-0') and not(self.list_store.get_value(self.tree_iterations[vm], 1) == 'shutdown')):
            open_vm(self.selected_vm)
        
    def monitor_vm_list(self, widget):
        def callback():
            process_xentop = real_time_data() 
            print(process_xentop.pid)
            for line in iter(process_xentop.stdout.readline, b''):
                raw_data = " ".join(str(line).replace('b\'', '').split()).split(" ")
                data = raw_data[0:6]
                data[1] = self.state_word(data[1])
                if(data[0] == 'NAME'):
                    continue
                if(not (data[0] in self.vms)):
                    continue
                GLib.idle_add(self.update_tree_view, data)
                if not self.is_thread_xentop_running:
                    os.killpg(os.getpgid(process_xentop.pid), signal.SIGKILL)
                    break
        thread_xentop = threading.Thread(target=callback)
        thread_xentop.start()

    def update_tree_view(self, data):
        self.list_store.set_row(self.tree_iterations[data[0]], data)

    def state_word(self, state):
        if('r' in state):
            return 'running'
        if('b' in state):
            return 'blocked'
        if('p' in state):
            return 'paused'
        if('s' in state):
            return 'shutdown'
        if('c' in state):
            return 'crashed'
        if('d' in state):
            return 'dying'
    
    def nothing(self, widget):
        print("hello")
            
AppWindow()

#nameserver 2806:1020:ffff:3::2
#nameserver 2806:1030:ffff:2::e
