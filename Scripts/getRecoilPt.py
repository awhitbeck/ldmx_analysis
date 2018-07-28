from ldmx_container import *
from math import sqrt 
from array import array 

r.gROOT.SetBatch(True)
r.gROOT.ProcessLine(".L ~/tdrstyle.C")
r.gROOT.ProcessLine("setTDRStyle()")

s = ldmx_container(sys.argv[1])

#px = array('f',[])
#py = array('f',[])
#pz = array('f',[])

h = r.TH1F("h",";recoil p_{T} [MeV];Events",800,0.,100.)

totEvents = s.tin.GetEntries()
for i in xrange(totEvents):
    if i >= 5000 : break
    if not i%1000 : print i,"/",totEvents
    s.getEvent(i)

    ecal_recoil = s.ecalVeto[0].getRecoilMomentum()
    findable_tracks = s.findableTracks
    findable_dic = {}
    for findable_track in findable_tracks:
        #print ",".join(map(str,findable_track.getSimParticle().getMomentum()))
        if findable_track.is4sFindable() or findable_track.is3s1aFindable() or findable_track.is2s2aFindable() : 
            findable_dic[findable_track.getSimParticle()] = findable_track

    if len(findable_dic) != 1 : continue

    findable_track = findable_dic.itervalues().next()
    sim_particle = findable_track.getSimParticle()
    p_find = sqrt(sum(map(lambda x: x*x,sim_particle.getMomentum())))
    min_mom_diff = 10000
    for hit in s.ecalSPHits : 
        if hit.getSimParticle() != sim_particle : continue
        pvec = hit.getMomentum()
        if pvec[2] < 0. : continue
        p = sqrt(sum(map(lambda x: x*x,pvec)))
        pt = sqrt(pvec[0]*pvec[0]+pvec[1]*pvec[1])
        if ( p_find - p ) < min_mom_diff :
            if p < 1.2 and pvec[2] > 0. :
                print "recoil momentum:",p," pt:",pt
                print "ecal momentum:",sqrt(sum(map(lambda x: x*x,ecal_recoil)))," pt:",sqrt(ecal_recoil[0]*ecal_recoil[0]+ecal_recoil[1]*ecal_recoil[1])
                h.Fill(pt)

can = r.TCanvas("can","can",500,500)
can.SetLogy()
h.Draw()
can.SaveAs("testPt.png")
