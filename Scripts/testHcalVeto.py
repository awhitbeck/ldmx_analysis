from ldmx_container import *
from math import sqrt 

s = ldmx_container(sys.argv[1])

totEvents = s.tin.GetEntries()
for i in xrange(totEvents):
    if i >= 5000 : break
    if not i%1000 : print i,"/",totEvents
    s.getEvent(i)

    hcal_pe = map(lambda x : x.getPE(),s.hcalDigis)
    max_PE = max(hcal_pe)
    sum_PE = sum(hcal_pe)

    print "max_PE:",max_PE
    print "sum_PE:",sum_PE
