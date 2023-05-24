#!/usr/bin/env python

import os
import sys
import optparse
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# we need to import some python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


from sumolib import checkBinary  # Checks for the binary in environ vars
import traci


import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import time
import random

## Fetch the service account key JSON file contents
cred = credentials.Certificate("secret_key.json")

## Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://four-way-junction-default-rtdb.firebaseio.com/"
})

## Get a reference to the database service
ref = db.reference('/')

## Generate vehicle flow
def vehicleFlow(N_E_number, N_S_number,N_W_number,E_N_number,E_S_number,E_W_number,S_N_number,S_E_number,S_W_number,W_N_number,W_E_number,W_S_number):
    f = open('4_way.rou.xml', 'w')

    s = '''<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">\n\
  \n\t  <vType id ="car" vClass= "passenger" length="5" accel="3.5" decel="2.2" sigma="1.0" maxSpeed="8" />\
  \n\t  <vType id= "ev" vClass="emergency" length="7" accel="5.5" decel="2.2" sigma="1.0" maxSpeed="20" guiShape="emergency" speedFactor="2.0" minGapLat="0.2"/>\
  \n\t  <vType id= "bus" vClass="bus" length="7" accel="5.5" decel="2.2" sigma="1.0" maxSpeed="5" color="0,0,1"/>\
  \n\t  <vType id= "motorcycle" vClass="motorcycle" length="5" accel="5.5" decel="2.2" sigma="1.0" maxSpeed="5" color="1,0,1"/>\
  \n\t  <vType id= "taxi" vClass="taxi" length="4" accel="5.5" decel="2.2" sigma="1.0" maxSpeed="5" color="255,0,0"/>\
  \n\
  \n\
  '''

    s += '\n   <flow id="N_E_flow" type="car" begin="0" end="0" number="{}" from=" E4" to=" E1" />'.format(N_E_number)
    s += '\n   <flow id="N_S_flow" type="bus" begin="0" end="0" number="{}" from=" E4" to="E3" />'.format(N_S_number)
    s += '\n   <flow id="N_W_flow" type="taxi" begin="0" end="0" number="{}" from="E4" to="-E0" />'.format(N_S_number)
    s += '\n   <flow id="E_N_flow" type="motorcycle" begin="0" end="0" number="{}" from="-E1" to="-E4" />'.format(E_N_number)
    s += '\n   <flow id="E_S_flow" type="bus" begin="0" end="0" number="{}" from=" -E1" to="E3" />'.format(E_S_number)
    s += '\n   <flow id="E_W_flow" type="ev" begin="0" end="0" number="{}" from=" -E1" to=" -E0" />'.format(E_W_number)
    s += '\n   <flow id="S_N_flow" type="car" begin="0" end="0" number="{}" from=" -E3" to=" -E4" />'.format(S_N_number)
    s += '\n   <flow id="S_E_flow" type="bus" begin="0" end="0" number="{}" from=" -E3" to="E1" />'.format(S_E_number)
    s += '\n   <flow id="S_W_flow" type="taxi" begin="0" end="0" number="{}" from="-E3" to="-E0" />'.format(S_W_number)
    s += '\n   <flow id="W_N_flow" type="motorcycle" begin="0" end="0" number="{}" from="E0" to="-E4" />'.format(W_N_number)
    s += '\n   <flow id="W_E_flow" type="bus" begin="0" end="0" number="{}" from=" E0" to="E1" />'.format(W_E_number)
    s += '\n   <flow id="W_S_flow" type="ev" begin="0" end="0" number="{}" from=" E0" to="E3" />'.format(W_S_number)
    
    s += '\n</routes>\n'

    f.write(s)
    f.close()





### Retrive data from DB
def retrive_data():
    x = 0
    while True:
        ## Retrive data form DB
        data = ref.get()
        vehicles = data['Vehicles']
        if len(vehicles) == 0:
            break
        elif x < len(vehicles):
              ## Assigning values
            N_E_number = vehicles[x]['N_E']
            N_S_number = vehicles[x]['N_S']
            N_W_number = vehicles[x]['N_W']
            E_N_number = vehicles[x]['E_N']
            E_S_number = vehicles[x]['E_S']
            E_W_number = vehicles[x]['E_W']
            S_N_number = vehicles[x]['S_N']
            S_E_number = vehicles[x]['S_E']
            S_W_number = vehicles[x]['S_W']
            W_N_number = vehicles[x]['W_N']
            W_E_number = vehicles[x]['W_E']
            W_S_number = vehicles[x]['W_S']
            x += 1
            
            vehicleFlow(N_E_number, N_S_number,N_W_number,E_N_number,E_S_number,E_W_number,S_N_number,S_E_number,S_W_number,W_N_number,W_E_number,W_S_number)
            print(N_E_number, N_S_number,N_W_number,E_N_number,E_S_number,E_W_number,S_N_number,S_E_number,S_W_number,W_N_number,W_E_number,W_S_number)            
            step = 0
            while traci.simulation.getMinExpectedNumber() > 0:
                traci.simulationStep()
                step += 1
        else:
            break

# contains TraCI control loop
def run():
    retrive_data()
    traci.close()
    sys.stdout.flush()


def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options

# main entry point
if __name__ == "__main__":
    options = get_options()

    # check binary
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # traci starts sumo as a subprocess and then this script connects and runs
    traci.start([sumoBinary, "-c", "4_way.sumocfg",
                             "--tripinfo-output", "tripinfo.xml"])
    run()
