from theoryUtils import *

r.gROOT.ProcessLine(".L ~/tdrstyle.C")
r.gROOT.ProcessLine("setTDRStyle()")

xsec = DMxsec()
can_xsec = r.TCanvas('can_xsec','can_xsec',500,500)
can_xsec.SetLogy()
can_xsec.SetLogx()
can_xsec.SetGridy()
can_xsec.SetGridx()
xsec.graph.SetMarkerStyle(8)
xsec.graph.SetLineWidth(3)
xsec.graph.GetYaxis().SetRangeUser(10,1e11)
xsec.graph.GetXaxis().SetTitle("m_{A'} [MeV]")
xsec.graph.GetYaxis().SetTitle("#sigma/#epsilon^{2} [pb]")
xsec.graph.Draw('Ac')

target = DMthermalTarget()
can_tar = r.TCanvas('can_tar','can_tar',500,500)
can_tar.SetLogy()
can_tar.SetLogx()
can_tar.SetGridy()
can_tar.SetGridx()
target.graph.SetMarkerStyle(8)
target.graph.SetLineWidth(3)
target.graph.GetXaxis().SetTitle("m_{#chi} [MeV]")
target.graph.GetYaxis().SetTitle("y=#epsilon^{2}#alpha_{D}(m_{#chi}/m_{A'})^{4}")
target.graph.GetYaxis().SetRangeUser(1e-17,1e-7)
target.graph.Draw('Ac')

print "test extrapolation:",target.graph.Eval(0.000333)

mchi=[0.001, 0.005, 0.01, 0.02, 0.04, 0.07, 0.1, 0.2, 0.4, 0.7, 1.0, 1.5]
#mchi=range(1,500)
#mchi = map(lambda x : x/1000.,mchi)
eps2_limit=[]
y_limit=[]
for m in mchi : 
    eps2_limit.append(2.4/(xsec.get_xsec(3.*m)*0.88))
    y_limit.append(2.4/(xsec.get_xsec(3.*m)*0.88)*target.alphaDark*target.mAp_over_mchi**4)

print zip(mchi,eps2_limit,y_limit)

limit = r.TGraph(len(mchi),array('f',mchi),array('f',y_limit))
limit.SetLineWidth(3)
limit.SetLineStyle(2)
limit.SetLineColor(2)
limit.SetMarkerStyle(8)
limit.SetMarkerColor(2)
limit.Draw("p")
