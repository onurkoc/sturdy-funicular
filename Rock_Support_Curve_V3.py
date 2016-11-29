# coding: utf-8
"""
__author__: onur koc
"""
import numpy as np
import matplotlib.pyplot as plt
import seaborn
from mpldatacursor import datacursor #optional to annotate any clicked point
get_ipython().magic('matplotlib qt')
# Needed for ipython to draw in a seperate window

# ------------
# Input values
# ------------
gamma = 25
# Specific weight of the rock mass [kN/m³]
H = 280
# Overburden [m]
nu = 0.3
# Poisson's ratio of the rock [-]
E = 1800000
# Modulus of elasticity of the rock [kPa]
p_o = gamma * H
# In-situ stress [kPa]
D = 10
# Diameter of the tunnel [m]
c = 1500
# Cohesion of the rock [kPa]
phi = 23
# Friction angle of the rock [deg]
Phi = np.deg2rad(phi)
# Convertion from degrees to radians [rad]

# --------------------------------
# Input values for support members
# --------------------------------

f_ck = 35
# Uniaxial compressive strength of the sprayed concrete [MPa]
E_c = 30000
# Young's modulus of the sprayed concrete [MPa]
nu_c = 0.2
# Poisson's ratio of the sprayed concrete [-]
t_c = 0.3
# Thickness of the sprayed concrete [m]
dis_sup = 1
# Distance of the support member to the face

# Other calculated values

p_i = np.arange(0, p_o, 100)
# Support pressure (an array from zero to insitu stress) [kPa]

sigma_cm = 2 * c * np.cos(Phi) / (1 - np.sin(Phi))
# Uniaxial strength of the rock mass [kPa]
k = (1 + np.sin(Phi)) / (1 - np.sin(Phi))
# Slope defined by the Mohr-Coulomb criterion [-]

# ----------------------------
# Analysis of tunnel behaviour
# ----------------------------

# Tunnel wall displacement

p_cr = (2 * p_o - sigma_cm) / (1 + k)
# Critical support pressure [kPa]
# Note: if the critical support pressure is smaller than the internal
# support pressure then failure does not occur

r_o = D / 2
# Radius of the tunnel [m]

u_ie = r_o * (1 + nu) / E * (p_o - p_i)
# Inward radial elastic displacement (Pi is a variable) [m]

r_p = r_o*(2*(p_o*(k-1)+sigma_cm)/(1+k)/((k-1)*p_i+sigma_cm))**(1/(k-1))
# Radius of the plastic zone [m]

u_ip = r_o*(1+nu)/E*(2*(1-nu)*(p_o-p_cr) * (r_p/r_o)**2-(1-2*nu)*(p_o-p_i))
# Inward radial plastic displacement (Pi is a variable) [m]

x = []

for i in range(len(p_i)):
    if p_i[i] > p_cr:
        x.append(u_ie[i])
    else:
        x.append(u_ip[i])

u_annot = r_o * (1+nu) / E * (p_o-p_cr)
# The abscissa of the ordinate: p_cr


# Logitudinal displacement profile

r_pm = r_o * ((2 * (p_o * (k-1) + sigma_cm)) / ((1+k) * sigma_cm))**(1/(k-1))
# Maximum plastic zone radius [m]

u_im = r_o * (1+nu)/E*(2*(1-nu)*(p_o-p_cr)*(r_pm/r_o)**2-(1-2*nu)*(p_o))
# Maximum displacement [m] - r_p = r_pm; p_i = 0

u_if = (u_im / 3) * np.exp(-0.15 * (r_pm / r_o))
# Displacement at the tunnel face (by Vlachopoulus and Diederichs) [m]

# Displacement ahead of the face

x_ = np.arange(-25, 40, 1)
# Distance from tunnel face (an array from -25m ahead and 40m behind the face)
# [m]

u_ix_a = (u_if) * np.exp(x_ / r_o)
# Tunnel wall displacement ahead of the face (x < 0) [m]

# Displacement behind the face

u_ix_b = u_im*(1-(1-u_if/u_im) * np.exp((-3*x_/r_o) / (2*r_pm/r_o)))
# Tunnel wall displacement behind the face (x > 0) [m]

x__ = []

for i in range(len(x_)):
    if x_[i] < 0:
        x__.append(u_ix_a[i])
    else:
        x__.append(u_ix_b[i])

lambda_face = u_if / u_im

# -----------------------
# Analysis of the support
# -----------------------

# Panet curve
#u_io = u_if + (u_im-u_if) * (1-(0.84*r_pm/(dis_sup + 0.84*r_pm))**2)
# Tunnel wall displacement at support installation [m]

# Vlachopoulus curve is as follows:
u_io = u_im*(1-(1-u_if/u_im) * np.exp((-3*dis_sup/r_o) / (2*r_pm/r_o)))

K_sc = E_c * (r_o**2 - (r_o-t_c)**2) / (2*(1-nu**2)*(r_o-t_c)*r_o**2)
# The stiffness of the sprayed concrete [MPa/m]

p_scmax = f_ck/2 * (1 - (r_o - t_c)**2 / r_o**2)
# The maximum sprayed concrete pressure [MPa]

u_iy = u_io + p_scmax / K_sc
# Yielding point of the sprayed concrete [m]

point_x = [u_io, u_iy, 1.3*u_iy]
point_y = [0, p_scmax, p_scmax]
# Points for the support yield line

if __name__ == "__main__":
    
    fig, ax1 = plt.subplots(num=1, dpi=125, edgecolor='w')
    ax1.plot(x, p_i/1000, lw=1.5, color='blue')
    plt.title('Ground Reaction Curve')
    ax1.set_ylabel('Support Pressure $P_i\,[MPa]$', fontsize=12)
    ax1.set_xlabel('Tunnel Wall Displacement $u_i\,[m]$', fontsize=12)
    for tl in ax1.get_yticklabels():
        tl.set_color('b')
    
    ax2 = ax1.twinx()
    ax2.plot(x__, x_, lw=1.5, color='red')
    ax2.set_ylabel('Distance from tunnel face $x\,[m]$', fontsize=12)
    # ax2.axhline(y=0, xmin=u_if, xmax=0.045, color='black')
    for tl in ax2.get_yticklabels():
        tl.set_color('r')
    xposition = [u_if]
    yposition = [0, 5]
    for xc in xposition:
        ax2.axvline(x=xc, color='k', linestyle='--', lw=1.0)
    for yc in yposition:
        ax2.axhline(y=yc, color='k', linestyle='--', lw=1.0)
    datacursor(display='multiple', draggable=True)
    
    plt.figure(num=2, dpi=125, edgecolor='b')
    plt.plot(x, p_i/1000, 'b-', lw=1.5)
    plt.plot(point_x, point_y, 'r-', lw=1.5)
    plt.title('Ground Reaction Curve')
    plt.ylabel('Support Pressure $P_i\,[MPa]$', fontsize=12)
    plt.xlabel('Tunnel Wall Displacement $u_i\,[m]$', fontsize=12)
    datacursor(display='multiple', draggable=True)
    plt.show()
