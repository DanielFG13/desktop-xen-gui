import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk

class vmAbout():
    
    builder = None
    window = None
    
    def __init__(self):
        
        self.builder = Gtk.Builder()
        self.builder.add_from_file("/home/josefuentes/finalProjectGenome/interface/about.glade")
        
        self.window = self.builder.get_object("vm-about")    
        self.show()    

        self.builder.connect_signals({
            "on_vm_about_delete_event": self.close,
            "on_vm_about_response": self.close,
            "on_vm_btn_close": self.close,
        })

    ################
    # UI LISTENERS #
    ################

    def show(self):
        self.window.show_all()
        
    def close(self, dialog, response):
        self.window.destroy()