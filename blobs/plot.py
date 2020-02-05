"""

"""

import plotly.graph_objects as go
from .geometry import *
from .bonds    import *

def plot(mol, args):
    
    data = []
    fig = go.Figure(data=data)
    
    if "geometry" in args:
        geometry_trace = geometry(mol)
        fig.add_trace(geometry_trace)
        
    if "bonds" in args:
        for bond in range(len(mol.connectivity)):
            bond_trace = bonds(mol, bond)
            for i in range(len(bond_trace)):
                fig.add_trace(bond_trace[i])
        
    
    #Scene Template
    fig.update_layout(template="plotly_white", 
                      showlegend=False,
                      scene={"xaxis": get_axis_template(mol,0),
                             "yaxis": get_axis_template(mol,1),
                             "zaxis": get_axis_template(mol,2)})
    
    fig.show(config={'scrollZoom': True})

def get_axis_template(mol, axis):
    template = {  "range": (mol.geometry[:,axis].min() -1, mol.geometry[:,axis].max() +1),
                  "showgrid"      : False,
                  "zeroline"      : False,
                  "showline"      : False,
                  "title"         : "",
                  "showticklabels": False,
                  "showbackground": False,
                  "showspikes"    : False}
    return template
