"""
frequencies.py
Psi4 frequencies visualization tool
"""

import numpy as np
import psi4
import blobs

import plotly.graph_objects as go
import plotly.express as px



class Freq():
    def __init__(self, wfn):
        self.wfn = wfn
        self.mol = wfn.molecule()
        self.geo = self.mol.to_arrays()[0]
        self.sym = self.mol.to_arrays()[2]
        self.indices = self.get_index()
        self.frequencies = wfn.frequency_analysis["omega"][2][self.indices]
        self.info = self.get_info()
        self.bonds = None
        self.norm = None
        

    def get_info(self):

        color = []
        size = []
        atoms_colors = blobs.get_colors()

        for i in range(len(self.geo)):
            for atom in atoms_colors:
                if self.sym[i] == atom:
                    color.append(atoms_colors[atom][0])
                    size.append(atoms_colors[atom][1] + 15)

        mol_dic = {
            "color": color,
            "size" : np.array(size)
                   }

        return mol_dic
    
    
    def get_index(self):
        vib_index = []
        for i in range(len(self.wfn.frequency_analysis["TRV"][2])):
            if self.wfn.frequency_analysis["TRV"][2][i] == "V":
                vib_index.append(i)
        return vib_index
    

    def plot(self,
             size=1,
             nframes = 8,
             vib = 0, 
            ):

        atoms_colors = blobs.get_colors()
        bonds = build_bond_list(self.geo)   
        self.bonds = bonds    
        fms = []
        norm_coord = self.wfn.frequency_analysis['x'][2][:,self.indices].T.reshape(len(self.indices),len(self.geo),3)
        self.norm = norm_coord
                       
        for frame in range(nframes - 1):
                      
            data = [] 
            data.append(go.Scatter3d(x=self.geo[:,0] + self.norm[vib][:,0]/(nframes - frame), 
                                     y=self.geo[:,1] + self.norm[vib][:,1]/(nframes - frame), 
                                     z=self.geo[:,2] + self.norm[vib][:,2]/(nframes - frame)))
            fms.append(go.Frame(data=data))         

            for i in range(1, len(bonds)):
                
                bond_color_1= atoms_colors[self.sym[bonds[i][0]]][0]
                bond_color_2= atoms_colors[self.sym[bonds[i][1]]][0]

                midx  = (self.geo[bonds[i][0]][0] + self.norm[vib][bonds[i][0],0]/(nframes - frame) + self.geo[bonds[i][1]][0] + self.norm[vib][bonds[i][1],0]/(nframes - frame)) / 2
                midy  = (self.geo[bonds[i][0]][1] + self.norm[vib][bonds[i][0],1]/(nframes - frame) + self.geo[bonds[i][1]][1] + self.norm[vib][bonds[i][1],1]/(nframes - frame)) / 2
                midz  = (self.geo[bonds[i][0]][2] + self.norm[vib][bonds[i][0],2]/(nframes - frame) + self.geo[bonds[i][1]][2] + self.norm[vib][bonds[i][1],2]/(nframes - frame)) / 2

                bond_x_1 = [self.geo[:,0][bonds[i][0]] + self.norm[vib][bonds[i][0],0]/(nframes - frame), midx]
                bond_y_1 = [self.geo[:,1][bonds[i][0]] + self.norm[vib][bonds[i][0],1]/(nframes - frame), midy]
                bond_z_1 = [self.geo[:,2][bonds[i][0]] + self.norm[vib][bonds[i][0],2]/(nframes - frame), midz]

                bond_x_2 = [self.geo[:,0][bonds[i][1]] + self.norm[vib][bonds[i][1],0]/(nframes - frame), midx]
                bond_y_2 = [self.geo[:,1][bonds[i][1]] + self.norm[vib][bonds[i][1],1]/(nframes - frame), midy]
                bond_z_2 = [self.geo[:,2][bonds[i][1]] + self.norm[vib][bonds[i][1],2]/(nframes - frame), midz]

                data.append(go.Scatter3d(
                            x=bond_x_1,
                            y=bond_y_1,
                            z=bond_z_1,
                            mode="lines",
                            line={
                                "color": bond_color_1,
                                "width": 7 * size
                            },
                        ))

                data.append(go.Scatter3d(
                            x=bond_x_2,
                            y=bond_y_2,
                            z=bond_z_2,
                            mode="lines",
                            line={
                                "color": bond_color_2,
                                "width": 7 * size
                            },
                        ))

        fms.reverse()
        fms_inv = fms.copy()
        fms.reverse()

        data = [go.Scatter3d(x=self.geo[:,0] + norm_coord[vib][:,0]/nframes, 
                            y=self.geo[:,1] + norm_coord[vib][:,1]/nframes, 
                            z=self.geo[:,2] + norm_coord[vib][:,2]/nframes,
                       mode='markers',
                       marker={"showscale": False,
                               "color": self.info["color"],
                                "size": self.info["size"] * size / 1.0,
                                "showscale": False,
                                "opacity": 1.0,
                                "line": {
                                        "width": 2,
                                        "color": "black"
                                        }
                                    })]

        for i in range(len(bonds)):

            midx  = (self.geo[bonds[i][0]][0] + self.norm[vib][bonds[i][0],0]/(nframes) + self.geo[bonds[i][1]][0] + self.norm[vib][bonds[i][1],0]/(frame)) / 2
            midy  = (self.geo[bonds[i][0]][1] + self.norm[vib][bonds[i][0],1]/(nframes) + self.geo[bonds[i][1]][1] + self.norm[vib][bonds[i][1],1]/(frame)) / 2
            midz  = (self.geo[bonds[i][0]][2] + self.norm[vib][bonds[i][0],2]/(nframes) + self.geo[bonds[i][1]][2] + self.norm[vib][bonds[i][1],2]/(frame)) / 2

            bond_color_1= atoms_colors[self.sym[bonds[i][0]]][0]
            bond_color_2= atoms_colors[self.sym[bonds[i][1]]][0]

            bond_x_1 = [self.geo[:,0][bonds[i][0]] + self.norm[vib][bonds[i][0],0]/(frame), midx]
            bond_y_1 = [self.geo[:,1][bonds[i][0]] + self.norm[vib][bonds[i][0],1]/(frame), midy]
            bond_z_1 = [self.geo[:,2][bonds[i][0]] + self.norm[vib][bonds[i][0],2]/(frame), midz]

            bond_x_2 = [self.geo[:,0][bonds[i][1]] + self.norm[vib][bonds[i][1],0]/(frame), midx]
            bond_y_2 = [self.geo[:,1][bonds[i][1]] + self.norm[vib][bonds[i][1],1]/(frame), midy]
            bond_z_2 = [self.geo[:,2][bonds[i][1]] + self.norm[vib][bonds[i][1],2]/(frame), midz]

            # midx  = (self.geo[bonds[i][0]][0] + self.geo[bonds[i][1]][0]) / 2
            # midy  = (self.geo[bonds[i][0]][1] + self.geo[bonds[i][1]][1]) / 2
            # midz  = (self.geo[bonds[i][0]][2] + self.geo[bonds[i][1]][2]) / 2

            # bond_color_1= atoms_colors[self.sym[bonds[i][0]]][0]
            # bond_color_2= atoms_colors[self.sym[bonds[i][1]]][0]

            # bond_x_1 = [self.geo[bonds[i][0]][0], midx]
            # bond_y_1 = [self.geo[bonds[i][0]][1], midy]
            # bond_z_1 = [self.geo[bonds[i][0]][2], midz]
            # bond_x_2 = [self.geo[bonds[i][1]][0], midx]
            # bond_y_2 = [self.geo[bonds[i][1]][1], midy]
            # bond_z_2 = [self.geo[bonds[i][1]][2], midz]

            data.append(go.Scatter3d(
                        x=bond_x_1,
                        y=bond_y_1,
                        z=bond_z_1,
                        mode="lines",
                        line={
                            "color": bond_color_1,
                            "width": 7
                        },
                    ))

            data.append(go.Scatter3d(
                        x=bond_x_2,
                        y=bond_y_2,
                        z=bond_z_2,
                        mode="lines",
                        line={
                            "color": bond_color_2,
                            "width": 7
                        },
                    ))
          
        fig = go.Figure(data=data, 
            
        layout=go.Layout(
            scene = {'xaxis': {'range': [self.geo[:,0].min() -2, self.geo[:,0].max() + 2], 'autorange': False},
                     'yaxis': {'range': [self.geo[:,1].min() -2, self.geo[:,1].max() + 2], 'autorange': False},
                     'zaxis': {'range': [self.geo[:,2].min() -2, self.geo[:,2].max() + 2], 'autorange': False}},
            title=F"Frequency: {self.frequencies[vib].real:.2f} 1/cm",
            updatemenus=[dict(
                type="buttons",
                buttons=[dict(label="Play",
                              method="animate",
                              args=[None,{"frame": {"duration": 0, "redraw": True}}]),

                        {"args": [[None], {"frame": {"duration": 0, "redraw": False},
                                           "mode": "immediate",
                                           "transition": {"duration": 0}}],
                        "label": "Stop",
                        "method": "animate"}
                        ])]),
                       
        frames = fms + fms_inv + fms + fms_inv + fms + fms_inv + fms + fms_inv + fms + fms_inv
        )

        #layout = go.layout.Template(layout=go.Layout(title_font=dict(family="Rockwell", size=24)))

        fig.update_layout(scene_xaxis_showticklabels=False,
                          scene_yaxis_showticklabels=False,
                          scene_zaxis_showticklabels=False,
                          dragmode="orbit",
                          width=size * 500,
                          height=size * 500,
                          template="plotly_white",
                          autosize=True,
                          showlegend=False,
                          hovermode=False,
                          xaxis=dict(autorange=True, showgrid=False, ticks='', showticklabels=False),
                          yaxis=dict(autorange=True, showgrid=False, ticks='', showticklabels=False),
                          scene={
                              "xaxis": {
                                  "range": (self.geo[:,0].min() -2, self.geo[:,0].max() + 2),
                                  "showgrid": False,
                                  "zeroline": False,
                                  "showline": False,
                                  "title": "",
                                  "ticks": '',
                                  "showticklabels": False, 
                                  "showspikes" : False
                              },
                              "yaxis": {
                                  "range": (self.geo[:,1].min() -2, self.geo[:,1].max() + 2),
                                  "showgrid": False,
                                  "zeroline": False,
                                  "showline": False,
                                  "title": "",
                                  "ticks": '',
                                  "showticklabels": False, 
                                  "showspikes": False
                                  
                              },
                              "zaxis": {
                                  "range": (self.geo[:,2].min() -2, self.geo[:,2].max() + 2),
                                  "showgrid": False,
                                  "zeroline": False,
                                  "showline": False,
                                  "title": "",
                                  "ticks": '',
                                  "showticklabels": False, 
                                  "showspikes": False
                              }
                          })

        fig.show(config={'scrollZoom': False})



