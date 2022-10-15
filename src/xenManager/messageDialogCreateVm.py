from email import message
import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, GObject
import os
from threading import Thread

class crateVmMessageDialog():
    
    builder = None
    window = None
    btn_close = None
    
    def __init__(self, vm_name):
        
        self.builder = Gtk.Builder()
        self.builder.add_from_file(os.getcwd() + "/src/interface/messageDialogCreateVm.glade")
        
        self.window = self.builder.get_object("message-create-vm")   
        self.btn_close = self.builder.get_object("createvm-dialog-btn-close")   
        self.window.format_secondary_text("Creating vm " + vm_name + ". This task can take several minutes")
        
        self.show()  
        
        self.builder.connect_signals({
            "on_dialog_btn_close": self.close,
        })  

    def update_message(self, message):
        self.window.format_secondary_text(message)

    ################
    # UI LISTENERS #
    ################

    def show(self):
        self.window.show_all()
        
    def close(self, widget):
        self.window.destroy()
        
        