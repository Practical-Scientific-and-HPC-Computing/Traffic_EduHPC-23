This is the code for the Peachy Assignment to parallelize the Nagel-Schreckenberg Traffic Model with OpenMP.  Originally given as an assignment in the University of Toronto course PHY1610H in the Winter of 2021.

You need a relatively recent g++ compiler, make or cmake for compilation, and a python 3 installation with matplotlib to use the npyplot.py script for creating a figure.

This Makefile also contains commands to run and plot results.

To compile the code, type 

```sh
   make 
```

To run the smaller test case and plot the results in the form an png files, use

```sh
   make test
```

To run the larger case and plot the results in the form an png files, use

```sh
   make largetest
```

The parameters are set in .ini files that can be given as command line arguments, e.g.:
```sh
   ./traffic test.ini
```
Output is in 3 files, two with postfixes -dens.npy, -velo.npy that contain the density and velocity of the traffic on a grid at the times stored in the file with postfix -time.npy.  These are in the binary numpy array format, which can be read e.g., by the npyplot.py script provided here, e.g.,
```sh
   python3 npyplot.py test.ini
```

More information on the assignment can be found in the file traffic_module--handout.pdf.

