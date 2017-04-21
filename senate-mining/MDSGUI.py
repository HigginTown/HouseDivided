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

import copy
import random
from Tkinter import *
from Numeric import *
from LinearAlgebra import *
import RandomArray
import orngMDS
import math
#import Pmw

DIMEN = 2

class Canvy:
    def clickL(self,event):
        pass
        
    def dragL(self,event):
        pass

    def resize(self,event):
        self.h = event.height
        self.w = event.width
        self.update()        

    def releaseL(self,event):
        r = self.canvas.gettags(CURRENT)
        idx = int(r[1])
        xa = (event.x-self.w/2)/self.sx+self.tx
        ya = (event.y-self.h/2)/self.sy+self.ty
        self.mds.X[idx][0]=xa
        self.mds.X[idx][1]=ya
        self.mds.freshD = 0    # mark the update
        self.update()
        
    def update(self):
        self.mds.getStress()
        self.canvas.delete(ALL)
        self.createitems()

    def randomize(self):
        self.mds.X = RandomArray.random(shape=[self.mds.n,2])
        self.update()
        
    def torgerson(self):
        self.mds.Torgerson()
        self.update()

    def smacof(self):
        self.mds.SMACOFstep()
        self.update()

    def smacofslow(self):
        self.mds.SMACOFstepSlow()
        self.update()

    def smacoflot(self):
        for i in range(50):
            self.mds.SMACOFstep()
        self.update()

    def smacoflocal(self):
        self.mds.SMACOFstepLocal()
        self.update()

    def lsmt(self):
        r = self.mds.LSMT()
        if r:
            print "LSMT operated"
        else:
            print "no effect in LSMT"
        self.update()

    def printxy(self):
        for i in range(self.mds.n):
            print self.names[i],
            for j in range(DIMEN):
                print self.mds.X[i][j],
            print                

    def jitter(self):
        # perturb +-1%
        mi = argmin(self.mds.X,0)
        ma = argmax(self.mds.X,0)
        st = 0.02*(ma-mi)
        for i in range(self.mds.n):
            for j in range(2):
                self.mds.X[i][j] += st[j]*(random.random()-0.5)
        self.update()

    def stess(self):
        self.mode = 1-self.mode
        self.update()

    def disable(self,event):
        self.canvas.itemconfig(CURRENT,fill="black")
        
    def enable(self,event):
        self.canvas.itemconfig(CURRENT,fill="white")
        
    def move(self,event):
        self.canvas.coords(CURRENT,event.x-5,event.y-5,event.x+5,event.y+5)

    def createitems(self):
        margins = 50
        # get the minmax bounds for the MDS,rescale
        mi = argmin(self.mds.X,0)
        ma = argmax(self.mds.X,0)
        mi_x = self.mds.X[mi[0]][0]
        mi_y = self.mds.X[mi[1]][1]
        ma_x = self.mds.X[ma[0]][0]
        ma_y = self.mds.X[ma[1]][1]
        self.tx = tx = (ma_x+mi_x)/2.0 # translation
        self.ty = ty = (ma_y+mi_y)/2.0
        sx = sx = (self.w-2*margins)/(ma_x-mi_x) # scaling
        sy = sy = (self.h-2*margins)/(ma_y-mi_y)

        # the scaling factor has to be the same for both axis
        # TODO: rotate them so that they will be a best fit
        sx = min(sx,sy)
        sy = sx
        self.sx = sx
        self.sy = sy
        colors = ["blue","lawngreen","lightblue","gold","seagreen","aquamarine","sienna","red","orchid","tomato","mediumpurple"]
        if self.res != None:
            cc = orngEval.CA(self.res)
        else:
            cc = [100.0]*len(self.mds.X)
        if self.mode == 0:
            # draw 10 of the strongest stresses, assuming signed rel. stress
            strlist = []
            for (l,(a,b)) in self.mds.arr:
                strlist.append((abs(l),l,(a,b)))
            strlist.sort()
            for (al,l,(a,b)) in strlist[-20:]:
                xa = self.w/2+(self.mds.X[a][0]-tx)*sx
                ya = self.h/2+(self.mds.X[a][1]-ty)*sy
                xb = self.w/2+(self.mds.X[b][0]-tx)*sx
                yb = self.h/2+(self.mds.X[b][1]-ty)*sy
                if l < 0: # repulsion
                    c = "red"
                else: # attraction
                    c = "darkgreen"
                self.canvas.create_line((xa,ya,xb,yb),fill=c)
                xc = (xa+xb)/2.0
                yc = (ya+yb)/2.0
                curl = math.sqrt((self.mds.X[a][0]-self.mds.X[b][0])*(self.mds.X[a][0]-self.mds.X[b][0]) + (self.mds.X[a][1]-self.mds.X[b][1])*(self.mds.X[a][1]-self.mds.X[b][1]))
                trul = curl/(1+l)
                pl = l
                l = (curl-trul)/(2.0*curl)
                #print pl, l, curl, trul
                if l < 0:
                    xd = -(xa-xb)*l
                    yd = -(ya-yb)*l
                    self.canvas.create_line((xa-xd,ya-yd,xa,ya),fill=c,width=3)
                    self.canvas.create_line((xa,ya,xb+xd,yb+yd),fill=c,width=3)
                else:
                    xd = -(xa-xb)*l
                    yd = -(ya-yb)*l
                    self.canvas.create_line((xc-xd,yc-yd,xc+xd,yc+yd),fill=c,width=3)
                
        for i in range(len(self.mds.X)):
            x = self.w/2+(self.mds.X[i][0]-tx)*sx
            y = self.h/2+(self.mds.X[i][1]-ty)*sy
            if cc[i] > 99.0:
                t = self.canvas.create_oval((x-5,y-5,x+5,y+5),fill=colors[i%len(colors)],tags=('node','%d'%i))
            else:
                t = self.canvas.create_arc((x-5,y-5,x+5,y+5),start=0,extent=360.0*cc[i],fill=colors[i%len(colors)],tags=('node','%d'%i))
