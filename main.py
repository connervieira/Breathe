# Breathe
# V0LT
# Licensed under the GPLv3
# Version 0.9 

import gi
import threading
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
from gi.repository import Gdk
from gi.repository import Gio
import sys
import random

class Main(Gtk.ApplicationWindow): # This is the class for the main application window. This is the first window shown when launching the application. 
    def __init__(self, app):
        Gtk.Window.__init__(self, title="Breathe", application=app) # This sets the title of the window, and links it to the main application instance.
        self.set_default_size(200, 38)

        def StartBreathing(self): # This function is called to open the berathing exercise window. 
            breathing_window = Breathing()

        self.start_button = Gtk.Button(label="Start") # Create start button.
        self.start_button.connect("clicked", StartBreathing) # Link start button to StartBreathing function.
        self.add(self.start_button) # Add the start button to the interface.
        
        self.show_all() # Show all elements on the interface


class Breathing(Gtk.ApplicationWindow):
    def __init__(self):
        # Create window
        Gtk.Window.__init__(self, title="Breathe") # Set window title
        self.set_default_size(600, 100)
        self.show() # Show window.
    
        self.increment_value = 0 # Initialize increment value variable to be used in the breathing animation later. 

        listbox = Gtk.ListBox() # Create any empty list box to organize UI elements
        self.breathing_bar = Gtk.ProgressBar() # Create a progress bar to visualize breathing.

        listbox.add(self.breathing_bar) # Add the breathing progress bar to the listbox.
        self.add(listbox) # Add the listbox to the interface.

        self.breathing_direction = Gtk.Label() # Create a blank label to show the breathing instructions.
        self.breathing_direction.set_markup("<span font_desc='Lato Light 25'>%s</span>" % "Sit upright somewhere comfortable") # Show the instructions in size 25 font.

        listbox.add(self.breathing_direction) # Add the breathing instructions text to the listbox.

        self.show_all() # Show all elements in the user interface.

        def StartBreathing(): # Called when the guided breathing starts.
            self.timeout_id = GLib.timeout_add(5, self.Animation, None)

        threading.Timer(6.0, StartBreathing).start() # Start the breathing exercises 6 seconds after the window has opened, giving the user time to read the instructions.

    def Animation(self, user_data):
        current_value = self.breathing_bar.get_fraction() # Define current_value as the current progress of the progress bar (0.0 through 1.0)

        if current_value == 0 or current_value == 1: # If the progress bar is either complete, or empty, set the incremental value to 0.
            self.increment_value = 0

        if self.increment_value >= 0:
            self.breathing_direction.set_markup("<span font_desc='Lato Light 40'>%s</span>" % "Breathe in")
        elif self.increment_value < 0:
            self.breathing_direction.set_markup("<span font_desc='Lato Light 40'>%s</span>" % "Breathe out")

        if current_value < 0.5:
            self.increment_value = self.increment_value + 0.000006 # Exponentially speed up until the progress bar passes 50%
        elif current_value >= 0.5:
            self.increment_value = self.increment_value - 0.000006 # Exponentially slow down until the progress bar reaches ~100%, the begin decreasing exponentially

        self.breathing_bar.set_fraction(current_value + self.increment_value) # Apply changes to the breathing progress bar. 
        return True


class MyApplication(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        win = Main(self)
        win.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)

app = MyApplication()
exit_status = app.run(sys.argv)
sys.exit(exit_status)
