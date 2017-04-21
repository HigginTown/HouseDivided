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

import time, string, orngContingency, Numeric
import piddle, piddlePIL, math
import orange

t = orange.ExampleTable("/cache/proj/politics/exp/votes/a-us-senate-108.tab")

# ordering of the blocs
# new 3
oth=[0.000067,0.007591,0.002238,0.000000,0.000005]
dem=[0.003435,0.409964,0.047890,0.001346,0.012614]
rep=[0.026974,0.001813,0.002866,0.136832,0.336465]

ord = []
for i in xrange(len(oth)):
    ord.append(dem[i]-rep[i])    
iord = [(ord[i],i) for i in range(len(ord))]
iord.sort()

fs = [open('difference-A-B.html','w'),open('difference-A-C.html','w'),open('difference-D-E.html','w'),open('difference-D-R.html','w')]
fts = [open('difference-A-B.tex','w'),open('difference-A-C.tex','w'),open('difference-D-E.tex','w'),open('difference-D-R.tex','w')]

# load vote proportions
f = open('/cache/proj/politics/exp/votes/omega.txt','r')
ff = f.readlines()
xmatt = [[] for x in range(5)]
for i in range(5):
    x = ff[i]
    l = string.split(x[:-1],sep='\t')
    q = []
    for j in range(len(l)):
        q.append(float(l[j]))
    for j in range(len(q)/2):
        xmatt[i].append([q[j*2],q[j*2+1]])
votp = []
for i in range(5):
    votp.append(xmatt[iord[i][1]])

# load senator proportions
f = open('R2-m.txt','r')
ff = f.readlines()
LUT = {}
senp = []
labels = [t.domain.attributes[i].name for i in range(100)]+['outcome']
for i in range(len(labels)):
    senp.append([])
    LUT[labels[i]] = i
    LUT["(%d)"%i] = i

power = [0.0] * 5
maxp = [0.0] * 5
examples = [""] *5
for x in ff:
    l = string.split(x[:-1],sep='\t')
    #i = LUT[l[0]]
    i = LUT[l[0]]
    if len(senp[i])==0:
        c = 0.0
        q = []
        for j in range(1,len(l)):
            v = float(l[j])
            c+=v
            q.append(v)
        for j in range(len(q)):
            #senp[i].append(q[iord[j][1]]/c)
            senp[i].append(q[iord[j][1]])
            power[j] += q[iord[j][1]]
            if q[iord[j][1]] > maxp[j]:
                maxp[j] = q[iord[j][1]]
                examples[j] = l[0]

#print power
#print maxp,examples

ss = ""
ss += "<html><table>"
ss += "<tr>"
ss += '<td colspan = "3">REP</td>'
ss += '<td colspan = "2">DEM</td>'
ss += '</tr>'
ss += '<tr> <td>A</td> <td>B</td> <td>C</td> <td>D</td> <td>E</td> <td>OUT</td> <td>dif</td> <td>MI</td> <td>Rice</td> </tr>\n'

lines = []
texlines = []
for f in fs:
    lines.append([])
    texlines.append([])
    print f
    f.write(ss)
    
