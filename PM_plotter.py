# -*- coding: utf-8 -*-
"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%    PLOTTER    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

 Plot the results in 3D format, they can be either plot individually or
 in goups of two or four.
 Save the plot in a svg file whose name is the Label of the variable

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
 Inputs:

 V              Potential distribution in the domain
 E              Electric field in the domain
 J              Current density
 rho            Charge density
 nE             Norm of E
 nJ             Norm of J
 plotvar:       List with the variables to be plotted
 Lable:         List of lables for plots
 nx, ny         Number of nodes in the x and y edges if the mesh is 
                structurated

     
 Outputs:

 3D plots of the variables found
 svg files of the plots made


 Nelson José Bayona, Salomón Castaño
 Universidad EAFIT, Sciences Department, Physics Engineering, Numeric Methods
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""

import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D #DO NOT ERREASE
import numpy as np

#Plot one variable in 3D using triangles to shape the surface
def t1_surf(X,Y,Z1,Label):
    fig = plt.figure(figsize=(7,7))
    ax = fig.add_subplot(111, projection='3d')

    surf1 = ax.plot_trisurf(X, Y, Z1, cmap=cm.plasma, linewidth=0.0, \
                    antialiased=False, edgecolor=None, alpha = 1)
    plt.colorbar(surf1, shrink=0.4, aspect=15)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel(Label)
    fig.savefig(Label+'.svg', format='svg', dpi=1200)
    plt.show()

#Plot one variable in 3D using squres to shape the surface 
def q1_surf(x,y,z1,Label,nx,ny):
    X = np.reshape(x, (ny, nx))
    Y = np.reshape(y, (ny, nx))
    Z1 = np.reshape(z1, (ny, nx))
    fig = plt.figure(figsize=(7,7))
    fig.savefig(Label+'.svg', format='svg', dpi=1200)
    ax = fig.add_subplot(111, projection='3d')
    
    surf1 = ax.plot_surface(X, Y, Z1, cmap=cm.plasma, linewidth=0.0, \
                    antialiased=False, edgecolor=None, alpha = 1)
    plt.colorbar(surf1, shrink=0.4, aspect=15)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel(Label)
    fig.savefig(Label+'.svg', format='svg', dpi=1200)   
    plt.show()

#Plot two variables in 3D using squres to shape the surface
def q2_surf(x,y,z1,col1,z2,col2,Label1,Label1c,Label2,Label2c,nx,ny):
    X = np.reshape(x, (ny, nx))
    Y = np.reshape(y, (ny, nx))
    Z1 = np.reshape(z1, (ny, nx))
    Z2 = np.reshape(z2, (ny, nx))
    col1 = np.reshape(col1, (ny, nx))
    col2 = np.reshape(col2, (ny, nx))
    fig = plt.figure(figsize=(20,10))
    ax = fig.add_subplot(1, 2, 1, projection='3d')
    my_col1 = cm.plasma(col1/np.amax(col1))
    my_col2 = cm.plasma(col2/np.amax(col2))
    
    surf1 = ax.plot_surface(X, Y, Z1, facecolors = my_col1, cmap=cm.plasma, linewidth=0.5, \
                    antialiased=False, edgecolor='w', alpha = 1)
    clb = plt.colorbar(surf1, shrink=0.4, aspect=15)
    clb.set_label(Label1c, labelpad=-40, y=1.1, rotation=0)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel(Label1)
    
    ax = fig.add_subplot(1, 2, 2, projection='3d')
    surf2 = ax.plot_surface(X, Y, Z2, facecolors = my_col2, cmap=cm.plasma, linewidth=0.0, \
                    antialiased=False, edgecolor=None, alpha = 1)
    clb = plt.colorbar(surf2, shrink=0.4, aspect=15)
    clb.set_label(Label2c, labelpad=-40, y=1.1, rotation=0)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel(Label2)
    fig.savefig(Label1+Label2+'.svg', format='svg', dpi=1200) 
    plt.show()

#Plot four variables in 3D using triangles to shape the surface
def t4_surf(X,Y,Z1,Z2,Z3,Z4,Label1,Label2,Label3,Label4):
    fig = plt.figure(figsize=(20,10))
    ax = fig.add_subplot(2, 2, 1, projection='3d')

    surf1 = ax.plot_trisurf(X, Y, Z1, cmap=cm.plasma, linewidth=0.0, \
                    antialiased=False, edgecolor=None, alpha = 1)
    plt.colorbar(surf1, shrink=0.4, aspect=15)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel(Label1)
    
    ax = fig.add_subplot(2, 2, 2, projection='3d')
    surf2 = ax.plot_trisurf(X, Y, Z2, cmap=cm.plasma, linewidth=0.0, \
                    antialiased=False, edgecolor=None, alpha = 1)
    plt.colorbar(surf2, shrink=0.4, aspect=15)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel(Label2)
    plt.show()
    
    ax = fig.add_subplot(2, 2, 3, projection='3d')
    surf3 = ax.plot_trisurf(X, Y, Z3, cmap=cm.plasma, linewidth=0.0, \
                    antialiased=False, edgecolor=None, alpha = 1)
    plt.colorbar(surf3, shrink=0.4, aspect=15)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel(Label3)
    plt.show()
    
    ax = fig.add_subplot(2, 2, 4, projection='3d')
    surf4 = ax.plot_trisurf(X, Y, Z4, cmap=cm.plasma, linewidth=0.0, \
                    antialiased=False, edgecolor=None, alpha = 1)
    plt.colorbar(surf4, shrink=0.4, aspect=15)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel(Label4)
    fig.savefig('Group plot.svg', format='svg', dpi=1200)
    plt.show()