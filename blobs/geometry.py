"""

"""

import plotly.graph_objects as go

def geometry(mol):
    
    geometry = go.Scatter3d(x      = mol.geometry[:,0],
                            y      = mol.geometry[:,1],
                            z      = mol.geometry[:,2],
                            hovertext  = mol.symbols,
                            mode   = 'markers+text', 
                            marker = {"size"      : mol.size / 2 + 15, 
                                      "color"     : mol.color,
                                      "showscale" : False,
                                      "opacity"   : 1.0,
                                      "line"      : {"color": "black", 
                                                     "width": 4}})
    
    return geometry
