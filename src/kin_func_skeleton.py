#!/usr/bin/env python
"""Kinematic function skeleton code for Prelab 3.
Course: EE 106A, Fall 2015
Written by: Aaron Bestick, 9/10/14
Used by: EE106A, 9/11/15

This Python file is a code skeleton for Pre lab 3. You should fill in 
the body of the eight empty methods below so that they implement the kinematic 
functions described in the homework assignment.

When you think you have the methods implemented correctly, you can test your 
code by running "python kin_func_skeleton.py at the command line.

This code requires the NumPy and SciPy libraries. If you don't already have 
these installed on your personal computer, you can use the lab machines or 
the Ubuntu+ROS VM on the course page to complete this portion of the homework.
"""

import numpy as np
import pylab as pl
from pylab import linalg
#import scipy as sp
#from scipy.linalg import expm
from math import cos, sin, sqrt
np.set_printoptions(precision=4,suppress=True)

def skew_3d(omega):
    """
    Converts a rotation vector in 3D to its corresponding skew-symmetric matrix.
    
    Args:
    omega - (3,) ndarray: the rotation vector
    
    Returns:
    omega_hat - (3,3) ndarray: the corresponding skew symmetric matrix
    """
    if not omega.shape == (3,):
        raise TypeError('omega must be a 3-vector')
    
    omega_hat = np.array([[0, -omega[2], omega[1]], [omega[2], 0, -omega[0]], [-omega[1], omega[0], 0]])

    return omega_hat

def rotation_2d(theta):
    """
    Computes a 2D rotation matrix given the angle of rotation.
    
    Args:
    theta: the angle of rotation
    
    Returns:
    rot - (3,3) ndarray: the resulting rotation matrix
    """
    
    rot = np.array([[cos(theta), -sin(theta)], [sin(theta), cos(theta)]])

    return rot

def rotation_3d(omega, theta):
    """
    Computes a 3D rotation matrix given a rotation axis and angle of rotation.
    
    Args:
    omega - (3,) ndarray: the axis of rotation
    theta: the angle of rotation
    
    Returns:
    rot - (3,3) ndarray: the resulting rotation matrix
    """
    if not omega.shape == (3,):
        raise TypeError('omega must be a 3-vector')
    
    i_d = np.eye(3)
    norm = sqrt(omega[0]**2+omega[1]**2+omega[2]**2)
    k = np.array([[0, -omega[2], omega[1]], [omega[2], 0, -omega[0]], [-omega[1], omega[0], 0]])
    k2 = np.dot(k,k)
    rot = i_d + sin(norm*theta)*k/norm + (1 - cos(norm*theta))*k2/(norm*norm)
    #print(rot)
    return rot

def hat_2d(xi):
    """
    Converts a 2D twist to its corresponding 3x3 matrix representation
    
    Args:
    xi - (3,) ndarray: the 2D twist
    
    Returns:
    xi_hat - (3,3) ndarray: the resulting 3x3 matrix
    """
    if not xi.shape == (3,):
        raise TypeError('omega must be a 3-vector')

    #CODE HERE
    xi_hat = np.array([[0, -xi[2], xi[0]], 
                      [xi[2], 0, xi[1]], 
                      [0, 0, 0]])
    return xi_hat

def hat_3d(xi):
    """
    Converts a 3D twist to its corresponding 4x4 matrix representation
    
    Args:
    xi - (6,) ndarray: the 3D twist
    
    Returns:
    xi_hat - (4,4) ndarray: the corresponding 4x4 matrix
    """
    if not xi.shape == (6,):
        raise TypeError('xi must be a 6-vector')

    xi_hat = np.array([[0, -xi[5], xi[4], xi[0]],
                       [xi[5], 0, -xi[3], xi[1]],
                       [-xi[4], xi[3], 0, xi[2]],
                       [0, 0, 0, 0]])
    #print(xi_hat)
    return xi_hat

