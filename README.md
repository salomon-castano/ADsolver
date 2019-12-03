# ADsolver

ADsolver is a FEM solver that can deal with electromagnetic problems related to conduction in lossy dielectrics. It can be used to approximate the **electric potential, electric field, charge density and current density** within a bidimensional geometry with Dirichlet or Neumann homogeneous border conditions. It does not have a graphic interphase nor preprocessing neither postprocessing routines, so it is recommended to use Gmesh to create the mesh and Paraview to visualize the results. Below the utilization of the software is shortly explained.

## Meshing
There are two ways to mesh: externally and within the software. If an externally generated mesh is being used, then it is important have in account two things:
* All elements must of "quad" type.
* All the borders must be defined as physical groups with an ordered numerical tag that ranges from 1 to n, being n the number of borders.

## Initialization files
For initialization a .init file is needed. There are two types of .init files, for internally generated mesh and for importing external meshes. Below, a template for importing an external mesh is shown and its parts are explained:
```
          EXTERNAL MESH INITIALIZATION FILE
Meshfile:                          square_1x1_400_nodes.msh
Conductivity:                      x**10*np.exp(y)+0.0001
Number of boundary conditions:     4
Boundary condition 1:              Neumann Homogeneous BC
Boundary condition 2:              x**2
Boundary condition 3:              2
Boundary condition 4:              Neumann Homogeneous BC
Plots:
    Voltage:             V: true
    Electric field:     nE: true
    Charge density:    rho: true
    Current density:    nJ: true
    Group plot:         GP: false
```
* Meshfile: file that contains the importing mesh
* Conductivity: electrical conductivity of the medium, it can be variable, non elementary functions require numpy and therefore they must be preceded by "np." e.g. np.exp(y).
* Number of boundary conditions: it can be less or equal to the number of borders (physical groups).
* Boundary condition *i*: it is associated to the physical group with tag *i*. It can be variable.
* Plots: indicates to make a quick surface plot of the variable assigned a value of *true* (*Group plot* displays the four variables in the same plot).

The init file for internally generated mesh is very similar but in this case the dimensions of the rectangle (in this case the mesh is mapped) and the number of nodes in a vertical and horizontal edges must be specified in the init file. Below an example is shown.
```
            INTERNAL MESH INITIALIZATION FILE
x length:      12
y length:      10
Number of nodes along the x edge:        13
Number of nodes along the y edge:        11
Conductivity:                      x + 1
Boundary condition 1:              Neumann Homogeneous BC
Boundary condition 2:              y-1
Boundary condition 3:              Neumann Homogeneous BC
Boundary condition 4:              1-y
Plots:
    Voltage:             V: true
    Electric field:     nE: true
    Charge density:    rho: true
    Current density:    nJ: true
    Group plot:         GP: false
```
Once finished the mesh and initialization files, the *PM_main.py* file can be ran to obtain the simulation results.

## Postprocessing

The results are automatically exported in a vtk file named *PM_solutions.vtk*, this file can be read in almost every visualization software. Also, images from the selected plots are automatically saved under the name of the variable plotted in svg files.
