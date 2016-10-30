# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 20:46:08 2016

@author: Onur Koc

Purpose: Calculation of the total mechanical compliance (Totale mechanische
         Nachgiebigkeit) in terms of hydration grade - J_tot
         J_tot = J_el + J_v (short term) + J_f (long term)
         
"""

import Arrhenius as arr
import numpy as np
import matplotlib.pyplot as plt
import seaborn

s1d = 24 * 60 * 60
# One day in seconds

t1y = 365 * s1d
# One year in seconds

t1w = 7 * s1d
# One year in seconds

t_0 = s1d
# Initial time instance taken as one day

time = np.linspace(t_0, t1w, 100)
# Time variable discretized

E_1d = arr.elasticity(t_0)
# Young's modulus after one day

J_el = 1 / E_1d
# Elastic term of total compliance
# This value is not variable dependent for that reason it is not defined 
# as a function

def comp_longterm (time):
    """Long term compliance in terms of time"""
    
    H_ = (1.0 / 7.0) * 10**6
    # Softening modulus for flow creep [MPa]
    
    try:
        return 1.0 / H_ * np.log(time/t_0)
    except ZeroDivisionError:
        pass
    
def comp_shortterm (hyd):
    """Short term compliance in terms of hydration grade"""
    
    J_vinf = 127.0 * 10**(-6)
    # Viscous compliance - meaning: short term compliance at infinity
    
    try:
        return J_vinf * (1 - hyd)
    except ZeroDivisionError:
        pass

J_f = comp_longterm(time) * 10**6
# Calling the function with the time variable defined in Arrhenius module

J_v = comp_shortterm(arr.hyd) * 10**6
# Calling the function with the hydration grade variable defined in Arrhenius
# module

J_tot = np.add(J_f, J_v)
# Total compliance

plt.figure(num=1, dpi=125, edgecolor='b')
plt.semilogx(time/s1d, J_f)
plt.title('$Total\ Mechanical\ Compliance$', fontsize=13)
plt.xlabel('$t\ [days]$', fontsize=12)
plt.ylabel('$J_{tot}$', fontsize=12)