def homog_2d(xi, theta):
    """
    Computes a 3x3 homogeneous transformation matrix given a 2D twist and a 
    joint displacement
    
    Args:
    xi - (3,) ndarray: the 2D twist
    (2,1,3)
    theta: the joint displacement
    0.658
    ret_desired = np.array([[-0.3924, -0.9198,  0.1491],
                         [ 0.9198, -0.3924,  1.2348],
                         [ 0.    ,  0.    ,  1.    ]])
    Returns:
    g - (3,3) ndarray: the resulting homogeneous transformation matrix
    """
    if not xi.shape == (3,):
        raise TypeError('xi must be a 3-vector')

    #YOUR CODE HERE
    g = np.eye(3)
    r = rotation_2d(xi[2]*theta)
    w = xi[2]
    p1 = np.array([[1 - cos(w*theta), sin(w*theta)], [-sin(w*theta), 1 - cos(w*theta)]]) 
    p2 = np.array([[0, -1], [1, 0]])
    p3 = np.array([[xi[0]/w], [xi[1]/w]])
    p = linalg.dot(linalg.dot(p1,p2),p3)
    g[0:2,0:2] = r
    g[0:2,2] = np.transpose(p)
    #print g
    #print omega
    #g = expm(omega*theta)
    return g

def homog_3d(xi, theta):
    """
    Computes a 4x4 homogeneous transformation matrix given a 3D twist and a 
    joint displacement.
    
    Args:
    xi - (6,) ndarray: the 3D twist
    theta: the joint displacement
    arg1 = np.array([2.0, 1, 3, 5, 4, 2])
    arg2 = 0.658
        ret_desired = np.array([[ 0.4249,  0.8601, -0.2824,  1.7814],
                            [ 0.2901,  0.1661,  0.9425,  0.9643],
                            [ 0.8575, -0.4824, -0.179 ,  0.1978],
                            [ 0.    ,  0.    ,  0.    ,  1.    ]])
    Returns:
    g - (4,4) ndarary: the resulting homogeneous transformation matrix
    """
    if not xi.shape == (6,):
        raise TypeError('xi must be a 6-vector')
    g = np.eye(4)
    r = rotation_3d(xi[3:6], theta)
    #rint omega
    norm = xi[3]**2+xi[4]**2+xi[5]**2
    i = np.eye(3)
    left1 = i - r
    omega = xi[3:6]
    v = xi[0:3]
    omegahat = skew_3d(omega)
    left2 = np.dot(omegahat,v)
    left = np.dot(left1,left2)
    right2 = np.dot(np.transpose(omega),v)
    right = theta * np.dot(omega,right2)
    #print left, right
    p = left + right
    p = p / norm
    #print p
    g[0:3,0:3] = r
    g[0:3, 3] = np.transpose(p)
    #print g
    #print g
    return g

def prod_exp(xi, theta):
    """
    Computes the product of exponentials for a kinematic chain, given 
    the twists and displacements for each joint.
    
    Args:
    xi - (6,N) ndarray: the twists for each joint
    theta - (N,) ndarray: the displacement of each joint
    
    Returns:
    g - (4,4) ndarray: the resulting homogeneous transformation matrix
    """
    if not xi.shape[0] == 6:
        raise TypeError('xi must be a 6xN')
    g = np.eye(4)
    j = np.shape(xi)[1]
    for x in range(j):
        h = homog_3d(xi[0:6,x], theta[x])
        g = np.dot(g, h)
    #YOUR CODE HERE

    return g

def forward_kinematics(ji):
    """
    Computes the product of exponentials for a kinematic chain, given 
    the twists and displacements for each joint.
    
    Args:
    ji - (6,7) ndarray: the twists for each joint
    
    Returns:
    g - (4,4) ndarray: the resulting homogeneous transformation matrix
    """
    if not xi.shape[0] == 6:
        raise TypeError('ji must be a 6xN')
    if not xi.shape[1] == 7:
        raise TypeError('ji must be a Nx7')

    h = prod_exp(ji, 0)
    return h

#-----------------------------Testing code--------------------------------------
#-------------(you shouldn't need to modify anything below here)----------------

def array_func_test(func_name, args, ret_desired):
    ret_value = func_name(*args)
    if not isinstance(ret_value, np.ndarray):
        print('[FAIL] ' + func_name.__name__ + '() returned something other than a NumPy ndarray')
    elif ret_value.shape != ret_desired.shape:
        print('[FAIL] ' + func_name.__name__ + '() returned an ndarray with incorrect dimensions')
    elif not np.allclose(ret_value, ret_desired, rtol=1e-3):
        print('[FAIL] ' + func_name.__name__ + '() returned an incorrect value')
    else:
        print('[PASS] ' + func_name.__name__ + '() returned the correct value!')

