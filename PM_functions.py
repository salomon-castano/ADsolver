# -*- coding: utf-8 -*-
"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%    FUNCTIONS    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

 J_DT:             Calculates the jacobian and the transpose of the gradient
                   of the form functions matrix
 
 normE2_J:         Calculates the squared norm of the electric field
 
 gauss_integrate:  Integrates using  gaussian integration

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
 Inputs:

 J_DT:             X: points of the element, (ri,sj): point being evaluated in
                   gaussian integral
                   
 normE2_J:         X: points of the element, (ri,sj): point being evaluated in
                   gaussian integral, potential_element: Potential in points 
                   of the element
                   
 gauss_integrate:  X: points of the element, cond_nodes: conductivity in
                   points of the element
                   
 Outputs:

 J_DT:             J: Jacobian, DT: Transpose of the form functions gradient
                   
 normE2_J:         J: Jacobian, nE2: squared norm of the electric field
                   
 gauss_integrate:  U: Guassian integral of the energy over the given element

 Nelson José Bayona, Salomón Castaño
 University EAFIT, Sciences Department, Physics Engineering, Numeric Methods
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""
import numpy as np

# Coordinates and wights of the points to be used in the gaussian integration
r = np.array([-0.861136, -0.339981, 0.339981, 0.861136])
w = np.array([0.347855, 0.652145, 0.652145, 0.347855])


def operators(func_nodes,X,ri,sj):
    phi = 0.25*np.array([(1-ri)*(1-sj), (1+ri)*(1-sj), \
                         (1+ri)*(1+sj), (1-ri)*(1+sj)])
    DT = 0.25*np.array([[sj-1, -sj+1, sj+1, -sj-1], \
                        [ri-1, -ri-1, ri+1, -ri+1]]) #Form functions matrix
    J = DT @ X #Jacobian
    detJ = np.linalg.det(J)
    invJ = np.linalg.inv(J)
    grad = invJ @ DT @ func_nodes #Calculate the gradient
    
    return phi, DT, J, detJ, invJ, grad

def gauss_integrate(cond_nodes, X, m, n):
    a = 0
    for i, ri in enumerate(r):
        for j, sj in enumerate(r):
            phi, DT, J, detJ, invJ, d_cond = operators(cond_nodes, X, ri, sj)
            #Evaluate the funtion to be integrated in point ri,sj and multiply
            #by the given weights
            Dm = invJ @ DT[:,m]
            Dn = invJ @ DT[:,n]
            a += (-np.dot(Dm, Dn) * cond_nodes[n] + phi[n] * np.dot(Dm, \
                  d_cond)) * detJ * w[i] * w[j]
    return a