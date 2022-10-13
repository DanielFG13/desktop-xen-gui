import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class AppWindow(Gtk.ApplicationWindow):
    
    builder = None
    main_window = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Here all the widgets and a button to open the second window
        self.builder = Gtk.Builder()
        self.builder.add_from_file("/home/josefuentes/finalProjectGenome/interface/vmPanel.glade")
        self.main_window = self.builder.get_object("vm-manager")
  
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

        self.show()
        
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
        
    def nothing(self, widget):
        print("hello")
            
AppWindow()