if __name__ == "__main__":
    print('Testing...')

    #Test skew_3d()
    arg1 = np.array([1.0, 2, 3])
    func_args = (arg1,)
    ret_desired = np.array([[ 0., -3.,  2.],
                            [ 3., -0., -1.],
                            [-2.,  1.,  0.]])
    array_func_test(skew_3d, func_args, ret_desired)

    #Test rotation_2d()
    arg1 = 2.658
    func_args = (arg1,)
    ret_desired = np.array([[-0.8853, -0.465 ],
                            [ 0.465 , -0.8853]])
    array_func_test(rotation_2d, func_args, ret_desired)

    #Test rotation_3d()
    arg1 = np.array([2.0, 1, 3])
    arg2 = 0.587
    func_args = (arg1,arg2)
    ret_desired = np.array([[-0.1325, -0.4234,  0.8962],
                            [ 0.8765, -0.4723, -0.0935],
                            [ 0.4629,  0.7731,  0.4337]])
    array_func_test(rotation_3d, func_args, ret_desired)

    #Test hat_2d()
    arg1 = np.array([2.0, 1, 3])
    func_args = (arg1,)
    ret_desired = np.array([[ 0., -3.,  2.],
                         [ 3.,  0.,  1.],
                         [ 0.,  0.,  0.]])
    array_func_test(hat_2d, func_args, ret_desired)

    #Test hat_3d()
    arg1 = np.array([2.0, 1, 3, 5, 4, 2])
    func_args = (arg1,)
    ret_desired = np.array([[ 0., -2.,  4.,  2.],
                            [ 2., -0., -5.,  1.],
                            [-4.,  5.,  0.,  3.],
                            [ 0.,  0.,  0.,  0.]])
    array_func_test(hat_3d, func_args, ret_desired)

    #Test homog_2d()
    arg1 = np.array([2.0, 1, 3])
    arg2 = 0.658
    func_args = (arg1,arg2)
    ret_desired = np.array([[-0.3924, -0.9198,  0.1491],
                         [ 0.9198, -0.3924,  1.2348],
                         [ 0.    ,  0.    ,  1.    ]])
    array_func_test(homog_2d, func_args, ret_desired)

    #Test homog_3d()
    arg1 = np.array([2.0, 1, 3, 5, 4, 2])
    arg2 = 0.658
    func_args = (arg1,arg2)
    ret_desired = np.array([[ 0.4249,  0.8601, -0.2824,  1.7814],
                            [ 0.2901,  0.1661,  0.9425,  0.9643],
                            [ 0.8575, -0.4824, -0.179 ,  0.1978],
                            [ 0.    ,  0.    ,  0.    ,  1.    ]])
    array_func_test(homog_3d, func_args, ret_desired)

    #Test prod_exp()
    arg1 = np.array([[2.0, 1, 3, 5, 4, 6], [5, 3, 1, 1, 3, 2], [1, 3, 4, 5, 2, 4]]).T
    arg2 = np.array([0.658, 0.234, 1.345])
    func_args = (arg1,arg2)
    ret_desired = np.array([[ 0.4392,  0.4998,  0.7466,  7.6936],
                            [ 0.6599, -0.7434,  0.1095,  2.8849],
                            [ 0.6097,  0.4446, -0.6562,  3.3598],
                            [ 0.    ,  0.    ,  0.    ,  1.    ]])
    array_func_test(prod_exp, func_args, ret_desired)
   
    """#Test forward_kinematics
    arg1 = np.array([[0.0635, 0.2598, 0.118, -0.0059, 0.0113, 0.9999], 
                     [0.1106, 0.3116, 0.3885, -0.7077, 0.7065, -0.0122], 
                     [0.1827, 0.3838, 0.3881, 0.7065, 0.7077, -0.0038],
                     [0.3682, 0.5684, 0.3181, -0.7077, 0.7065, -0.0122],
                     [0.4417, 0.6420, 0.3177, 0.7065, 0.7077, -0.0038],
                     [0.6332, 0,8337, 0.3067, -0.7077, 0.7065, -0.0122],
                     [0.7152, 0.9158, 0.3063, 0.7065, 0.7077, -0.0038]]).T
    func_args = (arg1,)"""
    print('Done!')
