# tmsi
Parser and management application for a Tinymesh radio network.
Listens to a serial COM port on the local PC where you have connected a Tinymesh gateway in packet mode.

## Environment and prerequisites before running
This is a python 3 application. It is tested on a Windows PC, but should be able to run on any python platform with a serial port and a GUI.
The app uses the tkinter framework do drive the GUI. If your platform has a GUI, your python 3 installation should already have tkinter included.
Install needed packages:
```
>pip install construct
>pip install dirq
>pip install pyserial
````

Verify that everything is set up correctly by running the unit test suite included:
```
>python test.py
```
## Usage with attached Tinymesh devkit gateway module
Start the comwrapper part that grabs incoming Tinymesh packets from the gateway:
    C:\Temp> python comwrapper port=COM1 baudrate=9600

In a separate process, start the GUI part of the application:
    C:\Temp> python tmsi_gui
    
If you don't have a Tinymesh devkit module, you can simulate its output by running ```python test_tm_live_data.py``` which will feed actual captured live data from the file live_test_data.txt to the serial port COM2 in binary format. Use a virtual COM port program like Eltima Virtual Serial Port Driver and create a virtual com port pair between COM1 and COM2 (this will feed any output to COM2 right back to COM1, where comwrapper should be listening.

## Sourcedoce and files documentation
The python code is documented using docstrings.

### comwrapper.py
A python script that should _allways_ be running when the Tinymesh network is active. It listens to incoming packets on the serial port (where your Tinymesh Gateway should be connected) and writes the packets to a store-and-forward queue, which is later read by the TinymeshController.

### tmsi_gui.py
A python script that runs the GUI part of the application. Invokes TinymeshController regularly and displays the health of radios, and shows any received Sportident punches.

### tmcontroller.py
Defines the class TinymeshController which checks for new Tinymesh packets on the store-and-forward queue, parses them, and updates a record of health and connectivity status for each radio unit. If a received packet contains a Sportident punch, parse it and log the punch. TinymeshController is a singleton that we call often from the event loop in the GUI.

### siparser.py
Defines parsing of a Sportident station punch.

### tmparser.py
Defines parsing of all different kinds of Tinymesh radio packets.

## TODO
Send punches to competition administration system using SIRAP.
Log sequence number of punches from each attached Sportident station (remember there can be more than one Sportident station per Tinymesh radio unit). Raise alarm when any gap in the sequence is detected. Number of missing punches, control number, and time interval.
