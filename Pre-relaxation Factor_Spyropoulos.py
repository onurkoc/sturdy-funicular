import numpy as np
import matplotlib.pyplot as plt
from mpldatacursor import datacursor 
import seaborn


# ------------
# Input values
# ------------
gamma = 23
# Specific weight of the rock mass [kN/m³]
H = 210
# Overburden [m]
E = 500000
# Modulus of elasticity of the rock [kPa]
p_o = gamma * H
# In-situ stress [kPa]
D = 12.4
# Diameter of the tunnel [m]
c = 300
# Cohesion of the rock [kPa]
phi = 28
# Friction angle of the rock [deg]
Phi = np.deg2rad(phi)
# Convertion from degrees to radians [rad]
r_o = D / 2
# Radius of the tunnel

# -----------------
# Output parameters
# -----------------

sigma_cm = 2 * c * np.cos(Phi) / (1 - np.sin(Phi))
# Uniaxial strength of the rock mass [kPa]

N_s = 2 * p_o / sigma_cm
# Overload factor

M_s = E / (1000 * gamma * H**0.9 * D**0.1)
# Pureley elastic response for M_s > 4

x = np.arange(0,100,1)
# Distance to the face, behind the face

k = (np.tan(np.deg2rad(45) + Phi/2))**2
# Slope defined by the Mohr-Coulomb criterion [-]

z = (1 + np.exp(2.2 * M_s**0.37 * x / r_o))**(-1.2)
# u_r / u_rmax

lambda_ = 1 - ((2 / ((k - 1) * N_s)) * (z**(-(k-1)/(k+1)) -1))
# Deconfinement ratio


plt.figure(num=1, dpi=125, edgecolor='w')
fig = plt.gcf()
fig.canvas.set_window_title('Equivalent support pressure coefficient')
plt.plot(x, 1 - lambda_, 'r-', lw=1.5, label='Spyropoulos, 2005')
plt.title('Equivalent support pressure coefficient $\lambda(x)$')
plt.ylabel('$\lambda\,[-]$', fontsize=12)
plt.xlabel('Distance to face $x\,[m]$', fontsize=12)
datacursor(display='multiple', draggable=True)
plt.show()