for i in range(len(t)):
    ny = 0
    nn = 0
    nv = 0
    for j in range(100):
        if int(str(t[i][j])) == 1:
            ny += 1
        elif int(str(t[i][j])) == 0:
            nn += 1
        else:
            nv += 1
    if int(t[i].getclass()) == 0:
        o = 0
    else:
        o = 1
    s = str(t[i][107-2])
    a = int(s[0])
    b = int(s[2])

    def predictoutcome(xy,xn,xv,a,b):
        aa = ((b-a)*xy)
        bb = ((a)*xn)
        if abs(aa-bb) < 1.0:
            return 0.5
        elif (aa > bb):            
            return 1
        else:
            return 0

    def getscore(kk):
        ey = 0.0
        en = 0.0
        env = 0.0
        # for all senators
        for j in xrange(100):
            # for all factions
            v = senp[j][kk]
            if int(str(t[i][j])) == 1:
                ey += v
            elif int(str(t[i][j])) == 0:
                en += v
            else:
                env += v
                
        return (ey,en,env)

    # printout of proportions
    ss = ""
    texs = ""
    ss += "<tr>"
    counts = []
    for kk in range(5):
        r = getscore(kk)
        rs = float(sum(r))
        counts.append((r,rs))
        c = 100.0*r[0]/rs
        ch = 255-2.55*(c)
        if ch < 100:
            ih = 255.0
        else:
            ih = 0.0
        ss += '<td bgcolor="#%02x%02x%02x"><font color="#%02x%02x%02x">%2.1f%%</font></td>'%(ch,ch,ch,ih,ih,ih,c)
        texs += "\\cellcolor{gr%d}\\color{gr%d}{\\tiny\\hspace{-6pt} %2.0f \\hspace{-6pt}}&"%(ch,ih,c)
    # printout of outcome
    if int(t[i].getclass()) == 0:
        c = 255
    else:
        c = 0

    thresh = (float(ny+nn+1)*a/b)
    if a == 3 and b == 5:
        thresh = (float(100)*a/b)
        
    ot = predictoutcome(ny,nn,nv,a,b)
    texs += "\\cellcolor{gr%d}\\color{gr%d}{\\tiny\\hspace{-5pt} %2.0f:%2.0f\\hspace{-5pt}}&"%(c,255-c,ny,nn)
    if ot==o:
        ss += '<td bgcolor="#%02x%02x%02x">&nbsp;&nbsp;&nbsp;&nbsp;</td>'%(c,c,c)
    else:
        ss += '<td bgcolor="#%02x%02x%02x"><font color="#%02x%02x%02x">****</font></td>'%(c,c,c,255-c,255-c,255-c) # error
    # print difference
    #ss += '<td>%d</td>'%round(thresh-ny)
    ss += '<td>%2.0f:%2.0f</td>'%(ny,nn)
    blocs = [[[0],[1]],[[0],[2]],[[3],[4]],[[0,1,2],[3,4]]]
    for mmi in xrange(4):
        xs = ''
        texx = ''
        rdif = []
        Q = Numeric.zeros((3,2),Numeric.Float) # counts
        N = ['vote','bloc']
        V = [['y','n','nv'],['A','B']]
        for mmj in range(2):
            for bb in blocs[mmi][mmj]:
                for tv in xrange(3):
                    Q[tv,mmj] += counts[bb][0][tv]
        C = orngContingency.ContingencyTable2(Q,N,V)
        #rajski = 1-C.JaccardInteraction()
        ent = orngContingency.Entropy(C.pa)
        if ent > 1e-5:
            rajski = C.InteractionInformation()/ent
        else:
            rajski = 0.0
        assert(len(C.pb) == 2)
        pa = C.pm[0,0]
        if C.pb[0] > 0:
            pa /= C.pb[0]
        pb = C.pm[0,1]
        if C.pb[1] > 0:
            pb /= C.pb[1]
        rice = abs(pa-pb)
        xs += '<td>%0.3f</td>'%(rajski)
        xs += '<td>%0.3f</td>'%(rice)
        xs += '<td>%s</td>'%(str(t[i][103])) #identification
        xs += '<td>%s</td>'%(str(t[i][104])) #description
        xs += '<td>%s</td>'%(str(t[i][106]))    # result
        xs += "</tr>\n"
        texx += " %s & %s & %0.3f \\\\\\hline\n"%(str(t[i][103]),str(t[i][104]),rice)

        texlines[mmi].append((-rice,texs+texx))
        lines[mmi].append((-rice,ss+xs))

# print sorted lines
for mm in xrange(len(lines)):
    lines[mm].sort()
    for (rd,st) in lines[mm]:
        fs[mm].write(st)

for mm in xrange(len(texlines)):
    texlines[mm].sort()
    for (rd,st) in texlines[mm]:
        fts[mm].write(st)
        
ss = "</table><p></html>"
for mm in xrange(len(lines)):
    fs[mm].write(ss)
