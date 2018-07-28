from ldmx_container import *
from math import sqrt
from array import array

s = ldmx_container('/nfs/slac/g/ldmx/data/mc/v5-magnet//4pt0_gev_signal_mc_pmax2pt0_gev/recon/*0.1*root')
#s = ldmx_container('/nfs/slac/g/ldmx/data/mc/v5-magnet/4pt0_gev_e_ecal_pn/bdt_skim/4pt0_gev_e_ecal_pn_v5_magnet_2pt8e11_eot_20180327_0002925_bdt_skim_recon.root',
#                   '/nfs/slac/g/ldmx/data/mc/v5-magnet/4pt0_gev_e_ecal_pn/bdt_skim/4pt0_gev_e_ecal_pn_v5_magnet_2pt8e11_eot_20180327_0002925_bdt_skim_recon.root')
s.setup()
for i in xrange(s.tin.GetEntries()):
    if i >= 10: break
    s.getEvent(i)
    #s.dump('simParticles')
    #s.dump('targetSPHits')
    
    goodTracks = map(lambda x : x.is4sFindable() or x.is3s1aFindable() or x.is2s2aFindable(),s.findableTracks)
    findable_tracks = sum(goodTracks)
    if findable_tracks != 1 : continue

    pdg = map(lambda x : x.getSimParticle().getPdgID(),s.targetSPHits)
    pdg_sim = map(lambda x : x.getPdgID(),s.simParticles)
    
    pt_sp = map(lambda x : sqrt(x.getMomentum()[0]**2+x.getMomentum()[1]**2) if x.getID()==40 and x.getSimParticle().getPdgID()==11 else -1.,s.targetSPHits)
    pt_all_sp = map(lambda x : sqrt(x.getMomentum()[0]**2+x.getMomentum()[1]**2),s.targetSPHits)
    pt_sim = map(lambda x : sqrt(x.getMomentum()[0]**2+x.getMomentum()[1]**2) if x.getPdgID()==11 else -1.,s.simParticles)
    
    p_sp = map(lambda x : sqrt(x.getMomentum()[0]**2+x.getMomentum()[1]**2+x.getMomentum()[2]**2) if x.getID()==40 and x.getSimParticle().getPdgID()==11 else -1.,s.targetSPHits)
    p_all_sp = map(lambda x : sqrt(x.getMomentum()[0]**2+x.getMomentum()[1]**2+x.getMomentum()[2]**2),s.targetSPHits)
    p_sim = map(lambda x : sqrt(x.getMomentum()[0]**2+x.getMomentum()[1]**2+x.getMomentum()[2]**2) if x.getPdgID()==11 else -1.,s.simParticles)
    
    recoil = s.getRecoil('targetSPHits')
    
    print 'pdg',pdg
    print 'pdg_sim',pdg_sim
    print 'pt_sp',pt_sp
    print 'pt_all_sp',pt_all_sp
    print 'pt_sim',pt_sim
    print 'pt_getRecoil',sqrt(recoil[0]**2+recoil[1]**2)
    
    # print 'p_sp',p_sp
    # print 'p_all_sp',p_all_sp
    # print 'p_sim',p_sim
    # print 'p_getRecoil',sqrt(recoil[0]**2+recoil[1]**2+recoil[2]**2)
    
