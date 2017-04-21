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


import orange, cPickle, string
from orngInteract import *
import Numeric
import copy
from orngDendrogram import *
from Numeric import *
import piddlePS

i=8
n = 'us-senate-10%d'%i
mod = '-m' # missing value handling

t = orange.ExampleTable('%s%s.tab'%(n,mod))
im = InteractionMatrix(t,prepare=0,interactions_too=0,dependencies_too=1,save_data=0)
cPickle.dump(im,open('dep-%s%s.pik'%(n,mod),'w'))

(diss,labels) = im.depExportDissimilarityMatrix(jaccard=1,color_coding = 1,include_label=1)


oth=[0.000067,0.007591,0.002238,0.000000,0.000005]
dem=[0.003435,0.409964,0.047890,0.001346,0.012614]
rep=[0.026974,0.001813,0.002866,0.136832,0.336465]
tot=[0.030476,0.419367,0.052994,0.138178,0.349084]
outc=[0.075100,0.047900,0.127100,0.056600,0.693300 ]


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
    #i = LUT[l[0]]
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


ad_matr = [[x[iord[y][1]] for y in range(len(x))] for x in [tot,rep,dem,outc]]
ad_tag = ['A','B','C','D','E']
ad_labels = ['*TOTAL','*Republican','*Democrat','*OUTCOME']
        
c = GDHClustering(diss,5)

# reorder the clustering...
f = open('ordering.txt','r')
ord = []
for l in f.readlines():
    s = string.split(l[:-1])
    ord.append(float(s[-1]))

# reorder the clustering...
L = {}
# copy the ordering of democrats
for x in range(48):
    L[c.order[x]] = c.order[x]
for x in range(48,len(c.order)):
    L[c.order[x]] = c.order[len(c.order)-x + 47]
for x in range(len(c.order)):
    c.order[x] = L[c.order[x]]


labels[-1] = "*Outcome"
canvas = c.dendrogram(labels,line_size=0.8,width=500,cluster_colors=im.depGetClusterAverages(c),line_width=3,matr=matt,g_lines=1,additional_labels=ad_labels,additional_matr=ad_matr,add_tags=ad_tag,adwidth=1.61)
canvas.getImage().save("dd_clu_%s%s.png"%(n,mod))
canvas = c.dendrogram(labels,width = 500, line_size=0.8,cluster_colors=im.depGetClusterAverages(c),line_width=3,canvas = piddlePS.PSCanvas((500,1315),n),matr=matt,g_lines=1,additional_labels=ad_labels,additional_matr=ad_matr,add_tags=ad_tag,adwidth=1.61)
canvas.save("clu_%s%s.ps"%(n,mod))

(diss2,labels) = im.depExportDissimilarityMatrix(jaccard=1,include_label=1,truncation=1e20)
canvas = c.matrix(labels,diss2,line_size=1,color_mode=2,diagonal=1)
canvas.getImage().save("matrix_%s.png"%n)
canvas = c.matrix(labels,diss2,line_size=1,color_mode=2,canvas = piddlePS.PSCanvas((1675,1675),n),diagonal=1)
canvas.save("matrix_%s.ps"%n)
