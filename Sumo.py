import osmnx as ox
import networkx as nx
import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import matplotlib.animation as animation
import random
from geographiclib.geodesic import Geodesic
import time

geod = Geodesic.WGS84
G = ox.graph_from_bbox(6.92216, 6.92019, 79.87877, 79.87732, network_type='drive') #, simplify=True)
G = ox.add_edge_speeds(G)
G = ox.add_edge_travel_times(G)

projected_graph = ox.project_graph(G, to_crs="EPSG:3395")
Gc = ox.consolidate_intersections(projected_graph, dead_ends=True)
edges = ox.graph_to_gdfs(ox.get_undirected(Gc), nodes=False)

vehnumber = 10
routes = []
route = []
allAngleList = []
direction = []
all_route_roadnames = []
all_route_speeds = []

angleList = []
direzione = []
route_roadnames = []
route_speed = []

LEFT_SIG = ""
STRAIGHT_SIG = ""
RIGHT_SIG = ""

columns = ['vehID', 'subroute', 'speed', 'turn', 'angle', 'lengthOfSubroute']
data = []
df = pd.DataFrame()

for iroute in range(vehnumber):
    
    try:
        y0 = 0.0
        x0 = 0.0
        
        lat = round(random.uniform(6.92019, 6.92216), 5)
        lon = round(random.uniform(79.87877, 79.87732), 5)
        good_orig_node = ox.get_nearest_node(G, (lat, lon), method='euclidean')

        lat = round(random.uniform(6.92019, 6.92216), 5)
        lon = round(random.uniform(79.87877, 79.87732), 5)
        good_dest_node = ox.get_nearest_node(G, (lat, lon), method='euclidean')

        routep1 = nx.shortest_path(G, good_orig_node, good_dest_node)
        lengthOfRoute1 = nx.shortest_path_length(G, good_orig_node, good_dest_node, weight='length')

        lat = round(random.uniform(6.92019, 6.92216), 5)
        lon = round(random.uniform(79.87877, 79.87732), 5)
        next_dest_node = ox.get_nearest_node(G, (lat, lon), method='euclidean')

        routep2 = nx.shortest_path(G, good_dest_node, next_dest_node)
        lengthOfRoute2 = nx.shortest_path_length(G, good_dest_node, next_dest_node, weight='length')

        route = routep1 + routep2
        lengthOfRoute = lengthOfRoute1 + lengthOfRoute2
        
        lor = round(lengthOfRoute/1000.0, 2)
        
        angleList = []
        direzione = []
        route_roadnames = []
        route_speed = []
         ## iterate through roads (i.e. edges) in a route
        for irou in route:
            
            incident_edges = edges[(edges['u_original']==irou) | (edges['v_original']==irou)]
            
            for _, edge in incident_edges.fillna('').iterrows():
                #print("vehID: ", iroute, " Road name: ", edge['name'], ", ", "Speed: ", edge['speed_kph'], " kmph")
                instantroad = edge['name']
                instantspd = edge['speed_kph']
                route_roadnames.append(edge['name'])
                route_speed.append(edge['speed_kph'])
                
                latlat = G.nodes[irou]['y']
                lonlon = G.nodes[irou]['x']

                #print("Left! {:.3f} degrees.".format(turnAngle['azi1']))
                direzione.append("straight")
                
                TURN_SIG = "straight"
                
                #print("GPS Coordinates: ", latlat, ", ", lonlon)
                turnAngle = geod.Inverse(latlat,lonlon,y0,x0)

                if turnAngle['azi1'] > 45.0 and turnAngle['azi1'] < 135.0:
                    #print("Right! {:.3f} degrees.".format(turnAngle['azi1']))
                    direzione.append("right")
                 
                    TURN_SIG = "right"
                if (turnAngle['azi1'] > -135.0 and turnAngle['azi1'] < -45.0):
                   #print("Left! {:.3f} degrees.".format(turnAngle['azi1']))
                    direzione.append("left")
                    TURN_SIG = "left"
                  
                y0 = latlat
                x0 = lonlon
                
                angleList.append(turnAngle['azi1'])

                values = [iroute, instantroad, instantspd, TURN_SIG, turnAngle['azi1'], edge.get('length', None)]
                zipped = zip(columns, values)
                a_dictionary = dict(zipped)
                #print(a_dictionary)
                data.append(a_dictionary)

            df = df.append(data, True)
            
            my_dict = {i:round(direzione.count(i)/len(direzione)*100.0,1) for i in direzione}