import os
from make_analysis_tree import *

input_dirs = {#"signal_1GeV":"/nfs/slac/g/ldmx/data/mc/v5-magnet//4pt0_gev_signal_mc_pmax2pt0_gev/recon/",
              #"ecal_PN":"/nfs/slac/g/ldmx/data/mc/v5-magnet/4pt0_gev_e_ecal_pn/bdt_skim/",
              #"target_EN":"/nfs/slac/g/ldmx/data/mc/v3-magnet/4pt0_gev_e_target_en/bdt_skim/",
              #"ecal_PN_train":"/nfs/slac/g/ldmx/data/mc/v5-magnet/4pt0_gev_e_ecal_pn/recon/",
              'ecal_gmumu':'/nfs/slac/g/ldmx/data/mc/v3-magnet/4pt0_gev_e_ecal_mumu/sim-reco-180118/',
              #'target_gmumu':'/nfs/slac/g/ldmx/data/mc/v3-magnet/4pt0_gev_e_target_mumu/sim-reco-171130/',
              }

for i in input_dirs: 

    input_files = []
    for (dp, d, f) in os.walk(input_dirs[i])
        input_files.extend(map(lambda x : dp+'/'+x,f))

    #input_files = os.listdir(input_dirs[i])
    print i,input_files[0]
    if i == 'ecal_muons' or i == 'target_muons':
        print "make_analysis_tree(input_files[0],input_files[0].split('/')[-1][:-5]+'_test.root',{'ecalVeto':('ldmx::EcalVetoResult','EcalVeto_reco'),'hcalVeto':('ldmx::HcalVetoResult','HcalVeto_reco')})"
        make_analysis_tree(input_files[0],input_files.split('/')[-1][:-5]+'_test.root',{'ecalVeto':('ldmx::EcalVetoResult','EcalVeto_reco'),'hcalVeto':('ldmx::HcalVetoResult','HcalVeto_reco')})
    else :
        print "make_analysis_tree(input_files[0],input_files[0].split('/')[-1][:-5]+'_test.root')"
        make_analysis_tree(input_files[0],input_files[0].split('/')[-1][:-5]+'_test.root')
