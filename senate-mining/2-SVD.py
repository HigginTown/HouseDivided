####
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Orange; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#    Author:  Aleks Jakulin
#    Contact: jakulin@acm.org
####

import orange, cPickle
from orngInteract import *
import Numeric,orngDimRed
import copy
from Numeric import *
import time, string
import piddleFIG,piddlePS
import Tkinter, ImageTk
import piddle, piddlePIL, math


class ViewImage:
    class PicCanvas:
        def draw(self):
            self.canvas = Tkinter.Canvas(self.master,width=self.pic.width(),height=self.pic.height())
            self.canvas.pack()
            self.canvas.create_image(0,0,anchor=Tkinter.NW,image=self.pic)
        
        def __init__(self,master,pic):
            self.master = master
            self.pic = pic
            self.draw()

    def __init__(self,pic):
        self.root = Tkinter.Tk()
        self.root.title("ViewImage")
        self.canvas = self.PicCanvas(self.root,ImageTk.PhotoImage(pic))
        self.root.mainloop()

class ViewCanvas:
    def __init__(self,canvas):
        self.root = Tkinter.Tk()
        self.root.title("ViewCanvas")
        self.canvas = canvas
        self.root.mainloop()


i=8
n = 'us-senate-10%d'%i
mod = '-m' # missing value handling

t = orange.ExampleTable('%s%s.tab'%(n,mod))

labels = []
for a in t.domain.attributes:
    labels.append(a.name)
labels.append(t.domain.classVar.name)

oth=[0.000067,0.007591,0.002238,0.000000,0.000005]
dem=[0.003435,0.409964,0.047890,0.001346,0.012614]
rep=[0.026974,0.001813,0.002866,0.136832,0.336465]

ord = []
for i in xrange(len(oth)):
    ord.append(dem[i]-rep[i])    
iord = [(ord[i],i) for i in range(len(ord))]
iord.sort()

f = open('R2%s.txt'%mod,'r')
ff = f.readlines()
LUT = {}
matt = []
for i in range(len(labels)):
    matt.append([])
    LUT[labels[i]] = i
    LUT["(%d)"%i] = i
for x in ff:
    l = string.split(x[:-1],sep='\t')
    i = LUT[l[0]]
    if len(matt[i])==0:
        c = 0.0
        q = []
        for j in range(1,len(l)):
            v = float(l[j])
            c+=v
            q.append(float(l[j]))
        for j in range(len(q)):
            matt[i].append(q[iord[j][1]]/c)



def ordinary_matrix():
    A = Numeric.zeros((len(t),1+len(t.domain.attributes)),Numeric.Float)
    for i in xrange(len(t)):
        s = 0.0
        c = 0.0
        for j in xrange(len(labels)):
            if not t[i][j].isSpecial():
                c += 1
                if int(t[i][j])==0:
                    s -= 1
                else:
                    s += 1
        s /= c
        for j in xrange(len(labels)):
            if not t[i][j].isSpecial():
                if int(t[i][j])==0:
                    A[i,j] = -1
                else:
                    A[i,j] = 1
            else:
                # try imputation
                #if int(t[i].getclass()) == 1: # submission
                if int(t[i].getclass()) == 0: # stratagem
                    A[i,j] = -1 
                else:
                    A[i,j] = 1
    

#def SVD_impute():
# imputation using the dPCA model
A = Numeric.zeros((len(t),1+len(t.domain.attributes)),Numeric.Float)
for i in xrange(len(t)):
    s = [0.0]*5
    c = [0.0]*5
    for j in xrange(len(labels)):
        if not t[i][j].isSpecial():
            for k in xrange(5):
                c[k] += matt[j][k]
                if int(t[i][j])==0:
                    s[k] -= matt[j][k]
                else:
                    s[k] += matt[j][k]
    for j in xrange(len(labels)):
        if not t[i][j].isSpecial():
            if int(t[i][j])==0:
                A[i,j] = -1
            else:
                A[i,j] = 1
        else:
            # try imputation
            for k in xrange(5):
                A[i,j] += matt[j][k]*s[k]/c[k]



cols = ["#051DFF","#FF05FC","#FF053A","#FFD305","#05FF11"]

def iRGB(s):
    return (int(s[1:3],16)/255.0,int(s[3:5],16)/255.0,int(s[5:7],16)/255.0)

def centering_by_senators():
    for d in xrange(101):
        (v,transf) = orngDimRed.Centering(A[:,d])
        A[:,d:d+1] = Numeric.reshape(v,(len(t),1))

#def centering_by_rows():
for d in xrange(len(t)):
    (v,transf) = orngDimRed.Centering(A[d,:])
    A[d:d+1,:] = Numeric.reshape(v,(1,len(t.domain.attributes)+1))


A = Numeric.transpose(A)
P = orngDimRed.PCA(A,components=2)

X = P.loading[:,0]*P.variance[0]
Y = P.loading[:,1]*P.variance[1]

dd = 1.0/max(max(X)-min(X),max(Y)-min(Y))

def transform(R):
    ma = max(R)
    mi = min(R)
    return 25+500*(R-mi)*(dd)

X = transform(X)
Y = transform(Y)

canvas = piddlePS.PSCanvas((550,550),n)
normal = piddle.Font(face="Courier")

yd = canvas.fontHeight(normal)/2.0
for j in xrange(101):
    if (j == 100):
        s = '*OUT*'
    else:
        s = string.split(t.domain.attributes[j].name,' ')[1]
    xd = canvas.stringWidth(s,font=normal)/2.0
    # compute the color
    r = 0.0
    g = 0.0
    b = 0.0
    for i in xrange(5):
        (r1,g1,b1) = iRGB(cols[i])
        r += matt[j][i]*r1
        g += matt[j][i]*g1
        b += matt[j][i]*b1
    colo = piddle.Color(r/2,g/2,b/2)
    canvas.drawString(s, X[j]-xd, Y[j]-yd,font=normal,color=colo)

canvas.save("PCA-dpca.eps")
#canvas.getImage().save("SVD-impute-submit.png")
#ViewImage(canvas.getImage())
