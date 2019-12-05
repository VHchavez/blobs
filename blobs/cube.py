"""
molecule.py
Psi4 cube files visualization tool
"""

import numpy as np
import psi4
from colors import get_colors

import plotly.graph_objects as go
import plotly.express as px


class Manager():
    def __init__(self, wfn):
        psi4.cubeprop(wfn)
        self.wfn = wfn
        self.geometry = self.wfn.molecule()
        self.spacing = psi4.core.get_global_option("CUBIC_GRID_SPACING")
        self.overage = psi4.core.get_global_option("CUBIC_GRID_OVERAGE")
        self.origin = self.get_origin()
        self.info = self.get_info()
        self.meta = None

    def get_origin(self):
        geometry = self.geometry.full_geometry().np

        L = self.overage
        D = self.spacing

        Xmin = np.zeros(3)
        Xmax = np.zeros(3)
        Xdel = np.zeros(3)

        N = np.zeros(3)
        O = np.zeros(3)

        for k in [0, 1, 2]:
            Xmin[k] = Xmax[k] = geometry[0, k]

            for atom in range(len(geometry)):
                Xmin[k] = geometry[atom, k] if Xmin[k] > geometry[atom, k] else Xmin[k]
                Xmax[k] = geometry[atom, k] if Xmax[k] < geometry[atom, k] else Xmax[k]

            Xdel[k] = Xmax[k] - Xmin[k]
            N[k] = int((Xmax[k] - Xmin[k] + 2.0 * L[k]) / D[k])

            if D[k] * N[k] < (Xmax[k] - Xmin[k] + 2.0 * L[k]):
                N[k] += 1

            O[k] = Xmin[k] - (D[k] * N[k] - (Xmax[k] - Xmin[k])) / 2.0

        return O

    def get_info(self):

        symbol = []
        x_geo = []
        y_geo = []
        z_geo = []
        color = []
        size = []
        atoms_colors = get_colors()

        for i in range(self.geometry.natom()):
            symbol.append(self.geometry.fsymbol(i))
            x_geo.append(int((self.geometry.fx(i) - self.origin[0]) / self.spacing[0]))
            y_geo.append(int((self.geometry.fy(i) - self.origin[1]) / self.spacing[1]))
            z_geo.append(int((self.geometry.fz(i) - self.origin[2]) / self.spacing[2]))

            for atom in atoms_colors:
                if self.geometry.fsymbol(i) == atom:
                    color.append(atoms_colors[atom][0])
                    size.append(atoms_colors[atom][1] + 15)

        mol_dic = {
            "sym": symbol,
            "x": np.array(x_geo),
            "y": np.array(y_geo),
            "z": np.array(z_geo),
            "color": color,
            "size": np.array(size)
        }

        return mol_dic

    def plot(self,
             cube_file,
             iso=0.03,
             cube_type="density",
             colorscale="Blues",
             size=1,
             plot_geometry=True,
             plot_bonds=True):

        cube, meta = cube_to_array(cube_file)
        self.meta = meta

        X, Y, Z = np.mgrid[:cube.shape[0], :cube.shape[1], :cube.shape[2]]

        data = []

        vol_data = go.Isosurface(x=X.flatten(),
                                 y=Y.flatten(),
                                 z=Z.flatten(),
                                 value=cube.flatten(),
                                 showscale=False,
                                 surface_count=2,
                                 isomax=iso,
                                 isomin=iso,
                                 opacity=0.2,
                                 colorscale=colorscale)

        data.append(vol_data)

        if cube_type == "orbital":
            vol_data_neg = go.Isosurface(x=X.flatten(),
                                         y=Y.flatten(),
                                         z=Z.flatten(),
                                         value=cube.flatten(),
                                         showscale=False,
                                         isomin=-1 * iso,
                                         isomax=-1 * iso,
                                         opacity=0.2,
                                         colorscale="Reds")

            data.append(vol_data_neg)

        if plot_geometry == True:

            geo_data = go.Scatter3d(x=self.info["x"],
                                    y=self.info["y"],
                                    z=self.info["z"],
                                    mode="markers",
                                    marker={
                                        "showscale": False,
                                        "color": self.info["color"],
                                        "size": self.info["size"] * size / 1.0,
                                        "showscale": False,
                                        "opacity": 1.0,
                                        "line": {
                                            "width": 2,
                                            "color": "gainsboro"
                                        }
                                    })

            data.append(geo_data)

        fig = go.Figure(data=data)

        if plot_bonds == True:

            bonds = build_bond_list(self.geometry.geometry().np)

            for i in range(len(bonds)):

                bond_x = [self.info["x"][bonds[i][0]], self.info["x"][bonds[i][1]]]
                bond_y = [self.info["y"][bonds[i][0]], self.info["y"][bonds[i][1]]]
                bond_z = [self.info["z"][bonds[i][0]], self.info["z"][bonds[i][1]]]

                fig.add_trace(
                    go.Scatter3d(
                        x=bond_x,
                        y=bond_y,
                        z=bond_z,
                        mode="lines",
                        line={
                            "color": "grey",
                            "width": 2
                        },
                    ))

        layout = go.layout.Template(layout=go.Layout(title_font=dict(family="Rockwell", size=24)))

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
                                  "autorange": True,
                                  "showgrid": False,
                                  "zeroline": False,
                                  "showline": False,
                                  "title": "",
                                  "ticks": '',
                                  "showticklabels": False
                              },
                              "yaxis": {
                                  "autorange": True,
                                  "showgrid": False,
                                  "zeroline": False,
                                  "showline": False,
                                  "title": "",
                                  "ticks": '',
                                  "showticklabels": False
                              },
                              "zaxis": {
                                  "autorange": True,
                                  "showgrid": False,
                                  "zeroline": False,
                                  "showline": False,
                                  "title": "",
                                  "ticks": '',
                                  "showticklabels": False
                              }
                          })

        fig.show(config={'scrollZoom': False})


def _getline(cube):
    """
    Read a line from cube file where first field is an int
    and the remaining fields are floats.

    Parameters

    ----------
    cube: file object of the cube file

    Returns

    -------
    (int, list<float>)

    """
    l = cube.readline().strip().split()
    return int(l[0]), list(map(float, l[1:]))


def cube_to_array(fname):
    """
    Read cube file into numpy array

    Parameters
    ----------
    fname: filename of cube file

    Returns
    --------
    (data: np.array, metadata: dict)

    """
    cube_details = {}
    with open(fname, 'r') as cube:
        cube.readline()
        cube.readline()  # ignore comments
        natm, cube_details['org'] = _getline(cube)
        nx, cube_details['xvec'] = _getline(cube)
        ny, cube_details['yvec'] = _getline(cube)
        nz, cube_details['zvec'] = _getline(cube)
        cube_details['atoms'] = [_getline(cube) for i in range(natm)]
        data = np.zeros((nx * ny * nz))
        idx = 0
        for line in cube:
            for val in line.strip().split():
                data[idx] = float(val)
                idx += 1
    data = np.reshape(data, (nx, ny, nz))
    cube.close()
    return data, cube_details


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
