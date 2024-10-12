# Documentation

## Installation

1. Install system dependencies
    - `sudo apt install python3 python3-pip`
2. Download and extract Breathe to a directory on your system.
3. Optionally, integrate Breathe with your desktop environment using a tool like Alacarte.
    - This step is not required, but might be useful if you'd prefer to launch Breathe from a graphical interface.

## Configuration

Once you've installed Breathe, you may want to configure it to better fit your preferences.

1. Start Breathe using Python 3.
    - Example: `python3 ~/Software/Breathe/main.py`
2. After the interface opens, press the "Configure" button.
3. Make configuration changes as desired.
    - **HealthBox Enabled**: This is a toggle that determines whether Breathe will submit your breathing sessions as "mindful minutes" to a HealthBox instance.
    - **HealthBox Endpoint**: This determines the endpoint Breathe will use to submit information to HealthBox. If you use a self-hosted HealthBox instance, you should update this value to point to its `submit.php` endpoint.
    - **HealthBox Service**: The determines the HealthBox service key that Breathe will use to authenticate with HealthBox. This key is generated in your HealthBox instance, and should be granted write access to the `mental>mindful_minutes` metric.
    - **Exercise Time**: This determines the length of time (in seconds) that a breathing exercise session will take place.
    - **Exercise Speed**: This is a multiplier that will increase/decrease the rate of the breathing exercises. Higher numbers will cause the guided breathing to cycle faster, while lower values will decrease the rate.


## Usage

This section describes the general process for using Breathe.

1. Start Breathe using Python 3.
    - Example: `python3 ~/Software/Breathe/main.py`
2. After the interface opens, press the "Start" button.
3. Sit somewhere comfortable to prepare for the breathing exercise.
4. When the exercise begins, start by taking a slow deep breath.
5. Then, slowly exhale.
6. Repeat the breathing exercises as instructed.
7. When the timer is finished, the exercise will end.
    - If configured to do so, this is also when Breath will submit the session to HealthBox.
