# 3D Magnetic modelling of ellipsoidal bodies

[D. T. Tomazella] (http://www.pinga-lab.org/people/tomazella.html)<sup>1</sup>, [V. C. Oliveira Jr.](http://www.pinga-lab.org/people/oliveira-jr.html)<sup>1</sup>.

*<sup>1</sup>Department of Geophysics, Observatório Nacional, Rio de Janeiro, RJ, Brazil.*

> This paper has been submitted for publication in 
> [**Geoscientific Model Development (GMD)**]

####Abstract

Since the second half of the nineteenth century, a vast literature has been published
on the magnetic modeling of uniformly magnetized ellipsoids. In this work,
we present a integrated review about magnetic modeling of triaxial, prolate and
oblate ellipsoids, with arbitrary orientation, with or without remanent magnetization
and with both isotropic and anisotropic susceptibilities. We also bring a
theoretical discussion regarding the commom value of isotropic susceptibility (0.1
SI), widely used by geoscientific community, and not often discussed, as the limit
of which the self-demagnetization can be overlooked in magnetic modeling. Apparently,
this value was obtained empirically and we propose an alternative way of
determining its limit, based on previous knowledge of the shape and the maximum
relative error allowed in the resultant magnetization. Jointly, we provide a set of
routines capable of modeling the magnetic field produce by triaxial, prolate and
oblate ellipsoidal bodies. These routines are written in Python language as part of
the Fatiando a Terra package. Examples in this work show the friendly and easy
usage of the program. Hence, we hope that this work can be useful both as educational
tool (e.g. Potential Methods and rock magnetism) as to applied geophysics
(e.g. high susceptibility bodies characterization) and are freely available at the link
https://github.com/DiegoTaka/ellipsoid-magnetic for the geoscientific community.

![Test with two triaxial ellipsoids modeled with the routines](manuscript/figures/ellipsoid_triaxial_multi.pdf)

> This paper has been submitted for publication in 
> [**Geoscientific Model Development (GMD)**]

#### Reproducing the results

You can download a copy of all the files in this repository by cloning the
[git](https://git-scm.com/) repository:

    git clone https://github.com/DiegoTaka/ellipsoid-magnetic.git

or [click here to download a zip archive](https://github.com/DiegoTaka/ellipsoid-magnetic/archive/master.zip).

All source code used to generate the results and figures in the paper are in
the `code` folder.
The data used in this study is provided in `data` and the sources for the
manuscript text and figures are in `manuscript`.
See the `README.md` files in each directory for a full description.

The calculations and figure generation are all run inside
[Jupyter notebooks](http://jupyter.org/).
You can view a static (non-executable) version of the notebooks in the
[nbviewer]() webservice:

http://nbviewer.jupyter.org/github.com/DiegoTaka/ellipsoid-magnetic

See sections below for instructions on executing the code.

#### Setting up your environment

You'll need a working Python **2.7** environment with all the standard
scientific packages installed (numpy, scipy, matplotlib, etc).  The easiest
(and recommended) way to get this is to download and install the
[Anaconda Python distribution](http://continuum.io/downloads#all).
Make sure you get the **Python 2.7** version.

You'll also need to install the [Fatiando a Terra](http://www.fatiando.org/) library
from GitHub.
We used a development version defined by the
commit hash [09cd37da986114a68c57c6a611271fc6cd22bde4]
(https://github.com/fatiando/fatiando/tree/09cd37da986114a68c57c6a611271fc6cd22bde4).
See the install instructions on the website.

#### Running the code

To execute the code in the Jupyter notebooks, you must first start the
notebook server by going into the repository folder and running:

    jupyter notebook

This will start the server and open your default web browser to the Jupyter
interface. In the page, go into the `code` folder and select the
notebook that you wish to view/run.

The notebook is divided cells (some have text while other have code).
Each cell can be executed using `Shift + Enter`.
Executing text cells does nothing and executing code cells runs the code
and produces it's output.
To execute the whole notebook, run all cells in order.

#### License

All source code is made available under a [BSD 3-clause]
(http://choosealicense.com/licenses/bsd-3-clause/) 
license.  You can freely
use and modify the code, without warranty, so long as you provide attribution
to the authors.  See `LICENSE.md` for the full license text.

The manuscript text is not open source. The authors reserve the rights to the
article content, which is currently submitted for publication in the
[**Geoscientific Model Development (GMD)**]