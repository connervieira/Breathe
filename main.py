# Breathe
# Conner Vieira - V0LT
# Licensed under the GPLv3
# Version 3.0 


# ----- Configuration -----

# This determines whether the time you spend focusing on breathing will be submitted to HealthBox as "mindful minutes". If this is enabled, then the following HealthBox configuration values must also be set.
config = {
    "healthbox": {
        "enabled": True,
        "endpoint": "https://v0lttech.com/healthbox/submit.php",
        "service_key": "15f0b9dbb9de6770ae0c3cb4"
    },
    "exercise": {
        "time": 60,
        "speed": 1
    }
}

# ----- End Of Configuration -----



# Import required Python modules
import threading
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
import sys
import time
import requests
import json


class Main(Gtk.ApplicationWindow): # This is the class for the main application window. This is the first window shown when launching the application. 
    def __init__(self, app):
        Gtk.Window.__init__(self, title="Breathe", application=app) # This sets the title of the window, and links it to the main application instance.
        self.set_default_size(200, 38*2)

        def StartBreathing(self): # This function is called to open the breathing exercise window. 
            breathing_window = Breathing()
        def EnterConfiguration(self): # This function is called to open the breathing exercise window. 
            configuration_window = Configuration()

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        self.add(vbox)

        self.start_button = Gtk.Button(label="Start") # Create start button.
        self.start_button.connect("clicked", StartBreathing) # Link start button to StartBreathing function.
        vbox.pack_start(self.start_button, True, True, 0)
        self.configure_button = Gtk.Button(label="Configure") # Create configure button.
        self.configure_button.connect("clicked", EnterConfiguration) # Link start button to StartBreathing function.
        vbox.pack_start(self.configure_button, True, True, 0)
        
        self.show_all() # Show all elements on the interface

class Configuration(Gtk.ApplicationWindow):
    def __init__(self):
        # Create window
        Gtk.Window.__init__(self, title="Configuration") # Set window title
        self.set_default_size(400, 200)
        self.set_resizable(False)
        self.show() # Show window.

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)


        hbox = Gtk.Box(spacing=6)
        self.label_healthbox_enabled = Gtk.Label()
        self.label_healthbox_enabled.set_text("HealthBox Enabled: ")
        hbox.pack_start(self.label_healthbox_enabled, True, True, 0)
        self.input_healthbox_enabled = Gtk.Switch()
        self.input_healthbox_enabled.set_active(config["healthbox"]["enabled"])
        self.input_healthbox_enabled.halign = Gtk.Align.CENTER
        hbox.pack_start(self.input_healthbox_enabled, True, True, 0)
        vbox.pack_start(hbox, True, True, 0)

        hbox = Gtk.Box(spacing=6)
        self.label_healthbox_endpoint = Gtk.Label()
        self.label_healthbox_endpoint.set_text("HealthBox Endpoint: ")
        hbox.pack_start(self.label_healthbox_endpoint, True, True, 0)
        self.input_healthbox_endpoint = Gtk.Entry()
        self.input_healthbox_endpoint.set_text(config["healthbox"]["endpoint"])
        hbox.pack_start(self.input_healthbox_endpoint, True, True, 0)
        vbox.pack_start(hbox, True, True, 0)

        hbox = Gtk.Box(spacing=6)
        self.label_healthbox_service = Gtk.Label()
        self.label_healthbox_service.set_text("HealthBox Service: ")
        hbox.pack_start(self.label_healthbox_service, True, True, 0)
        self.input_healthbox_service = Gtk.Entry()
        self.input_healthbox_service.set_text(config["healthbox"]["service_key"])
        hbox.pack_start(self.input_healthbox_service, True, True, 0)
        vbox.pack_start(hbox, True, True, 0)


        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        vbox.pack_start(separator, True, True, 0)

        hbox = Gtk.Box(spacing=6)
        self.label_exercise_time = Gtk.Label()
        self.label_exercise_time.set_text("Exercise Time: ")
        hbox.pack_start(self.label_exercise_time, True, True, 0)
        # TODO: Add slider
        vbox.pack_start(hbox, True, True, 0)

        hbox = Gtk.Box(spacing=6)
        self.label_exercise_speed = Gtk.Label()
        self.label_exercise_speed.set_text("Exercise Speed: ")
        hbox.pack_start(self.label_exercise_speed, True, True, 0)
        self.input_exercise_speed = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0.2, 4, 0.1)
        # TODO: Set value
        hbox.pack_start(self.input_exercise_speed, True, True, 0)
        vbox.pack_start(hbox, True, True, 0)

        self.show_all() # Show all elements on the interface.


