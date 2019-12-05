
<p align="center">
<br>
<img src="docs/media/logo_vertical.png" alt="Blobs" height=300> <br>
<a href="https://travis-ci.org/VHChavez/blobs"><img src="https://travis-ci.org/VHChavez/blobs.svg?branch=master"></a>
<a href="https://ci.appveyor.com/project/REPLACE_WITH_OWNER_ACCOUNT/blobs/branch/master"><img src="https://ci.appveyor.com/api/projects/status/REPLACE_WITH_APPVEYOR_LINK/branch/master?svg=true"></a>
<a href="https://opensource.org/licenses/BSD-3-Clause"><img src="https://img.shields.io/badge/License-BSD%203--Clause-blue.svg" /></a>
<br>
</p>

---

### Overview
Plotting a cube file just requires:

```
import blob
cube = blob.cube(wfn)
cube.plot("Da.cube", iso=0.03)
```

For the Full Jupyter tutorial see:
/blobs/tutorials/basics. 


### Required Packages
Set up a conda environment and proceed to install

```
conda install -c psi4 psi4
conda install -c plotly plotly
```

### Installation
```
git clone https://github.com/VHchavez/blobs
cd blobs
pip install --user -e .
```



