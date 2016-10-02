# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 23:22:56 2016

@author: Onur Koc
"""

import numpy as np
import matplotlib.pyplot as plt
#import seaborn
import Rock_Support_Curve_V3 as rs
#from mpldatacursor import datacursor #optional to annotate any clicked point
#get_ipython().magic('matplotlib qt')
# Needed for ipython to draw in a seperate window

# ------------
# Input values
# ------------

rate = 3
# Advance rate [m/day]

# -------------------------------------------------------
# The strength of the concrete (time+dependent behavior)
# -------------------------------------------------------

def strength(t):
    if t <= 8:
        return rs.f_ck * 0.03 * t
    else:
        return rs.f_ck*np.sqrt((t-0.212)/(116+0.841*t))

t = np.arange(0, 48, 1)
# Time from zero to 672h (28 days)

f_str = []
f_str = [strength(i) for i in t]

p_scmax = []
p_scmax = [f_str[i] * rs.t_c / rs.r_o for i in t]
# The maximum sprayed concrete pressure [MPa]

x = rs.dis_sup + rate * t / 24
# Distance from tunnel face (a time-dependent array) [m]

# A_b = -0.22*rs.nu + 0.81
# B_b = 0.39*rs.nu + 0.65
# u_ix = rs.u_if + rs.u_im * A_b * (1 - (B_b / (A_b + x / rs.r_o))**2)
# Unlu and Gercek
u_ix = rs.u_im*(1-(1-rs.u_if/rs.u_im)*np.exp(-3*x/(2*rs.r_pm)))
# Vlachopoulos

# u_ix = rs.u_if + (rs.u_im-rs.u_if) * (1-(0.84*rs.r_pm/(x + 0.84*rs.r_pm))**2)
# Tunnel wall displacement behind the face (x > 0) [m] (Panet)

# ------------------
# Plotting utilities
# ------------------

plt.figure(num=1, dpi=125, edgecolor='b')
fig = plt.gcf()
fig.canvas.set_window_title('Support Resistance')
plt.plot(u_ix, p_scmax, 'r-', lw=1.5)
plt.plot(rs.x, rs.p_i/1000, 'b-', lw=1.5)
plt.plot(rs.point_x, rs.point_y, 'y-', lw=1.5)
plt.title('Time dependent support resistance')
plt.ylabel('Support Pressure $P_i\,[MPa]$', fontsize=12)
plt.xlabel('Displacement $x\,[m]$', fontsize=12)
#datacursor(display='multiple', draggable=True)

plt.figure(num=2, dpi=125, edgecolor='b')
plt.plot(t, f_str, 'b-', lw=1.5)
plt.title('Strengt development over time')
plt.ylabel('Strength $f_{ck}\,[MPa]$', fontsize=12)
plt.xlabel('Time $t\,[h]$', fontsize=12)
#datacursor(display='multiple', draggable=True)
plt.show()
