# Parallelizing the 1-Dim Nagel-Schreckenberg Traffic Model


## The Nagel-Schreckenberg traffic model

The Nagel-Schreckenberg traffic model [@nagel1992cellular] is a 1D toy
model used to generate traffic-like behaviour.
This model is simple enough to avoid getting distracted with the details of its
abstraction but to nonetheless demonstrate interesting emerging properties,
such as congestion or stagnation points.

To describe the details of this model we will use dimensionless quantities,
meaning that position, velocity and time, all have the same "units".

The model in this case is 1-dimensional (1-D), which means that there is
only one spatial coordinate, which denotes the position of the cars along it.
In the model, each car has a position $x$ and a velocity $v$ which evolve in
time as follows:

 1. If the velocity $v$ is below a maximum velocity, $v_{max}$,
		then increase $v$ by 1 (try to speed up).

 2. If the car in front of the given car is at distance $d$ away,
		and $v \ge d$, then reduce $v$ to $d-1$  -- we don't want to hit the car.

 3. Add **randomness**:
		if $v>0$ then with probability *p* the car reduces its speed by 1.

 4. The car moves ahead by $v$ steps (on a circular track).


These four rules can be summarized as,
$$\left\{
\begin{array}{l c l}
	 v  & \leftarrow &  \min\left(v+1,v_{max}\right)	\\
	 v  & \leftarrow &  \min\left(v,d-1\right)		\\
	 v  & \leftarrow &  \left(0,v-1\right)	\text{ with probability } p	\\
	 x  & \leftarrow &  x + v
\end{array}
\right.
$$

where $\leftarrow$ means that the quantity on the left side of the arrow is
updated with the prescription on the right side of it.

Hence, this model can be fully characterized by the following parameters:

  * $v_{max}$,	maximum allowed velocity;
  * $N$,	number of cars on the model;
  * $L$,	length of the road/track;
  * $p$,	threshold probability to decrease current velocity.


In case you are not familiar with using randomness -- the ideas, concepts and
algorithms are quite complex and involved, and a topic of ongoing
research efforts.
But in this particular case, it can be done in a relatively
straightforward way:

 - Draw a random number $r$ using a PRNG with uniform distribution on $[0, 1)$.

 - For any chosen value $p \in [0, 1)$, the chance that $r$ is less than that value, is $p$ itself.

 - So if $r$ is less than $p$, we will accept the move and decrease $v$ if possible.

 - If $r$ is greater than or equal to $p$, we leave $v$ as it is, i.e., we reject the move.


It should be also noted that without the inclusion of *randomness* in the model
(i.e. rule \#3), the model would be deterministic, i.e. the cars will all
evolve preserving the pattern as is set in the initial configuration.

Although this is a simple model, it has very rich dynamics and emerging
properties, and has been used as foundations for more comprehensive models.


## Starter Code

For this assignment we provide a starter serial code, which can be found in
the following repository:

	https://github.com/Practical-Scientific-and-HPC-Computing/Traffic_EduHPC-23



The code simulates the dynamics of the Nagel-Schreckenberg traffic model
for a set of cars that start from random positions on a road with periodic
boundary conditions.
This periodic boundary condition can be thought of as an approximation of a very long road, or as a circular road (i.e., a round-about). It implies that there is no incoming and outgoing motion of vehicles.

The code generates three files in the numpy array format, with their names given
by the `outputprefix` parameter from the parameter file.
For instance, if `outputprefix` is set to 'traffic', the files 'traffic-dens.npy', 'traffic-time.npy' and 'traffic-velo.npy',
will contain the resulting positions, time and velocity of the cars for the simulation.

The code takes its simulation parameters from a parameter file which is specified
as a command line argument.
The parameter is a plain-text file containing the following parameters: 


```sh
L = number of positions in the road (e.g. 500) 
T = total number of time steps (e.g. 500) 
N = number of cars in the road (e.g. 300) 
p = probability of slowing down (e.g. 0.2) 
vmax = maximum velocity (e.g. 2) 
seed = random number seed (e.g. 13) 
outputprefix = prefix for the name of the files to save the data (e.g. "traffic")
per = number of iterations how often output is done (e.g. 10)
```



The code is written in C/C++ using the `C++17` standard.

For Pseudo-Random Number Generation (PRNG) it uses the 'random' library from the
C++ standard library.


We also include a python script `npyplot.py` to visualize the results from the
simulation, which will a generate an image similar to the one shown in Fig.1.

The starter code is located in the `code` directory of this
[repository](https://github.com/Practical-Scientific-and-HPC-Computing/Traffic_EduHPC-23).
The code is written in a modular fashion, with well defined modules to do
specific tasks.

This the full list of files from the `Code` directory:

|  Filename	     | Description				|
|------------------|--------------------------------------------|
| `Makefile`         | make file					|
| `CMakeLists.txt`   | cmake file					|
|------------------|--------------------------------------------|
| `README.md`	   | README file				|
|------------------|--------------------------------------------|
| `test.ini`         | parameter file for testing and reference case	|
| `largetest.ini`    | parameter file for longer and more demanding runs	|
|------------------|--------------------------------------------|
| `reference-test.png`	| image with results from the reference case	|
|------------------|--------------------------------------------|
| `npyplot.py`       | python script for visualizing results from the simulation	|
|------------------|--------------------------------------------|
| `npywriter.cpp`    | writing routine module			|
| `npywriter.h`      |	corresponding header file		|
| `parameters.cpp`   | parsing and processing of parameters module|
| `parameters.h`     | corresponding header file			|
| `traffic.cpp`      | main driver function			|


Most of the relevant code and functions for the assignment
(with the exception of the IO routines) are in the `traffic.cpp` file.



## How to compile and run the code

You need a relatively recent `g++` compiler (version 9 or above), `make` or `cmake` for compilation,
and a `python` 3 installation with `numpy`, `matplotlib`, and `plotly` version 5 or above, to use the `npyplot.py`
script for generating PNG files and generating interactive and HTML visualizations.

To compile the code, type 

```sh
   make 
```

The `Makefile` also contains commands to run and plot results.

To run the smaller test case and plot the results in the form an png files, use

```sh
   make test
```

To run the larger case and plot the results in the form an png files, use

```sh
   make largetest
```

The parameters are set in `.ini` files that can be given as command line arguments, e.g.:
```sh
   ./traffic test.ini
```

Output is in 3 files, two with postfixes `-dens.npy`, `-velo.npy` that contain
the density and velocity of the traffic on a grid at the times stored in the
file with postfix `-time.npy`. 
These are in the binary numpy array format, which can be read e.g., by the
`npyplot.py` script.
This scripts needs the same parameter file as the simulation executable,
so it can identify the resulting files and parameters used in the run, e.g.

```sh
   python3 npyplot.py test.ini
```

The `npyplot.py` script can generate different formats for the plots.
Using a second optional argument to the script, one could generate
PNG (default or `png`), interactive in browser (`interactive`) or HTML (`html`)
formats.
E.g.
```sh
   python3 npyplot.py test.ini interactive
```

#### WARNING
the `interactive` visualization is a *beta* feature and may
not work as expected with large datasets.

---


## IMPORTANT

You should carefully look at the code, it is properly commented and documented.
You must understand the code as many details of the implementation are critical for solving the assignment.

You should note that this is an *agent-based* implementation, i.e., an
implementation that keeps track of the positions and velocities of the $N$ cars
as (two) vectors of length $N$.
An alternative representation, the *grid* representation, which assigns a value
to every point on the road of length $L$ would be another possible way to tackle
this problem, here is only used in the output routines.


Pay utmost attention to the random number generation.
In our implementation, in spite of some of the short coming and disadvantages
it may have compared to other PRNG methods, we use a *multiplicative linear
congruent* generator, due to its ease of implementing a better discard method.

---



# THE ASSIGNMENT:  Parallelize the 1-D Nagel-Schreckenberg Traffic Model

The aim of this assignment is to parallelize the Nagel-Schreckenberg model, for
which we will use the starter code described before.

Your task is as follows:

  1. Speed up this code using **shared-memory parallelism**, by adding OpenMP
directives and thread-safe mechanisms for the pseudo-random number generator.

> Remember to always use `default(none)` in `pragma omp parallel` directives.

> You can start with the often-used approach of having a different seed for the random number generator of each thread, but this will break reproducibility across different number of threads.

> Then, you must pay particular attention to how to treat and deal with the PRNG,
specifically to guarantee the **reproducibility** of the results for the different
implementations.
	I.e. as the *seed* of the PRNG engine is set in the parameter file,
it is expected that for a given seed the results of serial and parallel
runs should match when running on the same hardware independent of the number
of threads used.

> To assess reproducibility, we suggest to use the `test.ini` parameters and visualize the results with
> ```python npyplot.py test.ini```
  

  2. Run a strong scaling analysis for your implementation for the parameters in the `largetest.ini` file for increasing numbers of threads. Set `per=0` in the ini file to focus on how the computation scales.
	If you are running on a HPC system (e.g. supercomputer or cluster),
create a submission script to submit your runs as jobs and automate the
timing measurements.

  3. Make a plot of the speedups as a function of the number of threads. Check if it is possible to estimate the serial fraction $f$ using Amdahl's law.

  4. Create a weak scaling analysis by creating several cases of increasing values of `L` and `N`  that are run with proportionally increasing number of threads.  Create a plot of their runtime vs. number of threads.
  
  5. Write a report based on the outcomes of the scaling analysis and the
results from your previous estimate.

Optional:

  6. Do a performance analysis to determine which parts of the
program are the most expensive ones.

  7. Focus on the I/O functions and look for opportunities
for improvement by parallelizing them. Repeat the scaling analysis now with output enabled.





![Visualization of the reference **test case** included with the starter code. Plots generated using the `npyplot.py` script.](../Code/reference-test.png)


---
