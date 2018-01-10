# MOKESetup
Python instructions for MOKE setup for use in labs

Instructions in Python to control a USB-3104 Voltage/Current output device to control a Kepco power supply. There are varying levels of complexity, with a simple text interface to a GUI. Not much range, obviously. 

Careful of too high voltage or current, and gain values must be adjusted to an acceptable value before continuing.

The VoltageTest files are the oldest and most primitive: they allow simple I/O for the device. The GUI code gives a window and GUI for the controlling of Voltage. The hysteresis code (which is the goal of the control; to create magnetic hysteresis loops) is the newest and still in its infant stages.
