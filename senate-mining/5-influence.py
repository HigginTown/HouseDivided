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

import orange,string
from orngContingency import *

n = 'us-senate-108'
mod = ''

t = orange.ExampleTable('%s%s.tab'%(n,mod))
labels = []
states = {} # list of reps from a particular state
parties = {}
lparties = {}
for i in xrange(len(t.domain.attributes)):
    a = t.domain.attributes[i]
    labels.append(a.name)
    state = str(a.name)[-3:-1]
    try:
        states[state].append(i)
        lparties[state].append(str(a.name)[-5])
        if parties[state] == str(a.name)[-5]:
            parties[state] = 1 # cohesive
        else:
            parties[state] = 0 # uncohesive
    except:
        states[state] = [i]
        parties[state] = str(a.name)[-5]
        lparties[state] = [str(a.name)[-5]]

# mutual informations
inf = []
miLUT = []
ll = []
tl = []
for i in xrange(len(t.domain.attributes)):
    a = t.domain.attributes[i]
    c = get2Int(t,a,t.domain.classVar)
    cEnt = Entropy(c.b)
    mi = c.InteractionInformation()
    miLUT.append(mi)
    nmi = mi/cEnt
    jmi = c.JaccardInteraction()
    agr = c.pm[1,0]+c.pm[2,1] # how often the vote agreed with the outcome
    nv = c.pm[0,0]+c.pm[0,1] # how often not-voted
    inf.append((nmi,jmi,agr,nv))
    ll.append((nmi,"%s\t%f\t%f\t%f\t%f"%(a.name,nmi,1-jmi,agr,nv)))
    ap = string.split(str(a.name))
    tl.append((nmi,"%s&%s&%2.1f&%2.1f&%2.1f \\\\ \n"%(ap[0],ap[1],100*nmi,100*agr,100*nv)))
ll.sort()
ll.reverse()
print "Senator\tExplains\tRajskiD\tAgreement\tNotVotingP"
tl.sort()
tl.reverse()
for (q,s) in ll:
    print s
f = open('influence-senator.tex','w')
for (q,s) in tl:
    f.write(s)
    

# state-wide
ll = []
def getv(v):
    return int(str(v))

tl = []
for (state,reps) in states.items():
    [ia,ib] = reps
    a = t.domain.attributes[ia]
    b = t.domain.attributes[ib]
    N = ['Joint',b.name]
    nj = len(t.domain.classVar.values)

    # merge the votes into a sum: don't distinguish between not-voting and conflicting voting
    ni = 5
    M = Numeric.zeros((ni,nj),Numeric.Float)
    for ex in t:
        q = 0
        for att in [a,b]:
            if getv(ex[att]) == 0:
                q -= 1
            elif getv(ex[att]) == 1:
                q += 1
        M[2+q,int(ex.getclass())] += 1
    V = [['-2','-1','0','1','2'],[t.domain.classVar.values[k] for k in range(nj)]]
    c = ContingencyTable2(M,N,V)

    # merge the votes into a sum: don't distinguish between not-voting and conflicting voting
    ni = 6
    M = Numeric.zeros((ni,nj),Numeric.Float)
    for ex in t:
        if (getv(ex[a]) == 0 and getv(ex[b]) == 1) or (getv(ex[a]) == 1 and getv(ex[b]) == 0):
            q = 3 # conflicting voting
        else:
            q = 0
            for att in [a,b]:
                if getv(ex[att]) == 0:
                    q -= 1
                elif getv(ex[att]) == 1:
                    q += 1
        M[2+q,int(ex.getclass())] += 1
    V = [['-2','-1','0','1','2','X'],[t.domain.classVar.values[k] for k in range(nj)]]
    d = ContingencyTable2(M,N,V)


    ii = (c.InteractionInformation())/cEnt
    ji = (d.InteractionInformation())/cEnt
    qi = (miLUT[ia]+miLUT[ib]+get3Int(t,a,b,t.domain.classVar).InteractionInformation())/cEnt
    ll.append((ji,"%s\t%d\t%f\t%f\t%f"%(state,parties[state],ii,ji,qi)))
    lp = lparties[state]
    lp.sort()
    assert(len(lp)==2)
    tl.append((ii,"%s&%s+%s&%2.1f \\\\ \n"%(state,lp[0],lp[1],100*ii)))
    
ll.sort()
ll.reverse()
tl.sort()
tl.reverse()
print "State\tCohesive?\tExplains(Simple)\tExplains(Sym)\tExplains(Asym)"
for (q,s) in ll:
    print s
f = open('influence-party.tex','w')
for (q,s) in tl:
    f.write(s)