def calculate_distance(rA, rB):
    """Calculate the distance between points A and B. Assumes rA and rB are numpy arrays."""
    dist_vec = (rA - rB)
    distance = np.linalg.norm(dist_vec)
    return distance


def calculate_distance_list(rA, rB):
    """Calculate the distance between points A and B. Assums rA and rB are lists."""
    squared_sum = 0
    for dim in range(len(rA)):
        squared_sum += (rA[dim] - rB[dim])**2

    distance = np.sqrt(squared_sum)
    return distance


def build_bond_list(coordinates, max_bond=2.7, min_bond=0):
    """ Build list of bonds from atomic coordinates based on distance.

    Parameters
    ----------
    coordinates : np.array
        An array of atomic coordinates.
    max_bond : float (optional)
        The maximum distance between atoms to be considered a bond. Default=2.934 bohr
    min_bond : float, optional
        The minimum distance between atoms to be considered a bond. Default is 0 bohr

    Retruns
    -------
    bonds : dictionary
        A dictonary of bonds with atom pair tuples as keys, and calculate bond lengths as values



    """
    num_atoms = len(coordinates)

    bonds_list = []

    for atom1 in range(num_atoms):
        for atom2 in range(atom1, num_atoms):
            distance = calculate_distance(coordinates[atom1], coordinates[atom2])

            if distance > min_bond and distance < max_bond:
                bonds_list.append([atom1, atom2, distance])

    return bonds_list
