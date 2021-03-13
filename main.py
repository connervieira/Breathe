# Breathe
# V0LT
# Licensed under the GPLv3
# Version 2.0 


# ----- Configuration -----

# Defines whether or not you'd like to submit the time you spend breathing to HealthBox as 'Mindful Minutes' (Metric B6). If this setting is changed, you'll need to configure your HealthBox instance information below.
use_healthbox = False

# Defines the host address and port that you host HealthBox on. If you're running HealthBox locally on it's default port, it will be 'localhost:5050'
healthbox_server = "localhost:5050"

# This is the API key that Breathe will use to communicate with HealthBox. This key needs to have 'source' permissions, and be allowed to access metric B6 (Mindful Minutes)
healthbox_apikey = ""

# This variable determines whether or not the URL will be printed when making the network request to HealthBox. This is extremely useful for debugging, but can be messy during normal usage. This should be left as 'False' if you aren't a developer.
url_debugging = False

# ----- End Of Configuration -----



# Import required Python modules
import gi
import threading
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
from gi.repository import Gdk
from gi.repository import Gio
import sys
import random
from datetime import datetime
import traceback
import urllib.parse


# Attempt to import the 'requests' module
try:
    import requests
except ModuleNotFoundError as error:
    if traceback.format_exception_only (ModuleNotFoundError, error) != ["ModuleNotFoundError: No module named 'requests'\n"]: # Make sure the error we're catching is the right one
        raise # If not, raise the error
    raise utils.MissingLibraryError ("making web server requests", "requests")



# Define the function required to make network requests to HealthBox
class APICallError (Exception): pass # This will be used when returning errors.

def make_request (*, server, api_key, submission = None, print_url = False):
    endpoint = "metrics/b6/submit".split ('/') # Define the method and metric that this request will use on HealthBox.
    url = f"http://{server}/api/source/{'/'.join (endpoint)}?api_key={urllib.parse.quote (api_key)}" # Form the URL that will be used to communicate with HealthBox
    if submission is not None:
        url += f"&submission={urllib.parse.quote (submission)}" # Attach the JSON submission data to the URL formed above.
    if print_url: print (f"Making a request to {url}")
    response = requests.get (url) # Send the network request.
    response_data = response.json () # Save the response of the network request to the response_data variable.
    if not response_data ["success"]: # If something goes wrong, return an error.
        raise APICallError (response_data ["error"])
    del response_data ["success"]
    del response_data ["error"]
    return response_data




class Main(Gtk.ApplicationWindow): # This is the class for the main application window. This is the first window shown when launching the application. 
    def __init__(self, app):
        Gtk.Window.__init__(self, title="Breathe", application=app) # This sets the title of the window, and links it to the main application instance.
        self.set_default_size(200, 38)

        def StartBreathing(self): # This function is called to open the breathing exercise window. 
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

        listbox = Gtk.ListBox() # Create any empty list box to organize UI elements.
        self.breathing_bar = Gtk.ProgressBar() # Create a progress bar to visualize breathing.

        listbox.add(self.breathing_bar) # Add the breathing progress bar to the listbox.
        self.add(listbox) # Add the listbox to the interface.

        self.breathing_direction = Gtk.Label() # Create a blank label to show the breathing instructions.
        self.breathing_direction.set_markup("<span font_desc='Lato Light 25'>%s</span>" % "Sit upright somewhere comfortable") # Show the instructions in size 25 font.

        listbox.add(self.breathing_direction) # Add the breathing instructions text to the listbox.

        self.show_all() # Show all elements in the user interface.

        def StartBreathing(): # Called when the guided breathing starts.
            self.start_time = int(datetime.timestamp(datetime.now())) # Save the time when the breathing exercise started to a variable.
            self.timeout_id = GLib.timeout_add(5, self.Animation, None)

        def StopBreathing(): # Called to stop the breathing exercise.
            end_time = int(datetime.timestamp(datetime.now())) # Save the time when the breathing exercise stopped to a variable.
            GLib.source_remove(self.timeout_id) # Stop the breathing progress bar animation started by StartBreathing()
            self.breathing_direction.set_markup("<span font_desc='Lato Light 40'>%s</span>" % "Good job!") # Display "Good job" message
            self.breathing_bar.set_fraction(0) # Set progress bar to 0. 
            
            if (use_healthbox == True):

                if (healthbox_server == ""): # Check to see if the user has entered a server address and port. If not, display an error.
                    print("Error: You've configured Breathe to use HealthBox, but you haven't entered the server address of your HealthBox instance. Please do so in the configuration at the top of 'main.py'.")

                elif (healthbox_apikey == ""): # Check to see if the user has entered an API key. If not, display an error.
                    print("Error: You've configured Breathe to use HealthBox, but you haven't entered an API key for Breathe to use. Please do so in the configuration at the top of 'main.py'.")

                else: # If the user has entered an API key and server address, attempt to submit the breathing session to HealthBox.

                    # Generate the submission data as plain text JSON data.
                    submission = '{"timestamp": ' + str(end_time) + ', "data": {"type_of_mindfulness": "Breathing", "start_time": ' + str(self.start_time) + ', "end_time": ' + str(end_time) + '}}'

                    # Form and send the network request that will be used to submit the information to HealthBox using the make_request function.
                    response = make_request (server = healthbox_server, submission = submission, api_key = healthbox_apikey, print_url = url_debugging)



        threading.Timer(6.0, StartBreathing).start() # Start the breathing exercises 6 seconds after the window has opened, giving the user time to read the instructions.
        threading.Timer(67.0, StopBreathing).start() # Stop breathing exercises after 67 seconds (62 seconds of breathing plus the 5 second timer above).

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
