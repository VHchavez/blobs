import numpy as np
from .atom_data import *

class Molecule():
    def __init__(self, mol):
        
        self.dict         = mol.dict()
        self.geometry     = self.dict["geometry"]
        self.natoms       = len(self.dict["geometry"])
        self.symbols      = self.dict["symbols"]
        self.connectivity = self.get_connectivity()
        self.color        = self.get_colors()
        self.size         = self.dict["atomic_numbers"]

    def get_colors(self):
        colors = []
        for i in range(len(self.geometry)):
            for atom in atom_colors:
                if self.symbols[i] == atom:
                    colors.append(atom_colors[atom][0])
                    
        return colors



    def get_connectivity(self):
            
            if "connectivity" not in self.dict:
                connectivity = build_bond_list(self.geometry)

            elif self.dict["connectivity"] is None:
                connectivity = build_bond_list(self.geometry)

            else:
                connectivity = self.dict["connectivity"]
                
            return connectivity


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


def build_bond_list(coordinates, max_bond=3.0, min_bond=0):
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
                    bonds_list.append([atom1, atom2, 1.0])

        return bonds_list
