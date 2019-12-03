# -*- coding: utf-8 -*-
"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%    MAIN    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

 Asks the user what geometry will be used
 Sums the contribution of each element and assambles the stiffness matrix
 Calculates the primary and secondary variables
 Exports the results in VTK

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
 Inputs:

 cap:          Mesh type:
                        1: Local structurated mesh
                        2: Externally generated mesh

 Outputs:

 V              Potential distribution in the domain
 E              Electric field in the domain
 J              Current density
 rho            Charge density
 nE             Norm of E
 nJ             Norm of J
 PM_solutions.vtk   File with the obtained variables and elements, nodes and
                    coordinates.

 Salomón Castaño
 Universidad EAFIT, Sciences Department, Physics Engineering, Numeric Methods
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""

import PM_initializer as init
import meshio
from timeit import default_timer
import numpy as np
import PM_functions as fc
import PM_plotter as plot
nx = 0
ny = 0
epsilon = 1

#%% choose a geometry
print('\nWhat kind of mesh is to be used? \n1. Local structurated mesh \
      \n2. Externally generated mesh')
ini = int(input("Write the associated number "))
#ini = 2
stage = 0
while stage == 0:
    if ini == 1:
        tic, element, pts, conductivity, B_nodes, b_global, nx, ny, mesh, Label, plotvar = init.structured()
        stage = 1
    if ini == 2:
        tic, element, pts, conductivity, B_nodes, b_global, mesh, Label, plotvar = init.unstructured()
        stage = 1
    if ini != 1 and ini != 2:
        ini = int(input("The number entered is out of range, please rentered it "))

toc_ini = default_timer()

#%% Sums the contribution of each element to the energy in the capacitor

num_e = len(element)/50
cont = num_e
j = 1
print('\nProgress                                      End')
k_global = np.zeros((len(pts),len(pts)))
for i, nodes in enumerate(element):
    nn = len(nodes)
    X = pts[nodes] #Position of the element nodes
    cond_nodes = conductivity[nodes] #conductivity in nodes of the element
    k_local = fc.gauss_integrate(cond_nodes, X, nn)
    for n in range(nn):
        for m in range(nn):
            k_global[nodes[n],nodes[m]] += k_local[n,m]
    if i > cont:
        j += 1
        print("%", end = '')
        cont = j*num_e
print('\n')
for node in B_nodes:
    k_global[node,:] = np.zeros(len(pts))
    k_global[node,node] = 1
x = pts[:,0]
y = pts[:,1]

toc_assem = default_timer()

V = np.linalg.solve(k_global,b_global)

toc_solve = default_timer()

#%% Post-processing

E = np.zeros((len(pts),2))
grad_cond = np.zeros((len(pts),2))
m = np.zeros(len(pts))
r = np.array([-1, 1, 1, -1])
s = np.array([-1, -1, 1, 1])
border = []
#The electric field E and current density J are calculated
for nodes in element:
    X = pts[nodes] #Position of the element nodes
    Voltage_nodes = V[nodes] #conductivity in nodes of the element.
    cond_nodes = conductivity[nodes] #conductivity in nodes of the element
    i = 0
    for i, node in enumerate(nodes):
        m[node] += 1
        E[node,:] += fc.operators(Voltage_nodes, X, r[i], s[i])[-1]
        grad_cond[node,:] += fc.operators(cond_nodes, X, r[i], s[i])[-1]

#Calculate the charge density rho and the norm of E and J
nJ = np.zeros(len(pts))
nE = np.zeros(len(pts))
rho = np.zeros(len(pts))
J = np.zeros((len(pts),2))
for i, field_node in enumerate(E):
    E[i,:] = E[i,:]/m[i]
    grad_cond[i,:] = grad_cond[i,:]/m[i]
    J[i,:] = (conductivity[i])*field_node
    nJ[i] = (np.dot(J[i,:],J[i,:]))**0.5
    nE[i] = (np.dot(E[i,:],E[i,:]))**0.5
    rho[i] = np.dot(grad_cond[i,:],E[i,:])/(conductivity[i])*epsilon

#Export results in vtk file
zeros = np.zeros((len(pts),1))
mesh.point_data["electrostatic_potential"] = V
mesh.point_data["norm_electrostatic_field"] = nE
mesh.point_data["charge_density"] = rho
mesh.point_data["norm_current_density"] = nJ
mesh.field_data["electrostatic_field"] = np.append(E, zeros, axis=1)
mesh.field_data["current_density"] = np.append(J, zeros, axis=1)
meshio.write("PM_solutions.vtk", mesh)

toc_post = default_timer()

#%% Display results
#plot results
if ini == 1:
    for i in range(len(Label)):
        if plotvar[i] == 'GP':
            plot.t4_surf(x,y,nJ,rho,V,nE,'Current density','Charge density',\
                         'Voltage','Electric field')
        else:
            plot.q1_surf(x,y,eval(plotvar[i]),Label[i],nx,ny)
else:
    for i in range(len(Label)):
        if plotvar[i] == 'GP':
            plot.t4_surf(x,y,nJ,rho,V,nE,'Current density','Charge density',\
                         'Voltage','Electric field')
        else:
            plot.t1_surf(x,y,eval(plotvar[i]),Label[i])
toc = default_timer() #Record the ending time

#Display computation times
print('\nSimulation time:     ', toc - tic,'s')
print('Initialization time: ', toc_ini - tic,'s')
print('Assembly time:       ', toc_assem - toc_ini,'s')
print('Solving time:        ', toc_solve - toc_assem,'s')
print('Postprocessing time: ', toc_post - toc_solve,'s')
print('Plotting time:       ', toc - toc_post,'s')
