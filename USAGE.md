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