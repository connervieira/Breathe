# Usage

## Running
### Steps
If you simply want to run Breathe, you can do so by running these steps:

1. Download the git repository and extract it to somewhere on your machine
2. Change into the Breathe directory (Ex: `cd Breathe`)
3. Run main.py (Ex: `python3 main.py`)

### Potential Issues
The following are potential issues you may encounter while trying to run Breathe:
\
\
\
1. You receive an error that Python3 wasn't found.

`python3: command not found`

To solve this issue, install python using your distribution's package manager to install Python3

Ubuntu: `sudo apt install python3`
\
\
\
2. You receive an error that Python is missing a package

`ModuleNotFoundError: No module found named 'xyz'`

All of the modules used by Breathe should be pre-installed, but if one is missing, install it using this command, substituting 'xyz' for the name of the module missing.

`pip3 install xyz`

You may first have to install pip3 using your distribution's package manager.

Ubuntu: `sudo apt install python3-pip`

## Integrating
If you prefer to launch applications from a GUI, you can optionally integrate Breathe with your desktop environment using alacarte.

1. If you haven't installed alacarte (Main Menu), you'll need to do so to integrate Breathe with your desktop environment using this method.

Ubuntu: `sudo apt install alacarte`

2. Run alacarte, either from your desktop environment or the command line.

`alacarte`

3. Select a category to install Breathe to in the left side bar.

4. Select "New Item" on the right.

5. In the Launcher Properties window that appears, enter 'Breathe' in the 'Name' field.

6. In the 'Command' field, enter the command to launch Breathe. Your file path will likely be different than the example below.

`python3 ~/Software/Breathe/main.py`

7. Click the blank icon to the left of the 'Launcher Properties' window, and select 'icon.png' from the Breathe folder.

8. Check the 'Launch In Terminal' box.


## Configuring HealthBox Integration

If you'd like to have Breathe automatically submit information about the time you spend focusing on your Breathing to HealthBox, you'll need to configure it by following these steps.

1. Start HealthBox, and select `Manage API keys` on the main menu.
2. Create a new API key for Breathe using the following command: `c Breathe`
    - It should be noted that the name of the key doesn't necessarily have to be Breathe. You can set it to anything you want.
3. Notice that a new API key has appeared at the top of the interface. Take note of it's number.
4. Edit the API key based on it's number using the following command. The number may be different for your API key. `e 1`
5. Set the API key type to `source` using the following command: `t s`
6. From now on, we'll be working on Breathe, but HealthBox should remain open, so Breathe can communicate with it. Open `main.py` in Breathe.
7. At the top of `main.py`, notice the `Configuration` section.
8. Change `use_healthbox` to `True`
9. Change `healthbox_server` to the server address and port of your HealthBox instance, in the form of `host:port`. For example, if HealthBox is running locally on your machine on the default port, you might enter `localhost:5050`. If you run HealthBox over LAN, you may enter something along the lines of `192.168.0.28:5050`
10. Change `healthbox_apikey` to the API key we created in HealthBox in the earlier steps.
11. Save `main.py`
12. Breathe should now automatically interface with HealthBox. You can test to see if everything works by completing a breathing exercise, then checking the database using the `Import or export database` function built into HealthBox. If you encounter issues, try checking the console window of Breathe to see if any errors appear that could lead you to the cause of the problem.
