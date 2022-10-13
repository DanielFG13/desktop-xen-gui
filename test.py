import gi
import subprocess

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class MyWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Hello World")

        self.button = Gtk.Button(label="Click Here")
        self.button.connect("clicked", self.on_button_clicked)
        self.add(self.button)

    def on_button_clicked(self, widget):
        #subprocess.run(["gnome-terminal", "--", "sudo", "xl", "console", "pruebaxen"])
        result = subprocess.run(["gnome-terminal", "--","sudo", "xen-create-image", "--hostname=testmv1", 
                         "--size=10GB", "--memory=1024MB", "--swap=20MB",
                         "--ip=192.168.1.150", "--vcpus=1","--password=0", "--force"])
        print(result)

win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

import os

print("path", os.getcwd())