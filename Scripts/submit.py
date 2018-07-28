import os
from make_analysis_tree import *

BASE_DIR=os.getcwd()
SW_DIR=BASE_DIR+'/../ldmx-sw/ldmx-sw-install/'
OUTPUT_DIR='/nfs/slac/g/ldmx/users/whitbeck/recoil/analysis/root_files_v5/'
#OUTPUT_DIR='/nfs/slac/g/ldmx/users/whitbeck/recoil/analysis/root_files_v6/'

input_dirs = {#"signal_1GeV":"/nfs/slac/g/ldmx/data/mc/v5-magnet//4pt0_gev_signal_mc_pmax2pt0_gev/recon/",
              #"ecal_PN":"/nfs/slac/g/ldmx/data/mc/v5-magnet/4pt0_gev_e_ecal_pn/bdt_skim/",
              #"ecal_PN_train":"/nfs/slac/g/ldmx/data/mc/v5-magnet/4pt0_gev_e_ecal_pn/recon/",
              #"target_PN":"/nfs/slac/g/ldmx/data/mc/v3-magnet/4pt0_gev_e_target_pn/bdt_skim/",
              #"target_EN":"/nfs/slac/g/ldmx/data/mc/v3-magnet/4pt0_gev_e_target_en/bdt_skim/",
              'ecal_gmumu':'/nfs/slac/g/ldmx/data/mc/v3-magnet/4pt0_gev_e_ecal_mumu/sim-reco-180118/',
              #'target_gmumu':'/nfs/slac/g/ldmx/data/mc/v3-magnet/4pt0_gev_e_target_mumu/sim-reco-171130/',
              }

for i in input_dirs: 
    input_files = []    
    for (dp, d, f) in os.walk(input_dirs[i]):
        input_files.extend(map(lambda x : dp+'/'+x,f))

    for f,input_file in enumerate(input_files) : 
        print input_file
        print 'output_dir',OUTPUT_DIR
        print 'base_dir',BASE_DIR
        print 'input_file',input_file
        print 'output_file',input_file.split('/')[-1]
        #print 'bash worker.sh {2} {3} {4} {5}'.format(BASE_DIR,input_file.split('/')[-1][:-5],OUTPUT_DIR,BASE_DIR,input_file,input_file.split('/')[-1])
        os.system('bsub -q short -o /nfs/slac/g/ldmx/users/whitbeck/recoil/analysis//logs_v5/output_{1}.log "bash worker.sh {2} {3} {4} {5}"'.format(BASE_DIR,input_file.split('/')[-1][:-5],OUTPUT_DIR,BASE_DIR,input_file,input_file.split('/')[-1]))
