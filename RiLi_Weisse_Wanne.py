# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 09:09:33 2016

@author: o.koc
"""

import numpy as np

h = 600
b = 1000
f_ctm = 2.6
f_cteff = 0.3 * f_ctm
phi = 14.0
c = 50.0
d_1 = c + (phi / 2)
d = h - d_1
E_cm = 31000
E_s = 200000
A_ceff = 2.5 * (h - d) * b
k_bet = 0.85
k_c = 1
k = 0.65 + (1 - 0.65) / (800 - 300) * (800 - h)
A_ct = b * h / 2
w_k = 0.2
F_s = A_ct * f_cteff * k * k_c
F_cr = A_ceff * f_cteff
phi_grenz = min(phi * 4 * (h - d) * f_cteff * b / F_s, phi)
sigma_s = np.sqrt(6 * w_k * f_cteff * E_s / phi_grenz)
as_erf_Fcr = F_cr / sigma_s * k_bet
as_erf_Fs = F_s / sigma_s * k_bet
as_erf = max(as_erf_Fcr, as_erf_Fs)
as_phi = phi**2 * np.pi / 4
e = as_phi / as_erf * 1000

print('d_1 = ', d_1)
print('d = ', d)
print('Ac_eff = ', A_ceff)
print('k = ', k)
print('A_ct = ', A_ct)
print('F_s = ', F_s)
print('F_cr = ', F_cr)
print('Phi_grenz = {:0.1f} mm'.format(phi_grenz))
print('As_erf_Fcr = {:0.2f} cm²/m'.format(as_erf_Fcr/100))
print('As_erf_Fs = {:0.2f} cm²/m'.format(as_erf_Fs/100))
print('As_erf = {:0.2f} cm²/m'.format(as_erf/100))
print('As_phi = {:0.2f} cm²/m'.format(as_phi/100))
print('Abstand = {:0.2f} cm/m'.format(e/10))