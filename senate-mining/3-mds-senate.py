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
import string, math
from orngInteract import *
import MDSGUI

i=8
n = 'us-senate-10%d'%i
#mod = ''
mod = '-m' # missing value handling
t = orange.ExampleTable('%s%s.tab'%(n,mod))
try:
    im = cPickle.load(open('dep-%s%s.pik'%(n,mod),'r'))
except:
    im = InteractionMatrix(t,prepare=0,interactions_too=0,dependencies_too=1,save_data=0)
    cPickle.dump(im,open('dep-%s%s.pik'%(n,mod),'w'))

(diss,labels) = im.depExportDissimilarityMatrix(jaccard=1,color_coding = 1,include_label=1)

# do MDS
MDSGUI.Run(diss,names=labels)