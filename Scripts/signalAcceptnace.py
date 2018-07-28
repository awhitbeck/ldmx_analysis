from test import *
from array import array

histos = plot_var('sqrt(targetSP_recoil_py*targetSP_recoil_py+targetSP_recoil_px*targetSP_recoil_px)','recoil_e_pt_ecal_sideband','(50,0.5,50.5)','Recoil-e p_{T} [MeV]','findable_tracks==1&&trigger_energy_sum<1500.&&EcalVeto_BDT>0.94&&max_back_hcal_pe<3&&max_side_hcal_pe<3',False,False,True,True)

events = {'0p001':1801407.,
          '0p01':2880916.,
          '0p1':1653273.,
          '1p0':1622770.}

acceptance=[]
DMmass = []
for s in events : 
    print s.replace('p','.')+':',histos[s].Integral()/dm_target_weight[s]/events[s]
    acceptance.append(histos[s].Integral()/dm_target_weight[s]/events[s])
    DMmass.append(float(s.replace('p','.'))/3.)

can = r.TCanvas('can','can',500,500)
can.SetLogx()
graph = r.TGraph(len(DMmass),array('f',DMmass),array('f',acceptance))
graph.GetXaxis().SetTitle("m_{#chi} [MeV]")
graph.GetYaxis().SetTitle("Signal Acceptance")
graph.SetMarkerStyle(8)
graph.Draw("Ap")
can.SaveAs('signalAcceptance.png')
