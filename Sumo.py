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