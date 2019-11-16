# -*- coding: utf-8 -*-
"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%    INICILIZER    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

 Read the initialization file selected by the user setting the given parameters
 Read the vtk or vtu file
 Set the border conditions.
 Assemble the load vector
 Creates the mesh needed for the vtk file

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
 Inputs:

Initialization file
Mesh file (ideally, .msh from Gmesh)

     
 Outputs:

mesh:           Mesh file for exporting in vtk
element:        Conformating points of each element
pts:            Coordenates of each point
conductivity:   Electrical conductivity in the domain
B_nodes:        Border nodes
b_global:       Global load vector
mesh:           Mesh for exporting in vtk
plotvar:        List with the variables to be plotted
Lable:          List of lables for plots
nx, ny          Number of nodes in the x and y edges if the mesh is 
structurated



 Nelson José Bayona, Salomón Castaño
 Universidad EAFIT, Sciences Department, Physics Engineering, Numeric Methods
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""
import meshio
import numpy as np


#%% Read an external mesh
def unstructured():
    datafile = input("Write the initialitation file name (including the extesion) ")
#    datafile = 'unstructured mesh 1.3.init'
    
    #Get the data from the initialization file
    data = []
    with open(datafile) as dataf:
        for line1 in dataf:
            inner_list = [elt.strip() for elt in line1.split(':')]
            data.append(inner_list)
    start0 = 1
    meshfile = data[start0+0][1:][0]
    cond = data[start0+1][1:][0]
    borders = int(data[start0+2][1:][0])
    #Get the border conditions
    BC = []
    for i in range(borders):
        BC.append(data[start0+3+i][1:][0])
        
    #Difine what is to be plotted
    start1 = start0+borders+4
    Label = []
    plotvar = []
    for i in range(5):
        if data[start1+i][2:][0] == 'true':
            Label.append(data[start1+i][0:][0])
            plotvar.append(data[start1+i][1:][0])
    
    # Read the mesh file
    mesh = meshio.read(meshfile) #Read the targetted file
    pts = mesh.points #Store the coordenates of each node
    pts = pts[:,0:2] #Z coordinate is negrected
    element = mesh.cells['quad'] #Store the points of each element
    line = mesh.cells['line'] #Store the points of the border lines
    B_lines = mesh.cell_data['line']['gmsh:physical']
    
    #Applay the border conditions and assemble the load vector
    B_nodes= []
    b_global = np.zeros(len(pts))
    for j in range(borders):
        linej = []
        if BC[j] != 'Neumann Homogeneus BC':
            for i in range(len(B_lines)):
                if B_lines[i] == j+1:
                    linej.append(line[i,:])
            linej = np.array(linej, np.int32)
            linej = np.array(list(set(linej[:,0])|set(linej[:,1])))
            B_function = lambda x, y : eval(BC[j])
            for node in linej:
                B_nodes.append(node)
                b_global[node] = B_function(pts[node,0],pts[node,1])
    B_nodes = list(set(B_nodes))
    
    #Calculate the conductivity in the domain and return the results
    conductivity = np.zeros(len(pts))
    cond_function = lambda x, y : eval(cond)
    for i, points in enumerate(pts):
        conductivity[i] = cond_function(points[0],points[1])
    return element, pts, conductivity, B_nodes, b_global, mesh, Label, plotvar
#%% create a structured mesh
    
def structured():
    datafile = input("Write the initialitation file name (including the extesion) ")
#    datafile = 'structured mesh 1.0.init'
    #Get the data from the initialization file
    data = []
    with open(datafile) as dataf:
        for line1 in dataf:
            inner_list = [elt.strip() for elt in line1.split(':')]
            data.append(inner_list)
    start0 = 1
    a = int(data[start0+0][1:][0])
    b = int(data[start0+1][1:][0])
    nx = int(data[start0+2][1:][0])
    ny = int(data[start0+3][1:][0])
    cond = data[start0+4][1:][0]
    
    #Get the border conditions
    BC0 = data[start0+5][1:][0]
    BC1 = data[start0+6][1:][0]
    BC2 = data[start0+7][1:][0]
    BC3 = data[start0+8][1:][0]
    
    #Difine what is to be plotted
    start1 = 11
    Label = []
    plotvar = []
    for i in range(5):
        if data[start1+i][2:][0] == 'true':
            Label.append(data[start1+i][0:][0])
            plotvar.append(data[start1+i][1:][0])
    
    #Prelocate the variables
    hx = a/(nx - 1)
    hy = b/(ny - 1)
    n = nx*ny
    x = np.zeros(n)
    y = np.zeros(n)
    conductivity = np.zeros(n)
    element = np.zeros(((nx-1)*(ny-1),4)).astype(int)
    B_nodes = []
    fx = np.zeros((nx, 2))
    fy = np.zeros((ny, 2))
    b_global = np.zeros(n)
    x = np.linspace(0,a,nx)   # do not erease! needed for eval(BCi)
    y = np.linspace(0,b,ny)   # do not erease! needed for eval(BCi) 
    
    #Applay the border conditions and assemble the load vector
    if BC0 != 'Neumann Homogeneus BC':
        fx[:,0] = eval(BC0)
        for i in range(0,nx):
            b_global[i] = fx[i,0]
            B_nodes.append(i)
    if BC2 != 'Neumann Homogeneus BC':
        fx[:,0] = eval(BC2)
        for i in range(0,nx):
            l = i + n - nx
            b_global[l] = fx[i,0]
            B_nodes.append(l)
    if BC3 != 'Neumann Homogeneus BC':
        fy[:,1] = eval(BC3)
        for j in range(0,ny):
            i = nx*j
            b_global[i] = fy[j,1]
            B_nodes.append(i)
    if BC1 != 'Neumann Homogeneus BC':
        fy[:,1] = eval(BC1)
        for j in range(0,ny):
            l = nx*j + nx - 1
            b_global[l] = fy[j,1]
            B_nodes.append(l)
    B_nodes = list(set(B_nodes))
    
    #Find the position of the points
    X1 = np.zeros(n)
    Y1 = np.zeros(n)
    pts = np.zeros((n,2))
    m = 0
    for j in range(0,ny):
        for i in range(0,nx):
            Y1[m] = hy*j
            X1[m] = hx*i
            pts[m,:] = [X1[m], Y1[m]]
            m += 1
    
    #Calculate the cnductivity over the given domain
    conductivity = np.zeros(len(pts))
    cond_function = lambda x, y : eval(cond)
    for i, points in enumerate(pts):
        conductivity[i] = cond_function(points[0],points[1])
    
    #Find the nodes belonging to each element
    for j in range(0,ny-1):
        for i in range(0,nx-1):
            p = nx*(j+1) + i
            q = nx*j + i
            element[(nx*j + i -j),:] = [q, q+1, p+1, p]
    
    #Generate the mesh file and return the results
    zeros = np.zeros((len(pts),1))
    mesh = meshio.Mesh(np.append(pts, zeros, axis=1), {"quad": element})
    return element, pts, conductivity, B_nodes, b_global, nx, ny, mesh, Label, plotvar