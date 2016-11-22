# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 21:49:53 2016

@author: Onur Koc
"""

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import math
import pandas as pd
import matplotlib.pyplot as plt
import sys
import seaborn
from mpldatacursor import datacursor #optional to annotate any clicked point

#---------------------------------------------------------------------------
#This part is needed only for pyinstaller execution
#---------------------------------------------------------------------------
import ctypes
import os

if getattr(sys, 'frozen', False):
  # Override dll search path.
  ctypes.windll.kernel32.SetDllDirectoryW('C:/IGT/Anaconda/Library/bin/')
  # Init code to load external dll
  ctypes.CDLL('mkl_avx2.dll')
  ctypes.CDLL('mkl_def.dll')
  ctypes.CDLL('mkl_vml_avx2.dll')
  ctypes.CDLL('mkl_vml_def.dll')

  # Restore dll search path.
  ctypes.windll.kernel32.SetDllDirectoryW(sys._MEIPASS)
  
#---------------------------------------------------------------------------
#End of the pyinstaller part
#---------------------------------------------------------------------------

class InteractionDiagram(QDialog):
    def __init__ (self, parent = None):
        super(InteractionDiagram, self).__init__(parent, \
            flags=Qt.WindowMinimizeButtonHint|Qt.WindowMaximizeButtonHint|Qt.WindowStaysOnTopHint)  
            #include this flag to add minimize button on GUI
        grid = QGridLayout()
        
        grid.addWidget(QLabel('h = '), 0,0)
        self.h_ = QLineEdit()
        self.h_.setInputMask('0.00')
        self.h_.setText('0.15') #set the default value in the box
        grid.addWidget(self.h_,0,1)
        
        grid.addWidget(QLabel('b = '), 1,0)
        self.b_ = QLineEdit()
        self.b_.setInputMask('0.00')
        self.b_.setText('1.00')
        grid.addWidget(self.b_,1,1)
        
        grid.addWidget(QLabel('d1 = '), 2,0)
        self.d_1 = QLineEdit()
        self.d_1.setInputMask('0.00')
        self.d_1.setText('0.03')
        grid.addWidget(self.d_1,2,1)
        
        grid.addWidget(QLabel('d2 = '), 3,0)
        self.d_2 = QLineEdit()
        self.d_2.setInputMask('0.00')
        self.d_2.setText('0.03')
        grid.addWidget(self.d_2,3,1)
        
        grid.addWidget(QLabel('fck = '), 4,0)
        self.f_ck = QComboBox()
        self.f_ck.addItems(('40',
                            '20',
                            '25',
                            '30',
                            '37',
                            '50'))
        grid.addWidget(self.f_ck,4,1)
        
        grid.addWidget(QLabel('fyk = '), 5,0)
        self.f_yk = QComboBox()
        self.f_yk.addItems(('500',
                            '420',
                            '550'))
        grid.addWidget(self.f_yk,5,1)
        
        grid.addWidget(QLabel('as1 = '), 6,0)
        self.a_s1 = QLineEdit()
        self.a_s1.setInputMask('0.00')
        self.a_s1.setText('3.35')
        grid.addWidget(self.a_s1,6,1)
        
        grid.addWidget(QLabel('as2 = '), 7,0)
        self.a_s2 = QLineEdit()
        self.a_s2.setInputMask('0.00')
        self.a_s2.setText('3.35')
        grid.addWidget(self.a_s2,7,1)
        
        grid.addWidget(QLabel('gamma_c = '), 8,0)
        self.gamma_c = QComboBox()
        self.gamma_c.addItems(('1.50',
                               '1.20',
                               '1.00'))
        grid.addWidget(self.gamma_c,8,1)
        
        grid.addWidget(QLabel('gamma_s = '), 9,0)
        self.gamma_s = QComboBox()
        self.gamma_s.addItems(('1.15',
                               '1.00'))
        grid.addWidget(self.gamma_s,9,1)

        grid.addWidget(QLabel('gamma_d = '), 10,0)
        self.gamma_d = QComboBox()
        self.gamma_d.addItems(('1.35',
                               '1.40',
                               '1.00'))
        grid.addWidget(self.gamma_d,10,1)
        
        openButton = QPushButton('Load .csv file!')
        openButton.setShortcut("Ctrl+O")
        self.connect(openButton, SIGNAL('pressed()'),self.loadFile)
        grid.addWidget(openButton,11,0,1,2)
        
        executeButton = QPushButton('Execute')
        self.connect(executeButton, SIGNAL('pressed()'), self.int_diagram)
        grid.addWidget(executeButton,12,0,1,2)
        
        self.setLayout(grid)
        self.setWindowTitle('Interaction Diagram')
        

    def loadFile(self):
        global file 
        name = QFileDialog.getOpenFileName(self, 'Open File')
        file = open(name,'r')
        
    
    def int_diagram(self):

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
        
        #Inputs from GUI:
        
        h_      = 0
        h_      = float(self.h_.text())
        d_1     = 0
        d_1     = float(self.d_1.text())
        d_2     = 0
        d_2     = float(self.d_2.text())
        b_      = 0
        b_      = float(self.b_.text())
        f_ck    = 0
        f_ck    = float(self.f_ck.currentText())
        f_yk    = 0
        f_yk    = float(self.f_yk.currentText())
        gamma_c = 0
        gamma_c = float(self.gamma_c.currentText())
        gamma_s = 0
        gamma_s = float(self.gamma_s.currentText())
        gamma_d = 0
        gamma_d = float(self.gamma_d.currentText())
        a_s1    = 0
        a_s1    = float(self.a_s1.text())
        a_s2    = 0
        a_s2    = float(self.a_s2.text())
        
        
        EStahl  = 200000    #N/mm2
        alpha   = a_s1 / a_s2
        f_cd    = f_ck / gamma_c
        f_yd    = f_yk / gamma_s
        d       = h_ - d_1
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
                        return min((-0.002 - y) * d / (x - y) , h_)
                    else:
                        return 0
                
                xi1_ = xi1()
                    
                #Druckzonenhöhe
                xi2 = min((-y * d) / (x - y) , h_)
            
                #Hilfswert
                h_w = (y - x) / d
            
                #Betondruckkraft
                F_c = f_cd * b_ * (-xi1_ + (xi2 - xi1_) * (1000 * y + 250000
                * y**2) - (xi2**2 - xi1_**2) * (500 * h_w + 250000 * h_w 
                * y) + (xi2**3 - xi1_**3) * 250000 * h_w**2 / 3)
                
                #Beton Moment
                M_c = f_cd * b_ * (-0.5 * xi1_**2 + 0.5 * (1000 * y + 250000 * y**2) 
                * (xi2**2 - xi1_**2) - (1000 + 500000 * y) * h_w / 3 
                * (xi2**3 - xi1_**3) + 62500 * h_w**2 * (xi2**4 - xi1_**4))
                
                #Ausmitte Betonkraft
                try: e_ausm = h_ / 2 - M_c / F_c
                except RuntimeWarning: pass
                
                #Stahldehnung Druckseite

                eps_s2 = y - (y - x) / d * d_2
                
                #Druckkraft Stahl
                F_s2 = math.copysign(1, eps_s2) * min((EStahl * abs(eps_s2)), f_yd) * alpha_ * a_s1_ / 1000
                
                #Zugkraft Stahl
                F_s1 = math.copysign(1, x) * min((EStahl * abs(x)), f_yd) * a_s1_ / 1000
                
                #Moment
                M_r = F_s1 * (h_ / 2 - d_1) - F_s2 * (h_ / 2 - d_2) - F_c * e_ausm
                
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
                        return min((-0.002 - y) * d / (x - y) , h_)
                    else:
                        return 0
                
                xi1_ = xi1()
                    
                #Druckzonenhöhe
                xi2 = min((-y * d) / (x - y) , h_)
            
                #Hilfswert
                h_w = (y - x) / d
            
                #Betondruckkraft
                F_c = f_cd * b_ * (-xi1_ + (xi2 - xi1_) * (1000 * y + 250000
                * y**2) - (xi2**2 - xi1_**2) * (500 * h_w + 250000 * h_w 
                * y) + (xi2**3 - xi1_**3) * 250000 * h_w**2 / 3)
                
                #Beton Moment
                M_c = f_cd * b_ * (-0.5 * xi1_**2 + 0.5 * (1000 * y + 250000 * y**2) 
                * (xi2**2 - xi1_**2) - (1000 + 500000 * y) * h_w / 3 
                * (xi2**3 - xi1_**3) + 62500 * h_w**2 * (xi2**4 - xi1_**4))
                
                #Ausmitte Betonkraft
                try: e_ausm = h_ / 2 - M_c / F_c
                except RuntimeWarning: pass
                
                #Stahldehnung Druckseite
                eps_s2 = y - (y - x) / d * d_2

                #Druckkraft Stahl
                F_s2 = math.copysign(1, eps_s2) * min((EStahl * abs(eps_s2)), f_yd) * alpha * a_s1 / 10000
                
                #Zugkraft Stahl
                F_s1 = math.copysign(1, x) * min((EStahl * abs(x)), f_yd) * a_s1 / 10000
                
                #Moment
                M_r = F_s1 * (h_ / 2 - d_1) - F_s2 * (h_ / 2 - d_2) - F_c * e_ausm
                
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
        df = pd.read_csv(file, sep = ';', header=1)
        
        moment_ = df['  Moments-MZ'][1:]
        n_kraft_ = df['   Forces-NX'][1:]
        
        moment_1 = round(pd.Series(moment_.astype(float)) * gamma_d / 1000, 4) 
        n_kraft_1 = round(pd.Series(n_kraft_.astype(float)) * gamma_d / 1000, 4)

        #from here on plotting utilities
        plt.figure(dpi=120)
        plt.plot(moment_bew, n_kraft_bew, 'r--', linewidth=1.5, \
                 label="$A_s \/= %0.2f\,cm^2/m$\n$f_{yk} = %0.1f\,N/mm^2$" %(a_s1,f_yk))
        plt.plot(moment_bew_neg, n_kraft_bew, 'r--',linewidth=1.5)
        plt.plot(moment_neg, n_kraft, 'b-', linewidth=1.5, \
                 label="$f_{ck} = %0.1f\,N/mm^2$\n$h \/\:\:\, = %0.2f\,m$\n$d'_1 = %0.2f\,m$\n$d'_2= %0.2f\,m$" %(f_ck,h_,d_1,d_2))
        plt.plot(moment, n_kraft, 'b-', linewidth=1.5)
        plt.plot(moment_1,n_kraft_1, 'r^', label="$Design\;Values$", markersize=5)
        
        plt.xlabel('Moment [MNm/m]', fontsize=10)
        plt.ylabel('Normal Force [MN/m]', fontsize=10)
        plt.title('Interaction Diagram', fontsize=12)
        datacursor(display='multiple', draggable=True, \
                    formatter='$M_d=$ {x}$\;MNm/m$ \n $N_d=$ {y}$\;MN/m$'.format, bbox=dict(fc='white'))
        ax = plt.gca()
        ax.set_ylim([min(n_kraft_bew),max(n_kraft_bew)]) #limit the y-axis to the bew.values
        ax.invert_yaxis() #invert the y-axis
        ax.grid(True) #grid on
        box = ax.get_position()
        
        #setting the legend outside the plot
        ax.set_position([box.x0, box.y0, box.width * 0.82, box.height * 1])
        ax.legend(loc='center left', bbox_to_anchor=(1,0.5),
                  fancybox=True, shadow=True, prop={'size':10})
        plt.show()

    
if __name__ == '__main__':
    app=0      
    app = QApplication([])
    window = InteractionDiagram()
    window.show()
    sys.exit(app.exec_())

        
        
