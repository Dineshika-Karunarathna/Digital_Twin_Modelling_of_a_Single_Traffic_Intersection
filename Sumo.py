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