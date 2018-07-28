from sampleInfo import *
from test import *
from array import array

plotVar = 'sqrt(recoilTracker_simHit_recoil_py**2+recoilTracker_simHit_recoil_px**2)'

histos = plot_var(plotVar,'recoil_e_pt_ecal_sideband','(50,0.5,100.5)','Recoil-e p_{T} [MeV]','findable_tracks==1&&trigger_energy_sum<1500.&&EcalVeto_BDT>0.94&&max_back_hcal_pe<3&&max_side_hcal_pe<3',False,False,True)

signals = ['0p001','0p01','0p1','1p0']
mA = array('f',[])
mChi = array('f',[])
UL = array('f',[])

for s in signals:
    mA.append(float(s.replace('p','.')))
    mChi.append(mA[-1]/3.)
    tot_yield = histos[s].Integral()
    print 'sample:',s,tot_yield
    UL.append(3./tot_yield*1e-7*0.5/81.)
    print 'UL(y):',UL[-1]

    
print mA
print mChi
print UL

graph = r.TGraph(len(mA),mChi,UL)

can = r.TCanvas('can','can',500,500)
can.SetLogx()
can.SetLogy()

graph.GetXaxis().SetRangeUser(.0002,1.)
graph.GetYaxis().SetRangeUser(1e-15,1e-5)
graph.GetXaxis().SetTitle('m_{#chi} [GeV]')
graph.GetYaxis().SetTitle('y=#epsilon^{2}#alpha_{D}(m_{#chi}/m_{A\'})^{4}')
graph.SetLineColor(4)
graph.SetMarkerColor(4)
graph.SetMarkerStyle(6)
graph.SetLineStyle(2)
graph.SetLineWidth(3)
graph.Draw('Ap')
print "Andrew's Limits: "
graph.Print()

target.graph.SetLineColor(1)
target.graph.SetLineStyle(1)
target.graph.SetLineWidth(3)
target.graph.Draw('c')

input_natalia = open('phase1_0.1X0.dat','r')
natalia_mass=array('f',[])
natalia_limit=array('f',[])
for line in input_natalia : 
    line = line[:-1]
    words = line.split(' ')
    while '' in words : 
        words.remove('')
    natalia_mass.append(float(words[0]))
    natalia_limit.append(float(words[1]))

natalia_graph = r.TGraph(len(natalia_mass),natalia_mass,natalia_limit)
natalia_graph.SetLineWidth(3)
natalia_graph.SetLineStyle(2)
natalia_graph.SetLineColor(2)
natalia_graph.SetMarkerColor(2)
natalia_graph.SetMarkerStyle(7)
natalia_graph.Draw('p')
print "Natalia's limits:",
natalia_graph.Print()

can.SaveAs('idealLimit.png')
