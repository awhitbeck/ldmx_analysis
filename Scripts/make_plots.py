import ROOT as r
from test import *

r.gROOT.SetBatch(True)

plots=[]

plots.append(('recoil_hits[9]','recoil_layer_10_hit_mult_hcal_veto','(10,-0.5,9.5)','Recoil tracker layer 10 Edep [MeV]','findable_tracks==1&&trigger_energy_sum<1500.&&EcalVeto_BDT>0.94&&max_back_hcal_pe<3&&max_side_hcal_pe<3'))

plots.append(('recoil_hits[9]','recoil_layer_10_hit_mult','(10,-0.5,9.5)','Recoil tracker layer 10 Edep [MeV]','findable_tracks==1&&trigger_energy_sum<1500.&&EcalVeto_BDT>0.94'))

plots.append(('recoil_charges[9]','recoil_layer_10_charge_hcal_veto','(50,0.,5.)','Recoil tracker layer 10 Edep [MeV]','findable_tracks==1&&trigger_energy_sum<1500.&&EcalVeto_BDT>0.94&&max_back_hcal_pe<3&&max_side_hcal_pe<3'))

plots.append(('recoil_charges[0]','recoil_layer_1_charge','(50,0.,5.)','Recoil tracker layer 1 Edep [MeV]','findable_tracks==1&&trigger_energy_sum<1500.&&EcalVeto_BDT>0.94'))

plots.append(('max(max_back_hcal_pe,max_side_hcal_pe)','max_pe_bdt_skim','(50,-0.5,49.5)','Max PE','findable_tracks==1&&trigger_energy_sum<1500.&&EcalVeto_BDT>0.94'))

plots.append(('sqrt(recoilTracker_simHit_recoil_py**2+recoilTracker_simHit_recoil_px**2)','recoil_e_pt_bdt_skim_hcal_veto_fine','(50,0.5,100.5)','Recoil-e p_{T} [MeV]','findable_tracks==1&&trigger_energy_sum<1500.&&EcalVeto_BDT>0.94&&max_back_hcal_pe<3&&max_side_hcal_pe<3'))

plots.append(('sqrt(recoilTracker_simHit_recoil_py**2+recoilTracker_simHit_recoil_px**2)','recoil_e_pt_bdt_skim_hcal_veto','(5,0.5,50.5)','Recoil-e p_{T} [MeV]','findable_tracks==1&&trigger_energy_sum<1500.&&EcalVeto_BDT>0.94&&max_back_hcal_pe<3&&max_side_hcal_pe<3'))

plots.append(('sqrt(recoilTracker_simHit_recoil_py**2+recoilTracker_simHit_recoil_px**2)','recoil_e_pt_bdt_skim_hcal_sb_fine','(50,0.5,100.5)','Recoil-e p_{T} [MeV]','findable_tracks==1&&trigger_energy_sum<1500.&&EcalVeto_BDT>0.94&&max_back_hcal_pe<3&&max_side_hcal_pe>=3'))

plots.append(('sqrt(recoilTracker_simHit_recoil_py**2+recoilTracker_simHit_recoil_px**2)','recoil_e_pt_bdt_skim_hcal_sb','(5,0.5,50.5)','Recoil-e p_{T} [MeV]','findable_tracks==1&&trigger_energy_sum<1500.&&EcalVeto_BDT>0.94&&max_back_hcal_pe<3&&max_side_hcal_pe>=3'))

plots.append(('EcalVeto_BDT','ecal_bdt_tight_hcal_veto','(6,0.94,1.0)','ECal BDT score','findable_tracks==1&&trigger_energy_sum<1500.&&max_back_hcal_pe<3&&max_side_hcal_pe<3'))

plots.append(('sum_back_hcal_pe+sum_side_hcal_pe','sum_pe_bdt_skim_tight_hcal_veto','(25,-0.5,24.5)','Sum PE','findable_tracks==1&&trigger_energy_sum<1500.&&max_back_hcal_pe<3&&max_side_hcal_pe<3&&EcalVeto_BDT>0.94'))

for p in plots : 
    if p[0] == 'EcalVeto_BDT':
        plot_var(*p+(True,True,False))
        plot_var(*p+(True,False,False))
        plot_var(*p+(False,True,False))
        plot_var(*p+(False,False,False))
    else : 
        plot_var(*p+(True,True,True))
        plot_var(*p+(True,False,True))
        plot_var(*p+(False,True,True))
        plot_var(*p+(False,False,True))
