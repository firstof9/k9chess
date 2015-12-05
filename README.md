# K9 Chess
Code and configuration files for a chess playing enhancement to a remote presence robot

# Directory Structure

## node-RED
This directory contains the flows to control K9

## python
This directory contains the python programs that use the Adafruit PWM Servo Driver to make K9 move.

Program | Description
---  | ---
servocontroller.py | Manipulates K9s steering and motors with failsafe reliant upon heartbeat
scanning.py | Controls K9s ears
head_down.py | Moves head to down position
head_up.py | Moves head to up position
wag_h.py | Wags tail horizontally
wag_v.py | Wags tail verticslly
servotuner.py | Can drive any PWM servo to any value (for callibration)
tail_up.py | Moves tail to up position
tail_down.py | Moves tail to down position

## www
This directory contains the HTML, CSS and JavaScript files used to provide the K9 user interface.

Directory | Description
---  | ---
k9.html | JQuery Mobile HTML5 pages for user interface
k9stage1.js | JavaScript program that captures user events and passes them and a control heartbeat to node-RED
jquery | Supporting JavaScript libraries
themes | Custom JQuery Mobile CSS Theme for K9