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

import time, string
import piddle, piddlePIL, math
import orange

t = orange.ExampleTable("/cache/proj/politics/exp/votes/a-us-senate-108.tab")

fs = []
fts = []
for i in xrange(5):
    fs.append(open('removal-%d.html'%i,'w'))
    fts.append(open('removal-%d.tex'%i,'w'))
    
# new 3
oth=[0.000067,0.007591,0.002238,0.000000,0.000005]
dem=[0.003435,0.409964,0.047890,0.001346,0.012614]
rep=[0.026974,0.001813,0.002866,0.136832,0.336465]

ord = []
for i in xrange(len(oth)):
    ord.append(dem[i]-rep[i])    
iord = [(ord[i],i) for i in range(len(ord))]
iord.sort()

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
edif = [0] * 5
dif = [0] * 5
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
ss += '<tr> <td>A</tr> <td>B</td> <td>C</td> <td>D</td> <td>E</td> <td>OUT</td> <td>dif</td> <td>A-</td> <td>B-</td> <td>C-</td> <td>D-</td> <td>E-</td> </tr>'

print ss

lines = []
texlines = []
for f in fs:
    f.write(ss)
    lines.append([])
    texlines.append([])
    
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

    def old_predictoutcome(xy,xn,xv,a,b):    
        thresh = (float(xy+xn)*a/b)
        xthresh = (float(xy+xn+xv)*a/b)
        if ((xy) >= thresh and not ((xy) == thresh and (xy) < xthresh)):
            return 1
        else:
            return 0

    def xpredictoutcome(xy,xn,xv,a,b):
        thresh = (float(xy+xn+1)*a/b)
        if a == 3 and b == 5:
            thresh = (float(100)*a/b)
        #if ((xy) >= thresh and not ((xy) == thresh and (xy) < xthresh)):
        if ((xy) >= thresh):            
            return 1
        else:
            return 0
        
    def predictoutcome(xy,xn,xv,a,b):
        aa = ((b-a)*xy)
        bb = ((a)*xn)
        if abs(aa-bb) < 1.00:
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
    ss += "<tr>"
    texs = ""
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

    # [base,demo-,rep-1,rep-2,rep-12]
    rate = ny
    oo = []
    rdif = [] # rate differences for line sorting
    for mm in [[0,1,2,3,4],[1,2,3,4],[0,2,3,4],[0,1,3,4],[0,1,2,4],[0,1,2,3]]:
        ey = 0.0
        en = 0.0
        env = 0.0
        for m2 in mm:
            ey += counts[m2][0][0]
            en += counts[m2][0][1]
            env += counts[m2][0][2]
        o2 = predictoutcome((ey),(en),(env),a,b)
        c = 255*(1-o2)
        rate2 = ey*(ny+nn)/(ey+en)
        if len(mm) < 5:
            # skip the default
            if ot != o2:
                # vote changed
                # compute inverted text color
                if c < 100:
                    ih = 255.0
                else:
                    ih = 0.0
                ss += '<td bgcolor="#%02x%02x%02x"><font color="#%02x%02x%02x">%2.1f</font></td>'%(c,c,c,ih,ih,ih,(rate2-rate)) # error
                texx = "\\cellcolor{gr%d}\\color{gr%d}{\\tiny\\hspace{-5pt} %2.1f:%2.1f\\hspace{-5pt}}&"%(c,ih,ey,en)
                texx += " %s & %s \\\\\\hline\n"%(str(t[i][103]),str(t[i][104]))
                texlines[len(oo)-1].append((rate2-rate,texs+texx))
            else:
                # didn't change
                ss += '<td bgcolor="#%02x%02x%02x">&nbsp;&nbsp;&nbsp;&nbsp;</td>'%(c,c,c) # error
            rdif.append(rate2-rate)
        if oo == []:
            rate = rate2
        oo.append(o2)

    ss += '<td>%s</td>'%(str(t[i][103]))
    ss += '<td>%s</td>'%(str(t[i][104]))
    ss += '<td>%s</td>'%(str(t[i][106]))
    ss += "</tr>"

    # is MPCA correct w/r threshold
    # Verify swings
    for mm in range(5):
        if ot != oo[1+mm] and oo[1+mm] != 0.5:
            edif[mm] += 1        
            lines[mm].append((rdif[mm],ss))
    # is MPCA correct also w/r true vote
    # exclude tables and clotures
    if string.find(str(t[i][106]),"Table")==-1 and string.find(str(t[i][106]),"Cloture")==-1:
        for mm in range(5):
            if ot != oo[1+mm] and oo[1+mm] != 0.5:
                dif[mm] += 1
    print ss

# print sorted lines
for mm in range(5):
    lines[mm].sort()
    texlines[mm].sort()
    for (rd,st) in lines[mm]:
        fs[mm].write(st)
    for (rd,st) in texlines[mm]:
        fts[mm].write(st)


ss = "</table><p>"
print ss
for f in fs:
    f.write(ss)

print "if-bloc-abstained swings w/r                       ",edif,"<br>"
print "if-bloc-abstained swings w/out Tabling and Cloture ",dif,"<br>"

ss = "</html>"
print ss
for f in fs:
    f.write(ss)
    
