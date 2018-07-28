from ldmx_container import *
from math import sqrt 
from array import array 

def make_analysis_tree(input_file,output_file_name,coll_type_args={}):

    print "[make_analysis_tree] input_file:",input_file
    print "[make_analysis_tree] output_file:",output_file_name
    print "[make_analysis_tree] collection names:",coll_type_args

    s = ldmx_container(input_file)#,input_file)
    for arg in coll_type_args : 
        s.collection_type[arg]=coll_type_args[arg]
    s.setup()

    trigger_energy_sum = array('f',[0.])

    recoil_hits = array('i',[0]*10)
    recoil_charges = array('f',[0.]*10)

    ecalSP_recoil_px = array('f',[0.])
    ecalSP_recoil_py = array('f',[0.])
    ecalSP_recoil_pz = array('f',[0.])

    recoilTracker_simHit_recoil_px = array('f',[0.])
    recoilTracker_simHit_recoil_py = array('f',[0.])
    recoilTracker_simHit_recoil_pz = array('f',[0.])

    targetSP_recoil_px = array('f',[0.])
    targetSP_recoil_py = array('f',[0.])
    targetSP_recoil_pz = array('f',[0.])

    EcalVeto_recoil_px = array('f',[0.])
    EcalVeto_recoil_py = array('f',[0.])
    EcalVeto_recoil_pz = array('f',[0.])

    EcalVeto_BDT = array('f',[0.])

    PN_weight = array('f',[1.])

    findable_tracks = array('i',[0])

    max_side_hcal_pe = array('i',[0])
    max_back_hcal_pe = array('i',[0])
    sum_side_hcal_pe = array('i',[0])
    sum_back_hcal_pe = array('i',[0])
    min_dxy_2PE = array('f',[0])
    min_dxy_3PE = array('f',[0])
    min_dxy_8PE = array('f',[0])
    min_dxy_dz_2PE = array('f',[0])
    min_dxy_dz_3PE = array('f',[0])
    min_dxy_dz_8PE = array('f',[0])
    min_dz_2PE = array('f',[0])
    min_dz_3PE = array('f',[0])
    min_dz_8PE = array('f',[0])
    num_noise_hits = array('f',[0])

    output_tree = r.TTree("analysis_tree","analysis_tree")

    output_tree.Branch('trigger_energy_sum', trigger_energy_sum, 'trigger_energy_sum/F' )

    output_tree.Branch('recoil_hits', recoil_hits, 'recoil_hits[10]/I')
    output_tree.Branch('recoil_charges', recoil_charges, 'recoil_charges[10]/F')

    output_tree.Branch('max_side_hcal_pe', max_side_hcal_pe, 'max_side_hcal_pe/I' )
    output_tree.Branch('max_back_hcal_pe', max_back_hcal_pe, 'max_back_hcal_pe/I' )
    output_tree.Branch('sum_side_hcal_pe', sum_side_hcal_pe, 'sum_side_hcal_pe/I' )
    output_tree.Branch('sum_back_hcal_pe', sum_back_hcal_pe, 'sum_back_hcal_pe/I' )
    
    output_tree.Branch('min_dxy_2PE', min_dxy_2PE, 'min_dxy_2PE/F' )
    output_tree.Branch('min_dxy_3PE', min_dxy_3PE, 'min_dxy_3PE/F' )
    output_tree.Branch('min_dxy_8PE', min_dxy_8PE, 'min_dxy_8PE/F' )
    output_tree.Branch('min_dxy_dz_2PE', min_dxy_dz_2PE, 'min_dxy_dz_2PE/F' )
    output_tree.Branch('min_dxy_dz_3PE', min_dxy_dz_3PE, 'min_dxy_dz_3PE/F' )
    output_tree.Branch('min_dxy_dz_8PE', min_dxy_dz_8PE, 'min_dxy_dz_8PE/F' )
    output_tree.Branch('min_dz_2PE', min_dz_2PE, 'min_dz_2PE/F' )
    output_tree.Branch('min_dz_3PE', min_dz_3PE, 'min_dz_3PE/F' )
    output_tree.Branch('min_dz_8PE', min_dz_8PE, 'min_dz_8PE/F' )
    output_tree.Branch('num_noise_hits', num_noise_hits, 'num_noise_hits/F' )

    output_tree.Branch('findable_tracks', findable_tracks, 'findable_tracks/I' )

    output_tree.Branch('PN_weight', PN_weight, 'PN_weight/F' )

    output_tree.Branch('EcalVeto_BDT', EcalVeto_BDT, 'EcalVeto_BDT/F' )

    output_tree.Branch('EcalVeto_recoil_px', EcalVeto_recoil_px, 'EcalVeto_recoil_px/F' )
    output_tree.Branch('EcalVeto_recoil_py', EcalVeto_recoil_py, 'EcalVeto_recoil_py/F' )
    output_tree.Branch('EcalVeto_recoil_pz', EcalVeto_recoil_pz, 'EcalVeto_recoil_pz/F' )

    output_tree.Branch('ecalSP_recoil_px', ecalSP_recoil_px, 'ecalSP_recoil_px/F')
    output_tree.Branch('ecalSP_recoil_py', ecalSP_recoil_py, 'ecalSP_recoil_py/F')
    output_tree.Branch('ecalSP_recoil_pz', ecalSP_recoil_pz, 'ecalSP_recoil_pz/F')

    output_tree.Branch('recoilTracker_simHit_recoil_px', recoilTracker_simHit_recoil_px, 'recoilTracker_simHit_recoil_px/F')
    output_tree.Branch('recoilTracker_simHit_recoil_py', recoilTracker_simHit_recoil_py, 'recoilTracker_simHit_recoil_py/F')
    output_tree.Branch('recoilTracker_simHit_recoil_pz', recoilTracker_simHit_recoil_pz, 'recoilTracker_simHit_recoil_pz/F')

    output_tree.Branch('targetSP_recoil_px', targetSP_recoil_px, 'targetSP_recoil_px/F')
    output_tree.Branch('targetSP_recoil_py', targetSP_recoil_py, 'targetSP_recoil_py/F')
    output_tree.Branch('targetSP_recoil_pz', targetSP_recoil_pz, 'targetSP_recoil_pz/F')

    h = r.TH1F("h",";recoil p_{T} [MeV];Events",800,0.,100.)

    totEvents = s.tin.GetEntries()
    for i in xrange(totEvents):
        #if i >= 1000 : break
        if not i%1000 : print i,"/",totEvents
        s.getEvent(i)
        #s.dump()
        #break
        
        if s.ecalVeto[0].getDisc() < 0.90 : continue

        ecalSP_recoil_px[0]=0.
        ecalSP_recoil_py[0]=0.
        ecalSP_recoil_pz[0]=0.

        recoilTracker_simHit_recoil_px[0]=0.
        recoilTracker_simHit_recoil_py[0]=0.
        recoilTracker_simHit_recoil_pz[0]=0.
        
        targetSP_recoil_px[0]=0.
        targetSP_recoil_py[0]=0.
        targetSP_recoil_pz[0]=0.
        
        EcalVeto_recoil_px[0]=0.
        EcalVeto_recoil_py[0]=0.
        EcalVeto_recoil_pz[0]=0.
        
        EcalVeto_BDT[0]=0.
        
        PN_weight[0]=1.
        
        findable_tracks[0]=0
        
        max_side_hcal_pe[0]=0
        max_back_hcal_pe[0]=0
        sum_side_hcal_pe[0]=0
        sum_back_hcal_pe[0]=0
        min_dxy_8PE[0]=0
        min_dxy_2PE[0]=0
        min_dxy_3PE[0]=0
        min_dxy_dz_8PE[0]=0
        min_dxy_dz_2PE[0]=0
        min_dxy_dz_3PE[0]=0
        min_dz_8PE[0]=0
        min_dz_2PE[0]=0
        min_dz_3PE[0]=0

        num_noise_hits[0]=0

        s.recoil_hit_charges(recoil_charges)
        s.recoil_hit_counts(recoil_hits)

        ecalSP_recoil_px[0],ecalSP_recoil_py[0],ecalSP_recoil_pz[0]=s.getRecoil("ecalSPHits")
        recoilTracker_simHit_recoil_px[0],recoilTracker_simHit_recoil_py[0],recoilTracker_simHit_recoil_pz[0]=s.getRecoil("recoilHits")
        targetSP_recoil_px[0],targetSP_recoil_py[0],targetSP_recoil_pz[0]=s.getRecoil("targetSPHits")
        EcalVeto_recoil_px[0],EcalVeto_recoil_py[0],EcalVeto_recoil_pz[0]=s.ecalVeto[0].getRecoilMomentum()
        EcalVeto_BDT[0] = s.ecalVeto[0].getDisc()
        
        if s.pnWeight[0] != None : 
            PN_weight[0] = s.pnWeight[0].getWeight()
            
        goodTracks = map(lambda x : x.is4sFindable() or x.is3s1aFindable() or x.is2s2aFindable(),s.findableTracks)
    
        findable_tracks[0] = sum(goodTracks)

        # print "trigger var0:",s.trigger[0].getAlgoVar0()
        # print "trigger var1:",s.trigger[0].getAlgoVar1()
        # print "trigger var2:",s.trigger[0].getAlgoVar2()
        # print "trigger var3:",s.trigger[0].getAlgoVar3()
        # print "trigger var4:",s.trigger[0].getAlgoVar4()

        trigger_energy_sum[0] = s.trigger[0].getAlgoVar0()

        if s.hcalDigis[0] != None :
            side_hcal_pe = map(lambda x : x.getPE() if x.getSection() != 0 else 0 ,s.hcalDigis)
            back_hcal_pe = map(lambda x : x.getPE() if x.getSection() == 0 else 0 ,s.hcalDigis)
            dxy_2PE = map(lambda x : max(abs(x.getX()),abs(x.getY())) if x.getPE() >=2 and x.getSection()==0 else 99999.,s.hcalDigis)
            dxy_3PE = map(lambda x : max(abs(x.getX()),abs(x.getY())) if x.getPE() >=3 and x.getSection()==0 else 99999.,s.hcalDigis)
            dxy_8PE = map(lambda x : max(abs(x.getX()),abs(x.getY())) if x.getPE() >=8 and x.getSection()==0 else 99999.,s.hcalDigis)
            dz_2PE = map(lambda x : x.getZ() if x.getPE() >=2 and x.getSection()==0 else 99999.,s.hcalDigis)
            dz_3PE = map(lambda x : x.getZ() if x.getPE() >=3 and x.getSection()==0 else 99999.,s.hcalDigis)
            dz_8PE = map(lambda x : x.getZ() if x.getPE() >=8 and x.getSection()==0 else 99999.,s.hcalDigis)
            num_noise_hits[0] = sum(map(lambda x : x.getNoise() , s.hcalDigis))
            min_dxy_2PE[0] = min(dxy_2PE)
            min_dxy_3PE[0] = min(dxy_3PE)
            min_dxy_8PE[0] = min(dxy_8PE)
            min_dxy_dz_2PE[0] = dz_2PE[dxy_2PE.index(min(dxy_2PE))]
            min_dxy_dz_3PE[0] = dz_3PE[dxy_3PE.index(min(dxy_3PE))]
            min_dxy_dz_8PE[0] = dz_8PE[dxy_8PE.index(min(dxy_8PE))]
            min_dz_2PE[0] = min(dz_2PE)
            min_dz_3PE[0] = min(dz_3PE)
            min_dz_8PE[0] = min(dz_8PE)
            max_side_hcal_pe[0] = int(max(side_hcal_pe))
            sum_side_hcal_pe[0] = int(sum(side_hcal_pe))
            max_back_hcal_pe[0] = int(max(back_hcal_pe))
            sum_back_hcal_pe[0] = int(sum(back_hcal_pe))
        
        output_tree.Fill()

    output_file = r.TFile(output_file_name,'RECREATE')
    output_tree.Write()
    output_file.Close()

if __name__ == "__main__":
    make_analysis_tree(sys.argv[1],sys.argv[2])
