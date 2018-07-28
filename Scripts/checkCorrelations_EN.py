from test import *

histos_hcal_sb = plot_var('sqrt(recoilTracker_simHit_recoil_py*recoilTracker_simHit_recoil_py+recoilTracker_simHit_recoil_px*recoilTracker_simHit_recoil_px)','recoil_e_pt_hcal_sideband','(50,0.5,50.5)','Recoil-e p_{T} [MeV]','findable_tracks==1&&trigger_energy_sum<1500.&&EcalVeto_BDT>0.94&&max_back_hcal_pe>=3&&max_side_hcal_pe>=3',False,False,True)

histos_ecal_sb = plot_var('sqrt(recoilTracker_simHit_recoil_py*recoilTracker_simHit_recoil_py+recoilTracker_simHit_recoil_px*recoilTracker_simHit_recoil_px)','recoil_e_pt_ecal_sideband','(50,0.5,50.5)','Recoil-e p_{T} [MeV]','findable_tracks==1&&trigger_energy_sum<1500.&&EcalVeto_BDT<0.94&&max_back_hcal_pe<3&&max_side_hcal_pe<3',False,False,True)

histos = plot_var('sqrt(recoilTracker_simHit_recoil_py*recoilTracker_simHit_recoil_py+recoilTracker_simHit_recoil_px*recoilTracker_simHit_recoil_px)','recoil_e_pt_ecal_sideband','(50,0.5,50.5)','Recoil-e p_{T} [MeV]','findable_tracks==1&&trigger_energy_sum<1500.&&EcalVeto_BDT>0.94&&max_back_hcal_pe<3&&max_side_hcal_pe<3',False,False,True)

histos_hcal_sb['target_en'].Print('all')
histos_ecal_sb['target_en'].Print('all')

can = r.TCanvas('can','can',500,500)
can.SetLogy()

histos_hcal_sb['target_en'].SetLineColor(6)
histos_hcal_sb['target_en'].SetMarkerColor(6)
histos_hcal_sb['target_en'].SetLineStyle(2)
histos_hcal_sb['target_en'].SetLineWidth(3)
histos_hcal_sb['target_en'].Scale(1./histos_hcal_sb['target_en'].Integral())

histos['target_en'].SetLineColor(1)
histos['target_en'].SetMarkerColor(1)
histos['target_en'].SetLineStyle(1)
histos['target_en'].SetLineWidth(3)
histos['target_en'].Scale(1./histos['target_en'].Integral())
histos['target_en'].GetYaxis().SetRangeUser(histos_hcal_sb['target_en'].GetMinimum()/10.,histos_hcal_sb['target_en'].GetMaximum()*10.)
histos['target_en'].GetYaxis().SetTitle('Events (a.u.)')

histos['target_en'].Draw('hist,e1')
histos_hcal_sb['target_en'].Draw('hist,e1,same')

leg = r.TLegend(0.2,.85,.9,.92)
leg.SetNColumns(5)
leg.SetBorderSize(0)
leg.SetFillColor(0)
leg.AddEntry(histos_hcal_sb['target_en'],'hcal sideband','l')
leg.AddEntry(histos['target_en'],'signal region','l')
leg.Draw()

can.SaveAs('checkRecoilPtCorrelations_EN.png')
