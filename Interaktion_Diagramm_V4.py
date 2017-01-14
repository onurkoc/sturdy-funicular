"""
@author: Onur Koc

This is an attempt to draw an interaction line
"""
import math
import pandas as pd
import matplotlib.pyplot as plt
import seaborn

#Epsilon values of the steel and the concrete

#a. Stahldehnung Zugseite 
epsilon_s1 = [
          -0.003499,-0.0032,-0.0029,-0.0026,-0.0023,-0.002,-0.0017,-0.0014,
          -0.0011,-0.0008,-0.0005,-0.0002,0.0,0.0004,0.0007,0.001,0.0013,
          0.0016,0.0019,0.0022,0.0025,0.0028,0.0031,0.0034,0.0037,0.004,
          0.0043,0.0049,0.0052,0.0055,0.006,0.0065,0.007,0.0075,0.008,
          0.009,0.0095,0.01,0.011,0.012,0.012,0.012,0.012,0.012,0.012,
          0.012,0.012,0.012,0.012,0.012,0.012,0.012
          ]

#b. Betonstauchung
epsilon_c = [
          -0.0035,-0.0035,-0.0035,-0.0035,-0.0035,-0.0035,-0.0035,-0.0035,
          -0.0035,-0.0035,-0.0035,-0.0035,-0.0035,-0.0035,-0.0035,-0.0035,
          -0.0035,-0.0035,-0.0035,-0.0035,-0.0035,-0.0035,-0.0035,-0.0035,
          -0.0035,-0.0035,-0.0035,-0.0035,-0.0035,-0.0035,-0.0035,-0.0035,
          -0.0035,-0.0035,-0.0035,-0.0035,-0.0035,-0.0035,-0.0035,-0.0035,
          -0.0032,-0.0029,-0.0026,-0.0023,-0.002,-0.0017,-0.0014,-0.0011,
          -0.0008,-0.0005,-0.0002,0.0
          ]

#Mapping the epsilon values as pandas dataframe
df = pd.DataFrame({'eps_c' : epsilon_c, 'eps_s1' : epsilon_s1})

#Inputs:

h       = 0.20   #int(input('Höhe in [m] eingeben: '))
d_1     = 0.03   #int(input('Betondeckung_1 in [m] eingeben: '))
d_2     = 0.03   #int(input('Betondeckung_2 in [m] eingeben: '))
b       = 1.00   #int(input('Breite in [m] eingeben: '))
f_ck    = 25     #int(input('Betondruckfestigkeit in [N/mm2] eingeben: '))
f_yk    = 420    #int(input('Stahlzugfestigkeit in [N/mm2] eingeben: '))
gamma_c = 1.5    #float(input('Teilsicherheit für Beton eingeben: '))
gamma_s = 1.15   #float(input('Teilsicherheit für Stahl eingeben: '))
gamma_d = 1.35   #float(input('Teilsicherheit für Last eingeben: '))
a_s1    = 3.35   #float(input('Zugbewehrungsfläche in [cm2/m] eingeben: '))
a_s2    = 3.35   #float(input('Druckbewehrungsfläche in [cm2/m] eingeben: '))

#Constant values and the design values
EStahl  = 200000    #N/mm2
alpha   = a_s1 / a_s2
f_cd    = f_ck / gamma_c
f_yd    = f_yk / gamma_s
d       = h - d_1
a_s1_   = 0 #indicating naked concrete interaction line
alpha_  = 1 #again for naked concrete interaction line

#iterating for every epsilon value pair
moment  = []
n_kraft = []
for i in range(len(df.eps_c)):
        #calling eps_c and eps_s1 from now on as y and x
        x = df.eps_s1[i]
        y = df.eps_c[i]
        
        #Rechteckanteil       
        def xi1():
            if (-0.002 - y) * d / (x - y) > 0:
                return min((-0.002 - y) * d / (x - y) , h)
            else:
                return 0
        
        xi1_ = xi1()
            
        #Druckzonenhöhe
        xi2 = min((-y * d) / (x - y) , h)
    
        #Hilfswert
        h_w = (y - x) / d
    
        #Betondruckkraft
        F_c = f_cd * b * (-xi1_ + (xi2 - xi1_) * (1000 * y + 250000
            * y**2) - (xi2**2 - xi1_**2) * (500 * h_w + 250000 * h_w 
            * y) + (xi2**3 - xi1_**3) * 250000 * h_w**2 / 3)
        
        #Beton Moment
        M_c = f_cd * b * (-0.5 * xi1_**2 + 0.5 * (1000 * y + 250000 * y**2) 
            * (xi2**2 - xi1_**2) - (1000 + 500000 * y) * h_w / 3 
            * (xi2**3 - xi1_**3) + 62500 * h_w**2 * (xi2**4 - xi1_**4))
        
        #Ausmitte Betonkraft
        e_ausm = h / 2 - M_c / F_c
        
        #Stahldehnung Druckseite
        eps_s2 = y - (y - x) / d * d_2
        
        #Druckkraft Stahl
        F_s2 = math.copysign(1, eps_s2) * min((EStahl * abs(eps_s2)), f_yd) * alpha_ * a_s1_ 
        
        #Zugkraft Stahl
        F_s1 = math.copysign(1, x) * min((EStahl * abs(x)), f_yd) * a_s1_ 
        
        #Moment
        M_r = F_s1 * (h / 2 - d_1) - F_s2 * (h / 2 - d_2) - F_c * e_ausm
        
        #Normalkraft
        N_r = F_s2 + F_s1 + F_c
        
        #M und N, writing to list
        moment.append(M_r)
        n_kraft.append(N_r)
        
