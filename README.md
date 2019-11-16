# ADsolver

ADsolver is a FEM solver that can deal with electromagnetic problems related to conduction in lossy dielectrics. It can be used to approximate the **electric potential, electric field, charge density and current density** within a bidimensional geometry with Dirichlet or Neumann homogeneous border conditions. It does not have a graphic interphase nor preprocessing neither postprocessing routines so it is recommended to use Gmesh to create the mesh and Paraview to visualize the results. Below the utilization of the software is shortly explained.

## Meshing:
There are two ways to mesh: externally and within the software. If an externally generated mesh is being used then it is important have in acount two things:
* All elements must of "quad" type.
* All the borders must be defined as physical groups with oredered numerecal tag that ranges from 1 to n, being n the number of borders.

## Initializtion files
For initilization a .init file is needed. There are two types of .init files, for internally generated mesh and for importing external meshes. Below, a template for importing a extarnal mesh is shown and its parts are explained:
```
          EXTERNAL MESH INITIALIZATION FILE
Meshfile:                          square_1x1_400_nodes.msh
Conductivity:                      x**10*np.exp(y)+0.0001
Number of boundary conditions:     4
Boundary condition 1:              Neumann Homogeneuos BC
Boundary condition 2:              1
Boundary condition 3:              2
Boundary condition 4:              Neumann Homogeneuos BC
Plots:
    Voltage:             V: true
    Electric field:     nE: true
    Charge density:    rho: true
    Current density:    nJ: true
    Group plot:         GP: false
```
* Meshfile: file that conteins the importing mesh
* Conductivity: Electrical conductivity of the medium, it can be variable, non elementary functions require numpy and therefore they must be preceded by "np.".
* Number of boudary conditions: ...it's rather obvious.
* Boundary condition *i*: It corresponds to the physical group with tag *i*. It can be variable.
* Plots: Indicates to make a quick surface plot of the variable assignated a value of *true* 
