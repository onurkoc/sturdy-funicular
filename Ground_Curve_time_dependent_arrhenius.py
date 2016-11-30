# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 23:22:56 2016

@author: Onur Koc
"""

import numpy as np
import matplotlib.pyplot as plt
import Rock_Support_Curve_V3 as rs
from mpldatacursor import datacursor #optional to annotate any clicked point
import Arrhenius as arr
import seaborn

# ------------
# Input values
# ------------

rate = 4
# Advance rate [m/day]

# -------------------------------------------------------
# The strength of the concrete (time dependent behavior)
# -------------------------------------------------------

p_scmax = arr.fc_t * rs.t_c / rs.r_o 
# The maximum sprayed concrete pressure [MPa]

x = rs.dis_sup + rate * arr.time / arr.s2d
# Distance from tunnel face (a time-dependent array) [m]

u_ix = rs.u_im*(1-(1-rs.u_if/rs.u_im)*np.exp(-3*x/(2*rs.r_pm)))
# Vlachopoulos

# ------------------
# Plotting utilities
# ------------------
if __name__ == "__main__":
    
    plt.figure(figsize=(12,8), dpi=100)
    fig = plt.gcf() #gcf = get current figure
    fig.canvas.set_window_title('Ground Curve vs. Support Resistance')
    plt.title('Time dependent support resistance')

    plt.subplot(2,2,1)
    ax = plt.gca() #gca = get current axis
    ax.set_xlim([0, 0.7])
    plt.plot(u_ix, p_scmax, 'r-', lw=1.5, label='SpC, NL')
    plt.plot(rs.x, rs.p_i/1000, 'b-', lw=1.5, label='Ground Curve')
    plt.plot(rs.point_x, rs.point_y, 'y-', lw=1.5, label='SpC, LE')
    plt.legend(loc='upper right')
    plt.ylabel('Support Pressure $P_i\,[MPa]$', fontsize=12)
    plt.xlabel('Radial Displacement $x\,[m]$', fontsize=12)
    datacursor(display='multiple', draggable=True)
    
    plt.subplot(2,2,2)
    ax1 = plt.gca() #gca = get current axis
    ax1.set_ylim([0, max(rs.p_i/1000)]) 
    #limit the y-axis to the given values
    plt.plot(arr.time/arr.s2d, p_scmax, color='red', lw=1.5, label='SpC, NL')
    plt.legend(loc='upper right')
    plt.ylabel('Support Pressure $P_i\,[MPa]$', fontsize=12)
    plt.xlabel('$t\ [days]$', fontsize=12)
    datacursor(display='multiple', draggable=True)
    
    plt.subplot(2,2,3)
    ax2 = plt.gca() #gca = get current axis
    ax2.invert_yaxis() #invert the y-axis
    ax2.xaxis.set_ticks_position('top')
    ax2.set_xlim([0, 0.7])
    plt.plot(u_ix, arr.time/arr.s2d * rate, color='olivedrab', lw=1.5, 
             label='SpC, NL')
    plt.legend(loc='lower left')
    plt.ylabel('Distance to face $[m]$', fontsize=12)
    datacursor(display='multiple', draggable=True)

    plt.subplot(2,2,4)
    ax3 = plt.gca() #gca = get current axis
    ax3.invert_yaxis() #invert the y-axis
    ax3.xaxis.set_ticks_position('top')
    plt.plot(arr.time/arr.s2d, arr.time/arr.s2d * rate, color='cadetblue',
             lw=1.5, label='Advance Rate')
    plt.legend(loc='lower left')
    plt.ylabel('Distance to face $[m]$', fontsize=12)
    
    plt.tight_layout(pad=1.5, w_pad=0.5, h_pad=0.5)
    datacursor(display='multiple', draggable=True)
