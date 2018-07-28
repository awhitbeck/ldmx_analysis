#/bin/bash

base_dir="/nfs/slac/g/ldmx/users/whitbeck/recoil/analysis/root_files_v5/"

######## v5
#hadd -f /nfs/slac/g/ldmx/users/whitbeck/recoil/analysis/root_files_v5/ecal_pn_v5_magnet_bdt_skim_recon.root /nfs/slac/g/ldmx/users/whitbeck/recoil/analysis/root_files_v5/4pt0_gev_e_ecal_pn_v5_magnet_2pt8e11_eot_*_bdt_skim_recon.root

hadd -f ${base_dir}/reco_ntran_4pt0_gev_e_target_muon_v3_magnet_20170907.root ${base_dir}/reco_ntran_4pt0_gev_e_target_muon_v3_magnet_20170907_*.root

hadd -f ${base_dir}/reco_ntran_4pt0_gev_e_ecal_muon_v3_magnet.root ${base_dir}/reco_ntran_4pt0_gev_e_ecal_muon_v3_magnet_2*.root

#hadd -f /nfs/slac/g/ldmx/users/whitbeck/recoil/analysis/root_files_v5/ecal_pn_v5_magnet_recon.root /nfs/slac/g/ldmx/users/whitbeck/recoil/analysis/root_files_v5/4pt0_gev_e_ecal_pn_v5_magnet_4pt5e7_eot_*_tskim_resim_recon.root

#hadd -f /nfs/slac/g/ldmx/users/whitbeck/recoil/analysis/root_files_v5/reco_e_target_en_v3_magnet_4pt0_gev_recon.root /nfs/slac/g/ldmx/users/whitbeck/recoil/analysis/root_files_v5/reco_e_target_en_v3_magnet_4pt0_gev_*_recon.root

#hadd -f /nfs/slac/g/ldmx/users/whitbeck/recoil/analysis/root_files_v5/target_pn_v5_magnet_recon.root /nfs/slac/g/ldmx/users/whitbeck/recoil/analysis/root_files_v5/4pt0_gev_e_target_pn_v3_magnet_*_tskim_recon_merge_recon.root

#hadd -f /nfs/slac/g/ldmx/users/whitbeck/recoil/analysis/root_files_v5/signal_mA_1p0_recon.root /nfs/slac/g/ldmx/users/whitbeck/recoil/analysis/root_files_v5/LDMX_W_UndecayedAP.4.0GeV.W.pMax.2.0.mA.1.0.*_unweighted_events_recon.root

#hadd -f /nfs/slac/g/ldmx/users/whitbeck/recoil/analysis/root_files_v5/signal_mA_0p1_recon.root /nfs/slac/g/ldmx/users/whitbeck/recoil/analysis/root_files_v5/LDMX_W_UndecayedAP.4.0GeV.W.pMax.2.0.mA.0.1.*_unweighted_events_recon.root

#hadd -f /nfs/slac/g/ldmx/users/whitbeck/recoil/analysis/root_files_v5/signal_mA_0p01_recon.root /nfs/slac/g/ldmx/users/whitbeck/recoil/analysis/root_files_v5/LDMX_W_UndecayedAP.4.0GeV.W.pMax.2.0.mA.0.01.*_unweighted_events_recon.root

#hadd -f /nfs/slac/g/ldmx/users/whitbeck/recoil/analysis/root_files_v5/signal_mA_0p001_recon.root /nfs/slac/g/ldmx/users/whitbeck/recoil/analysis/root_files_v5/LDMX_W_UndecayedAP.4.0GeV.W.pMax.2.0.mA.0.001.*_unweighted_events_recon.root