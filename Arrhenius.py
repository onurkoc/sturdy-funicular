# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 2016
 
@author: onur koc
"""

import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate
import Rock_Support_Curve_V3 as rs

def hydration_degree (ksi, time):
    """Define the right hand-side of the the ode"""
    
    a, b, c, d, f = 3.2469, 51.9501, 509.7504, 5.1950, 0.086
    # Coefficients of the chemical affinity
    
    Af = a * ((1 - np.exp(-b * (ksi - f))) / (1 + c * (ksi - f) ** d))
    # Chemical affinity
    
    E_a = 4000
    # Activation energy [K]
    
    R = 1
    # Universal gas constant
    
    T_o = 25
    # Initial temperature
    
    T = 273.15 + T_o
    # Absolute temperature
    
    return Af * np.exp(-E_a / (R * T))

def comp_str (ksi, fc_inf):
    """Development of compressive strength in time"""
    
    ksi_0 = 0.01
    # Initial hydration degree

    return (ksi - ksi_0) / (1 - ksi_0) * fc_inf

def elasticity (ksi, E_inf):
    """Development of Young's modulus in time"""

    return E_inf * np.sqrt(ksi)

s2d = 24 * 60 * 60
# One day in seconds

t1y = 28 * s2d
# Time in days

time = np.linspace(0.0, t1y, 100)
# Time variable discretized

E_inf = rs.E_c
# Elasticity at infinity [MPa]

fc_inf = rs.f_ck
# Strength at infinity [MPa]

ksi_init = 0.1
# Initial hydration at t = 0

hyd = scipy.integrate.odeint(hydration_degree, ksi_init, time)
# Solve the hydration-ODE
    
fc_t = comp_str(hyd, fc_inf)
# Calling strength function

E_ = elasticity(hyd, E_inf)
# Calling elasticity function

if __name__ == "__main__":
    
    plt.figure(num=1, dpi=125, edgecolor='b')
    plt.plot(time/s2d, hyd, 'go-', markersize=3)
    plt.title('$Hydration\ Degree$', fontsize=13)
    plt.xlabel('$t\ [days]$', fontsize=12)
    plt.ylabel('$\\xi$', fontsize=12)

    plt.figure(num=2, dpi=125, edgecolor='b')
    plt.plot(time/s2d, fc_t)
    plt.title('$Strength\ Development$', fontsize=13)
    plt.xlabel('$t\ [days]$', fontsize=12)
    plt.ylabel('$f_c\ [MPa]$', fontsize=12)

    plt.figure(num=3, dpi=125, edgecolor='b')
    plt.plot(time/s2d, E_)
    plt.title('$Elasticity\ Development$', fontsize=13)
    plt.xlabel('$t\ [days]$', fontsize=12)
    plt.ylabel('$E\ [MPa]$', fontsize=12)
