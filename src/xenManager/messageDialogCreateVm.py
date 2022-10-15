from email import message
import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
import os

class crateVmMessageDialog():
    
    builder = None
    window = None
    spinner = None
    message = None
    
    def __init__(self, message):
        self.message = message
        self.builder = Gtk.Builder()
        self.builder.add_from_file(os.getcwd() + "/src/interface/messageDialogCreateVm.glade")
        
        self.window = self.builder.get_object("message-create-vm")   
        self.btn_close = self.builder.get_object("createvm-dialog-btn-close")   
        self.window.format_secondary_text(self.message)
        self.spinner = self.builder.get_object("loading-spinner1") 
    
        self.show()  
        
    ##################
    # UPDATE METHODS #
    ##################

    def update_message(self, message):
        self.message = message
        self.window.format_secondary_text(message)

    def set_spinner_animation(self, animation):
        if(animation):
            self.spinner.start()
        else:
            self.spinner.destroy()
            
    ################
    # UI LISTENERS #
    ################

    def show(self):
        self.window.show_all()
        
    def close(self, widget):
        self.window.destroy()