class Breathing(Gtk.ApplicationWindow):
    def __init__(self):
        # Create window
        Gtk.Window.__init__(self, title="Breathe") # Set window title
        self.set_default_size(600, 100)
        self.show() # Show window.
        self.connect("destroy", self.on_destroy)
    
        self.increment_value = 0 # Initialize increment value variable to be used in the breathing animation later. 

        listbox = Gtk.ListBox() # Create any empty list box to organize UI elements.
        self.breathing_bar = Gtk.ProgressBar() # Create a progress bar to visualize breathing.

        listbox.add(self.breathing_bar) # Add the breathing progress bar to the listbox.
        self.add(listbox) # Add the listbox to the interface.

        self.breathing_direction = Gtk.Label() # Create a blank label to show the breathing instructions.
        self.breathing_direction.set_markup("<span font_desc='Lato Light 25'>%s</span>" % "Sit upright somewhere comfortable") # Show the instructions in size 25 font.
        listbox.add(self.breathing_direction) # Add the breathing instructions text to the listbox.

        self.show_all() # Show all elements in the user interface.

        def StartBreathing(): # Called when the guided breathing starts.
            self.start_time = int(time.time()) # Save the time when the breathing exercise started to a variable.
            self.timeout_id = GLib.timeout_add(5, self.Animation, None)

        def StopBreathing(): # Called to stop the breathing exercise.
            end_time = int(time.time()) # Save the time when the breathing exercise stopped to a variable.
            GLib.source_remove(self.timeout_id) # Stop the breathing progress bar animation started by StartBreathing()
            self.breathing_bar.set_fraction(0) # Set progress bar to 0. 
            
            if (config["healthbox"]["enabled"] == True):
                submission = "?service=" + config["healthbox"]["service_key"] + "&category=mental&metric=mindful_minutes&key-type_of_mindfulness=breathing&key-start_time=" + str(self.start_time) + "&key-end_time=" + str(end_time)
                full_url = config["healthbox"]["endpoint"] + submission
                response = requests.get(full_url)
                try:
                    response = json.loads(response.text) # Convert the response to JSON.
                    print(response)
                except Exception as e:
                    print("JSON decode error: " + str(e))
                    self.breathing_direction.set_markup("<span font_desc='Lato Light 40'>%s</span>" % "Internal HealthBox error")
                if ("error" in response):
                    self.breathing_direction.set_markup("<span font_desc='Lato Light 40'>%s</span>" % "HealthBox error")
                elif ("success" in response):
                    self.breathing_direction.set_markup("<span font_desc='Lato Light 40'>%s</span>" % "Exercise complete")
                    print("HealthBox success: " + str(response))
                else:
                    self.breathing_direction.set_markup("<span font_desc='Lato Light 40'>%s</span>" % "Unknown HealthBox error")
            else:
                self.breathing_direction.set_markup("<span font_desc='Lato Light 40'>%s</span>" % "Exercise complete!")

        self.start_timer = threading.Timer(6.0, StartBreathing) # Start the breathing exercises 6 seconds after the window has opened, giving the user time to read the instructions.
        self.end_timer = threading.Timer(config["exercise"]["time"] + 6.0, StopBreathing)
        self.start_timer.start()
        self.end_timer.start()

    def Animation(self, user_data):
        current_value = self.breathing_bar.get_fraction() # Define current_value as the current progress of the progress bar (0.0 through 1.0)

        if current_value == 0 or current_value == 1: # If the progress bar is either complete, or empty, set the incremental value to 0.
            self.increment_value = 0

        if self.increment_value >= 0:
            self.breathing_direction.set_markup("<span font_desc='Lato Light 40'>%s</span>" % "Breathe in")
        elif self.increment_value < 0:
            self.breathing_direction.set_markup("<span font_desc='Lato Light 40'>%s</span>" % "Breathe out")

        if current_value < 0.5:
            self.increment_value = self.increment_value + 0.000006 * config["exercise"]["speed"] # Bounce off of the bottom of the progress bar (accelerate upwards).
        elif current_value >= 0.5:
            self.increment_value = self.increment_value - 0.000006 * config["exercise"]["speed"] # Bounce off of the top of the progress bar (accelerate downwards).

        self.breathing_bar.set_fraction(current_value + self.increment_value) # Apply changes to the breathing progress bar. 
        return True

    def on_destroy(self, widget): # This runs when this window is closed.
        self.start_timer.cancel() # Cancel the exercise start trigger.
        self.end_timer.cancel() # Cancel the exercise end trigger.


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
