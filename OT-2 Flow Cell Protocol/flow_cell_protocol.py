import sys
from opentrons import robot, labware, instruments
import requests
sys.path.append('/data/user_storage/linnar_custom_libraries') # Make sure this points to the folder containing pyduino.py on the OT-2
from pyduino import *
import time

tiprack = labware.load('tiprack-200ul', '1')
sourcedye = labware.load('point', '2')
sourcewash = labware.load('point', '8')
pipette = instruments.P300_Multi(
    mount='right',
    tip_racks=[tiprack]
)

#Global variables
valveopen = False
valvepin = 7
serveradress = 'http://169.254.178.187:8080/update/'

if not robot.is_simulating():
	a = Arduino(serial_port='/dev/ttyACM0', baud_rate=9600, read_timeout=5) #Set serial port for Arduino manually, check on OT2 using ls /dev/ttyACM*. This needs an automated way of doing it
	a.set_pin_mode(valvepin, 'O') #set pin used for solenoid valve to output state
	time.sleep(1)

def webrequest(step):
    # Send a GET request to serveradress/step until a 'done' is returned.
    done = False
    while not done:
        r = requests.get(serveradress + step)
        done = r.json()['done']

def valvetoggle():
    if not robot.is_simulating():
        global valveopen
        if valveopen == False:
            a.digital_write(valvepin, 1)
            valveopen = True
        else:
            a.digital_write(valvepin, 0)
            valveopen = False  

def run_custom_protocol(
    cycles = 4,
    aspiration_speed = 50, 
    dispense_speed = 10, 
    wash_dispense_speed = 5,
    volume = 40,
    wash_volume = 300,
    wash_cycles = 1,
    valvetime = 10):

    flow_cell = labware.load('1x8_flow_cell', '3')

    for i in range (0,cycles):
        pipette.pick_up_tip()
        pipette.set_flow_rate(aspirate = aspiration_speed, dispense = wash_dispense_speed)
        for c in range (0, wash_cycles):
            pipette.aspirate(wash_volume, sourcewash)
            pipette.move_to((flow_cell.wells(0), (0,0,70))) # Move to location above flow cell, to avoid potential collision with vacuum manifold hardware
            pipette.move_to((flow_cell.wells(0), (0,0,3)))
            pipette.instrument_mover.push_active_current() 
            pipette.instrument_mover.set_active_current(0.08) # Set current to lower level, to reduce force applied to flow cell when inserting tips all the way for a good seal 
            pipette.move_to((flow_cell.wells(0), (0,0,-1)))
            valvetoggle()
            pipette.dispense(wash_volume, (flow_cell.wells(0), (0,0,-1)))
            if not robot.is_simulating():
                time.sleep(valvetime)
            valvetoggle()
            webrequest('capture_image')
            pipette.instrument_mover.pop_active_current()
            pipette.move_to((flow_cell.wells(0), (0,0,70)))
        pipette.drop_tip()

        pipette.pick_up_tip()
        pipette.aspirate(volume, sourcedye)
        pipette.move_to((flow_cell.wells(0), (0,0,70)))
        pipette.move_to((flow_cell.wells(0), (0,0,3)))
        pipette.instrument_mover.push_active_current()
        pipette.instrument_mover.set_active_current(0.08) #set current to lower level, to reduce force applied to flow cell when inserting tips all the way for a good seal 
        pipette.move_to((flow_cell.wells(0), (0,0,-1)))
        valvetoggle()
        pipette.dispense(0.8*volume, (flow_cell.wells(0), (0,0,-1)))
        pipette.dispense(0.2*volume, (flow_cell.wells(0), (0,0,-1)))
        if not robot.is_simulating():
            time.sleep(valvetime)
        valvetoggle()
        webrequest('capture_image')
        pipette.instrument_mover.pop_active_current()
        pipette.move_to((flow_cell.wells(0), (0,0,70)))
        pipette.drop_tip()

run_custom_protocol()
for c in robot.commands():
    print(c)

if not robot.is_simulating():
    a.close