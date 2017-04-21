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

import orange, cPickle, difflib
from orngInteract import *
import Numeric
from orngDendrogram import *
from Numeric import *
from orngContingency import ContingencyTable2
import time, string
import piddleFIG

n = 'us-senate-108'
mod = ''
comps = 5

t = orange.ExampleTable('%s%s.tab'%(n,mod))
labels = []
for a in t.domain.attributes:
    labels.append(a.name)
labels.append(t.domain.classVar.name)

LUT = {}
matt = []
for i in range(len(labels)):
    LUT[labels[i]] = i
    LUT["(%d)"%i] = i
    matt.append([])

# new 3
oth=[0.000067,0.007591,0.002238,0.000000,0.000005]
dem=[0.003435,0.409964,0.047890,0.001346,0.012614]
rep=[0.026974,0.001813,0.002866,0.136832,0.336465]

ord = []
for i in xrange(len(oth)):
    ord.append(dem[i]-rep[i])    
iord = [(ord[i],i) for i in range(len(ord))]
iord.sort()

# load senator proportions
f = open('R2-m.txt','r')
ff = f.readlines()
matl = ['A','B','C','D','E','Rep','Dem','All']
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
PLUT = {'D':1,'R':0,'I':2}
for i in xrange(len(t.domain.attributes)):
    m = [0.0,0.0,0.0]
    m[PLUT[str(t.domain.attributes[i].name)[-5]]] += 1.0
    matt[i] += m[:2]
    matt[i] += [1] # all
    
for i in xrange(len(matt[0])):
    count = 0
    tot = avgai = avgxai = avgent = avgxent = 0.0
    for j in xrange(len(t)):
        ny = 0.0
        na = 0.0
        nn = 0.0
        for k in xrange(len(t.domain.attributes)):
            r = t[j][k]
            if not r.isSpecial():
                r = str(r)
                w = matt[k][i]
                if int(r) == 1:
                    ny += w
                elif int(r) == 0:
                    nn += w
                elif int(r) == -1:
                    na += w
                else:
                    raise "hell"
            else:
                na += 1
            

        sum = float(na+ny+nn)
        sumx = float(ny+nn)
        tot += sum
        if sum > 0:
            count += 1
            if sumx == 0:
               sumx = 1
            avgai += (max([ny,nn,na])-0.5*(sum - max([ny,nn,na])))/sum 
            avgxai += (max([ny,nn])-0.5*(sumx - max([ny,nn])))/sumx
            if ny > 0:
                avgent -= ( (ny/sum)*log(ny/sum) ) / log(3.0)
                avgxent -= ( (ny/sumx)*log(ny/sumx) ) / log(2.0)
            if nn > 0:  
                avgent -= ( (nn/sum)*log(nn/sum) ) / log(3.0)
                avgxent -= ( (nn/sumx)*log(nn/sumx) ) / log(2.0)
            if na > 0:  
                avgent -= ( (na/sum)*log(na/sum) ) / log(3.0)
    if count != 0:
        avgai /= count
        avgxai /= count
        avgent /= count
        avgxent /= count
    print "%s & %0.3f & %0.3f & %2.1f \\\\"%(matl[i],avgai,avgent,tot/count)
