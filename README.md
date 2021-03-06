
### *blobs is no longer being developed. For better and enhanced functionality, visit the project [moly](https://github.com/VHchavez/moly) instead*
<p align="center">
<br>
<img src="docs/media/logo_vertical.png" alt="Blobs" height=300> <br><br>
<a href="https://opensource.org/licenses/BSD-3-Clause"><img src="https://img.shields.io/badge/License-BSD%203--Clause-blue.svg" /></a>
<br>
</p>

<!--
<a href="https://travis-ci.org/VHChavez/blobs"><img src="https://travis-ci.org/VHChavez/blobs.svg?branch=master"></a>
<a href="https://ci.appveyor.com/project/VHchavez/blobs"><img src="https://ci.appveyor.com/api/projects/status/REPLACE_WITH_APPVEYOR_LINK/branch/master?svg=true"></a>
-->


---


### Overview

Plot cube files produced with [Psi4](https://www.github.com/psi4/psi4) directly in a Jupyter Notebook. Visualizing a cube is as simple as:
```
# Psi4 Calculation
import psi4 
be2 = psi4.geometry("""
0 1 
  H      1.0686     -0.1411      1.0408
  C      0.5979      0.0151      0.0688
  H      1.2687      0.2002     -0.7717
  O     -0.5960     -0.0151     -0.0686
""")

psi4.set_options({"cubeprop_tasks" : ['density', 'orbitals'],
                  "cubeprop_orbitals" : [8, 9]})

energy, wfn = psi4.energy("SCF/cc-pVDZ", molecule=be2,return_wfn=True)

#Visualization with blobs
import blobs
cube = blobs.Cube(wfn)
cube.plot("Da.cube", iso=0.03)
```

For a full Jupyter tutorial visit [here](https://github.com/VHchavez/blobs/blob/b32ede91d43514fe24e15c9da0a2ebbb43d383e9/blobs/tutorial/Cube_Plot_Basics.ipynb).


### Required Packages
Set up a conda environment with Psi4(Recommended)
```
conda create -n p4env psi4 -c psi4
conda activate p4env

#Get plotly
conda install -c plotly plotly
```

More information on their corresponding repositories: 

<p align="center">
  <a href="https://github.com/psi4/psi4numpy"><img src="https://molssi.org/wp-content/uploads/2018/06/psi4numpybanner_eqn-1200x390_c.jpg" height=80 /></a>
  <a href="https://www.github.com/plotly/plotly.py"><img src="https://prismic-io.s3.amazonaws.com/plotly%2F6ea9b995-cdd8-49cb-b058-38bd44c1982d_plotly-logo-01-stripe%402x.png" height=80 /></a>
</p>


### Installation
```
git clone https://github.com/VHchavez/blobs
cd blobs
pip install .
```



