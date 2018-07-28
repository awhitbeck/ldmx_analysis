from test import *

histos_hcal_sb = plot_var('sqrt(targetSP_recoil_py*targetSP_recoil_py+targetSP_recoil_px*targetSP_recoil_px)','recoil_e_pt_hcal_sideband','(50,0.5,50.5)','Recoil-e p_{T} [MeV]','findable_tracks==1&&trigger_energy_sum<1500.&&EcalVeto_BDT>0.94&&max_back_hcal_pe>=3&&max_side_hcal_pe>=3',False,False,True)

histos_ecal_sb = plot_var('sqrt(targetSP_recoil_py*targetSP_recoil_py+targetSP_recoil_px*targetSP_recoil_px)','recoil_e_pt_ecal_sideband','(50,0.5,50.5)','Recoil-e p_{T} [MeV]','findable_tracks==1&&trigger_energy_sum<1500.&&EcalVeto_BDT<0.94&&max_back_hcal_pe<3&&max_side_hcal_pe<3',False,False,True)

histos = plot_var('sqrt(targetSP_recoil_py*targetSP_recoil_py+targetSP_recoil_px*targetSP_recoil_px)','recoil_e_pt_ecal_sideband','(50,0.5,50.5)','Recoil-e p_{T} [MeV]','findable_tracks==1&&trigger_energy_sum<1500.&&EcalVeto_BDT>0.94&&max_back_hcal_pe<3&&max_side_hcal_pe<3',False,False,True)

can = r.TCanvas('can','can',500,500)
can.SetLogy()

histos_hcal_sb['ecal_pn'].SetLineColor(6)
histos_hcal_sb['ecal_pn'].SetMarkerColor(6)
histos_hcal_sb['ecal_pn'].SetLineStyle(2)
histos_hcal_sb['ecal_pn'].SetLineWidth(3)
histos_hcal_sb['ecal_pn'].Scale(1./histos_hcal_sb['ecal_pn'].Integral())

histos_ecal_sb['ecal_pn_inc'].SetLineColor(2)
histos_ecal_sb['ecal_pn_inc'].SetMarkerColor(2)
histos_ecal_sb['ecal_pn_inc'].SetLineStyle(2)
histos_ecal_sb['ecal_pn_inc'].SetLineWidth(3)
histos_ecal_sb['ecal_pn_inc'].Scale(1./histos_ecal_sb['ecal_pn_inc'].Integral())

histos['ecal_pn'].SetLineColor(1)
histos['ecal_pn'].SetMarkerColor(1)
histos['ecal_pn'].SetLineStyle(1)
histos['ecal_pn'].SetLineWidth(3)
histos['ecal_pn'].Scale(1./histos['ecal_pn'].Integral())
histos['ecal_pn'].GetYaxis().SetRangeUser(histos_hcal_sb['ecal_pn'].GetMinimum()/10.,histos_hcal_sb['ecal_pn'].GetMaximum()*10.)
histos['ecal_pn'].GetYaxis().SetTitle('Events (a.u.)')

histos['ecal_pn'].Draw('hist,e1')
histos_hcal_sb['ecal_pn'].Draw('hist,e1,same')
histos_ecal_sb['ecal_pn_inc'].Draw('hist,e1,same')


leg = r.TLegend(0.2,.85,.9,.92)
leg.SetNColumns(5)
leg.SetBorderSize(0)
leg.SetFillColor(0)
leg.AddEntry(histos_hcal_sb['ecal_pn'],'hcal sideband','l')
leg.AddEntry(histos_ecal_sb['ecal_pn_inc'],'ecal sideband','l')
leg.AddEntry(histos['ecal_pn'],'signal region','l')
leg.Draw()

can.SaveAs('checkRecoilPtCorrelations.png')