#iterating for every epsilon value pair but this time with reinforcement
moment_bew  = []
n_kraft_bew = []
for i in range(len(df.eps_c)):
        #calling eps_c and eps_s1 from now on as y and x
        x = df.eps_s1[i]
        y = df.eps_c[i]
        
        #Rechteckanteil       
        def xi1():
            if (-0.002 - y) * d / (x - y) > 0:
                return min((-0.002 - y) * d / (x - y) , h)
            else:
                return 0
        
        xi1_ = xi1()
            
        #Druckzonenhöhe
        xi2 = min((-y * d) / (x - y) , h)
    
        #Hilfswert
        h_w = (y - x) / d
    
        #Betondruckkraft
        F_c = f_cd * b * (-xi1_ + (xi2 - xi1_) * (1000 * y + 250000
            * y**2) - (xi2**2 - xi1_**2) * (500 * h_w + 250000 * h_w 
            * y) + (xi2**3 - xi1_**3) * 250000 * h_w**2 / 3)
        
        #Beton Moment
        M_c = f_cd * b * (-0.5 * xi1_**2 + 0.5 * (1000 * y + 250000 * y**2) 
            * (xi2**2 - xi1_**2) - (1000 + 500000 * y) * h_w / 3 
            * (xi2**3 - xi1_**3) + 62500 * h_w**2 * (xi2**4 - xi1_**4))
        
        #Ausmitte Betonkraft
        e_ausm = h / 2 - M_c / F_c
        
        #Stahldehnung Druckseite
        eps_s2 = y - (y - x) / d * d_2
        
        #Druckkraft Stahl
        F_s2 = math.copysign(1, eps_s2) * min((EStahl * abs(eps_s2)), f_yd) * alpha * a_s1 / 10000
        
        #Zugkraft Stahl
        F_s1 = math.copysign(1, x) * min((EStahl * abs(x)), f_yd) * a_s1 / 10000
        
        #Moment
        M_r = F_s1 * (h / 2 - d_1) - F_s2 * (h / 2 - d_2) - F_c * e_ausm
        
        #Normalkraft
        N_r = F_s2 + F_s1 + F_c
        
        #M und N, writing to list
        moment_bew.append(M_r)
        n_kraft_bew.append(N_r)

moment_neg = []
#left side of the diagram (concrete)
for i in range(len(moment)):
    moment_neg.append(float(abs(moment[i])*-1))
    
moment_bew_neg = []
#left side of the diagram (with reinforcement)
for i in range(len(moment_bew)):
    moment_bew_neg.append(float(abs(moment_bew[i])*-1))
    
#reading from the ZSoil file while converting them into design values
df_ = pd.read_csv('M-N.csv', sep = ';', header=1)

moment_ = df_['  Moments-MZ'][1:]
n_kraft_ = df_['   Forces-NX'][1:]

n_kraft_1 = []
for i in range(len(n_kraft_)):
    n_kraft_1.append(gamma_d * float(n_kraft_[i+1]) / 1000)
moment_1 = []
for i in range(len(moment_)):
    moment_1.append(gamma_d * float(moment_[i+1]) / 1000)


#from here on plotting utilities
plt.figure(num=1, dpi=125, edgecolor='b')
plt.plot(moment_bew, n_kraft_bew, 'r--', linewidth=1.5, 
         label="$A_s \/= %0.2f\,cm^2/m$\n$f_{yk} = %0.1f\,N/mm^2$" %(a_s1,f_yk))
plt.plot(moment_bew_neg, n_kraft_bew, 'r--',linewidth=1.5)
plt.plot(moment_neg, n_kraft, 'b-', linewidth=1.5,
         label="$f_{ck} = %0.1f\,N/mm^2$\n$h \/\:\:\, = %0.2f\,m$\n$d'_1 = %0.2f\,m$\n$d'_2= %0.2f\,m$" %(f_ck,h,d_1,d_2))
plt.plot(moment, n_kraft, 'b-', linewidth=1.5)
plt.plot(moment_1,n_kraft_1, 'r^', label="$Design\;Values$")
#plt.text(1, 1, r"$h = %0.2f$" %h, fontsize=20)
plt.xlabel('Moment [MNm/m]')
plt.ylabel('Normalkraft [MN/m]')
plt.title('Interaktion-Diagramm')
ax = plt.gca()
ax.set_ylim([min(n_kraft_bew),max(n_kraft_bew)]) #limit the y-axis to the bew.values
ax.invert_yaxis() #invert the y-axis
ax.grid(True) #grid on
box = ax.get_position()
#setting the legend outside the plot
ax.set_position([box.x0, box.y0, box.width * 0.7, box.height * 1])
ax.legend(loc='center left', bbox_to_anchor=(1,0.5),
          fancybox=True, shadow=True)