"""

"""

import plotly.graph_objects as go
import numpy as np
from .atom_data import *

def bonds(mol, bond):

    trace = []

    color_bond_1 = atom_colors[mol.symbols[mol.connectivity[bond][0]]][0]
    color_bond_2 = atom_colors[mol.symbols[mol.connectivity[bond][1]]][0]
    color_bonds = [color_bond_1, color_bond_2]
    
    #Middle point between points
    midx = (mol.geometry[mol.connectivity[bond][0]][0] + mol.geometry[mol.connectivity[bond][1]][0])/2
    midy = (mol.geometry[mol.connectivity[bond][0]][1] + mol.geometry[mol.connectivity[bond][1]][1])/2
    midz = (mol.geometry[mol.connectivity[bond][0]][2] + mol.geometry[mol.connectivity[bond][1]][2])/2

    #Half bonds -> List of tuples from atom_i to mid_point(atom_i, atom_j)
    x_bond = [np.array([mol.geometry[mol.connectivity[bond][0]][0], midx]), np.array([mol.geometry[mol.connectivity[bond][1]][0], midx])]
    y_bond = [np.array([mol.geometry[mol.connectivity[bond][0]][1], midy]), np.array([mol.geometry[mol.connectivity[bond][1]][1], midy])]
    z_bond = [np.array([mol.geometry[mol.connectivity[bond][0]][2], midz]), np.array([mol.geometry[mol.connectivity[bond][1]][2], midz])]

    #Double bonds
    xo = mol.geometry[mol.connectivity[bond][0]][0]
    yo = mol.geometry[mol.connectivity[bond][0]][1]
    zo = mol.geometry[mol.connectivity[bond][0]][2]
    #Displace color bonds so that that color boundaries match. 
    slope_len  = np.sqrt( (xo - midx)**2 + (yo - midy)**2 + (zo - midz)**2 )
    slope_x    = (xo - midx) / slope_len
    slope_y    = (yo - midy) / slope_len
    slope_z    = (zo - midz) / slope_len

    bsx = 0
    bsz = slope_y/4
    bsy = (-1 * bsx * (xo - midx) - bsz * (zo - midz)) / (yo - midy)

    
    #Single Bonds
    if mol.connectivity[bond][2] == 1.0:
        
        for i in [0, 1]:
            trace.append(go.Scatter3d(
                     x=x_bond[i],
                     y=y_bond[i],
                     z=z_bond[i],
                     hovertext = "",
                     mode="lines",
                     marker={"size":1},
                     line={"color": color_bonds[i],
                          "width": 10,
                          "showscale" : False}))
        
    #Double Bonds
    if mol.connectivity[bond][2] == 2.0:
        
        #atom_i
        for i in [0, 1]:
            trace.append(go.Scatter3d(
                     x=x_bond[i] + bsx,
                     y=y_bond[i] + bsy,
                     z=z_bond[i] + bsz,
                     mode="lines",
                     marker={"size":1},
                     line={"color": color_bonds[i],
                          "width": 10,
                          "showscale" : False}))
        #atom_j
        for i in [0, 1]:
            trace.append(go.Scatter3d(
                     x=x_bond[i] - bsx,
                     y=y_bond[i] - bsy,
                     z=z_bond[i] - bsz,
                     mode="lines",
                     marker={"size":1},
                     line={"color": color_bonds[i],
                          "width": 10,
                          "showscale" : False}))
            
    #Triple Bonds
    if mol.connectivity[bond][2] == 3.0:

        for i in [0, 1]:
            trace.append(go.Scatter3d(
                     x=x_bond[i] + bsx,
                     y=y_bond[i] + bsy,
                     z=z_bond[i] + bsz,
                     mode="lines",
                     marker={"size":1},
                     line={"color": color_bonds[i],
                          "width": 10,
                          "showscale" : False}))

        for i in [0, 1]:
            trace.append(go.Scatter3d(
                     x=x_bond[i] - bsx,
                     y=y_bond[i] - bsy,
                     z=z_bond[i] - bsz,
                     mode="lines",
                     marker={"size":1},
                     line={"color": color_bonds[i],
                          "width": 10,
                          "showscale" : False}))
        for i in [0, 1]:
            trace.append(go.Scatter3d(
                     x=x_bond[i],
                     y=y_bond[i],
                     z=z_bond[i],
                     mode="lines",
                     marker={"size":1},
                     line={"color": color_bonds[i],
                          "width": 10,
                          "showscale" : False}))
            

    return trace