#            self.balloon.tagbind(self.canvas,t,self.names[i])
            self.canvas.create_text(x+8,y+8,text=self.names[i])

    def draw(self):
        #self.balloon = Pmw.Balloon(self.master)
        self.canvas = Canvas(self.master,width = 600, height = 600)
        self.h = 700
        self.w = 700
        self.canvas.bind("<Configure>",self.resize);
        self.canvas.pack()
        self.createitems()
        self.canvas.tag_bind('node', "<B1-Motion>", self.move)
        self.canvas.tag_bind('node', "<ButtonRelease-1>", self.releaseL)

    def init(self,master,mds,res,names):
        self.mds = mds
        self.names = names
        self.res = res
        self.master = master
        self.mode = 1
        self.draw()
        

class App:
    def __init__(self,master,a,b,c):
        self.mode = 0
        self.toolbar = Frame(master)
        self.toolbar.pack(side=TOP,fill=X)
        self.frame2 = Frame(master)
        self.frame2.pack(side=BOTTOM)
        self.canvas = Canvy()
        
        button = Button(self.toolbar, text="RANDOM", command = self.canvas.randomize)
        button.pack(side=LEFT)
        button = Button(self.toolbar, text="TORGERSON", command = self.canvas.torgerson)
        button.pack(side=LEFT)
        button = Button(self.toolbar, text="JITTER", command = self.canvas.jitter)
        button.pack(side=LEFT)
        button = Button(self.toolbar, text="PRINT", command = self.canvas.printxy)
        button.pack(side=LEFT)
        button = Button(self.toolbar, text="STRESS", command = self.canvas.stess)
        button.pack(side=LEFT)
        button = Button(self.toolbar, text="LSMT", command = self.canvas.lsmt)
        button.pack(side=LEFT)
        button = Button(self.toolbar, text="SMACOF/10", command = self.canvas.smacofslow)
        button.pack(side=LEFT)
        button = Button(self.toolbar, text="SMACOF", command = self.canvas.smacof)
        button.pack(side=LEFT)
        button = Button(self.toolbar, text="50x SMACOF", command = self.canvas.smacoflot)
        button.pack(side=LEFT)
        button = Button(self.toolbar, text="L-SMACOF", command = self.canvas.smacoflocal)
        button.pack(side=LEFT)
        button = Button(self.toolbar, text="QUIT", command = self.toolbar.quit)
        button.pack(side=LEFT)
        self.canvas.init(self.frame2,a,b,c)

def Init(dissimilarities,names=None,weights = None,initpos = None):
    if type(dissimilarities)==type([]):
        # convert a bottom triangular list into a matrix
        print "converting dissimilarities..."
        print type(dissimilarities)
        d = orngMDS.constructMatrixFromProx(dissimilarities)
    else:
        d = dissimilarities
        assert(shape(d)[1]==len(d)) # must be a square matrix
        
    if weights!=None:
        if type(dissimilarities)==type([]):
            print "converting weights..."
            print type(weights)
            w = orngMDS.constructMatrixFromProx(weights)
        else:
            w = weights
        assert(len(w)==len(d))
        assert(shape(w)[1]==len(d)) # must be a square matrix
        mds = orngMDS.WMDS(d,dimensions=DIMEN)
        mds.setWeights(w)
    else:
        mds = orngMDS.MDS(d,dimensions=DIMEN)

    if initpos != None:
        if type(initpos)==type([]):
            ip = array(initpos)
        else:
            ip = initpos
        assert(shape(ip)[0]==len(d))
        assert(shape(ip)[1]==2)
        mds.X = ip

    if names != None:
        assert(len(names)==len(d))
        for i in names:
            assert(type(i)==type(""))
        n = names
    else:
        n = []
        for i in range(len(d)):
            n.append("%d"%i)

    mds.getStress()            
    root = Tk()
    app = App(root,mds,None,n)
    return root
    
def Run(dissimilarities,names=None,weights = None,initpos = None):
    root = Init(dissimilarities,names,weights,initpos)
    root.title("PyMDS")
    root.mainloop()