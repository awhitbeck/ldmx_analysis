import ROOT as r
from math import sqrt
from sampleInfo import *

def include_overflow(histo):
    temp=r.TH1F(histo.GetName()+"_inc_ovrflw",histo.GetTitle(),histo.GetNbinsX()+1,histo.GetBinLowEdge(1),histo.GetBinLowEdge(histo.GetNbinsX())+4*histo.GetBinWidth(histo.GetNbinsX()))
    for i in xrange(1,histo.GetNbinsX()+2):
        temp.SetBinContent(i,histo.GetBinContent(i))
        temp.SetBinError(i,histo.GetBinError(i))
    return temp

r.gROOT.ProcessLine(".L ~/tdrstyle.C")
r.gROOT.ProcessLine("setTDRStyle()")
r.gROOT.SetBatch(True)

trees={}
histos={}
back_pe_histos={}
side_pe_histos={}
hcal_veto_histos={}
sum_back_pe_histos={}
sum_side_pe_histos={}
sum_hcal_pe_histos={}
for s in files : 
    print s
    trees[s] = r.TChain('analysis_tree')
    trees[s].Add(base_dir+files[s])
    print "total events:",trees[s].GetEntries()
    histos[s] = r.TH1F('histo_'+s,';recoil p_{T};Events',100,0,50)
    histos[s].Sumw2()
    back_pe_histos[s] = r.TH1F('back_pe_histo_'+s,';max PE;Events',51,-0.5,50.5)
    back_pe_histos[s].Sumw2()
    side_pe_histos[s] = r.TH1F('side_pe_histo_'+s,';max PE;Events',51,-0.5,50.5)
    side_pe_histos[s].Sumw2()
    hcal_veto_histos[s] = r.TH1F('hcal_veto_histo_'+s,';max PE;Events',51,-0.5,50.5)
    hcal_veto_histos[s].Sumw2()
    sum_back_pe_histos[s] = r.TH1F('sum_back_pe_histo_'+s,';sum PE;Events',51,-0.5,50.5)
    sum_back_pe_histos[s].Sumw2()
    sum_side_pe_histos[s] = r.TH1F('sum_side_pe_histo_'+s,';sum PE;Events',51,-0.5,50.5)
    sum_side_pe_histos[s].Sumw2()
    sum_hcal_pe_histos[s] = r.TH1F('sum_hcal_pe_histo_'+s,';sum PE;Events',51,-0.5,50.5)
    sum_hcal_pe_histos[s].Sumw2()
    for i in xrange(trees[s].GetEntries()):
        #if i >= 1000 : break 
        if not i % 100000 : print i
        trees[s].GetEntry(i)
        bdt=getattr(trees[s],'EcalVeto_BDT')
        #if bdt < 0.94 : continue
        tracks=getattr(trees[s],'findable_tracks')
        if tracks!=1 : continue
        back_hcal_veto=getattr(trees[s],'max_back_hcal_pe')
        side_hcal_veto=getattr(trees[s],'max_side_hcal_pe')
        sum_back_hcal=getattr(trees[s],'sum_back_hcal_pe')
        sum_side_hcal=getattr(trees[s],'sum_side_hcal_pe')
        #if back_hcal_veto > 8 or side_hcal_veto > 8 : continue
        trigger_energy_sum=getattr(trees[s],'trigger_energy_sum')
        if trigger_energy_sum > 1500.: continue 
        pn_weight=getattr(trees[s],'PN_weight')
        px=getattr(trees[s],'targetSP_recoil_px')
        py=getattr(trees[s],'targetSP_recoil_py')
        histos[s].Fill(sqrt(px**2+py**2),pn_weight*xsec_weight[s])
        back_pe_histos[s].Fill(back_hcal_veto,pn_weight*xsec_weight[s])
        side_pe_histos[s].Fill(side_hcal_veto,pn_weight*xsec_weight[s])
        hcal_veto_histos[s].Fill(max(side_hcal_veto,back_hcal_veto),pn_weight*xsec_weight[s])
        sum_back_pe_histos[s].Fill(sum_back_hcal,pn_weight*xsec_weight[s])
        sum_side_pe_histos[s].Fill(sum_side_hcal,pn_weight*xsec_weight[s])
        sum_hcal_pe_histos[s].Fill(sum_side_hcal+sum_back_hcal,pn_weight*xsec_weight[s])

    histos[s] = include_overflow(histos[s])
    back_pe_histos[s] = include_overflow(back_pe_histos[s])
    side_pe_histos[s] = include_overflow(side_pe_histos[s])
    hcal_veto_histos[s] = include_overflow(hcal_veto_histos[s])
    sum_back_pe_histos[s] = include_overflow(sum_back_pe_histos[s])
    sum_side_pe_histos[s] = include_overflow(sum_side_pe_histos[s])
    sum_hcal_pe_histos[s] = include_overflow(sum_hcal_pe_histos[s])

    back_pe_histos[s].SetLineColor(line_colors[s])
    back_pe_histos[s].SetLineStyle(line_styles[s])
    back_pe_histos[s].SetLineWidth(line_widths[s])
    side_pe_histos[s].SetLineColor(line_colors[s])
    side_pe_histos[s].SetLineStyle(line_styles[s])
    side_pe_histos[s].SetLineWidth(line_widths[s])
    hcal_veto_histos[s].SetLineColor(line_colors[s])
    hcal_veto_histos[s].SetLineStyle(line_styles[s])
    hcal_veto_histos[s].SetLineWidth(line_widths[s])
    sum_back_pe_histos[s].SetLineColor(line_colors[s])
    sum_back_pe_histos[s].SetLineStyle(line_styles[s])
    sum_back_pe_histos[s].SetLineWidth(line_widths[s])
    sum_side_pe_histos[s].SetLineColor(line_colors[s])
    sum_side_pe_histos[s].SetLineStyle(line_styles[s])
    sum_side_pe_histos[s].SetLineWidth(line_widths[s])
    sum_hcal_pe_histos[s].SetLineColor(line_colors[s])
    sum_hcal_pe_histos[s].SetLineStyle(line_styles[s])
    sum_hcal_pe_histos[s].SetLineWidth(line_widths[s])
    histos[s].SetLineColor(line_colors[s])
    histos[s].SetLineStyle(line_styles[s])
    histos[s].SetLineWidth(line_widths[s])

leg = r.TLegend(.2,.75,.9,.9)
leg.SetFillColor(0)
leg.SetNColumns(6)

can = r.TCanvas('can','can',500,500)    
can.SetLogy()

#tag='_hcal_pe_8'
tag=''

first=True
for s in histos:
    leg.AddEntry(histos[s],s,'l')
    if first : 
        histos[s].Draw('histo')
        first = False
    else :
        histos[s].Draw('histo,SAME')
leg.Draw()
can.SaveAs('recoil_pt_xsec_norm'+tag+'.png')

first=True
for s in back_pe_histos:     
    if first :
        back_pe_histos[s].Draw('histo')
        first = False
    else :
        back_pe_histos[s].Draw('histo,SAME')
leg.Draw()
can.SaveAs('back_hcal_max_pe_xsec_norm'+tag+'.png')

first=True
for s in side_pe_histos:
    if first :
        side_pe_histos[s].Draw('histo')
        first = False
    else :
        side_pe_histos[s].Draw('histo,SAME')
leg.Draw()
can.SaveAs('side_hcal_max_pe_xsec_norm'+tag+'.png')

first=True
for s in hcal_veto_histos:
    if first :
        hcal_veto_histos[s].Draw('histo')
        first = False
    else :
        hcal_veto_histos[s].Draw('histo,SAME')
leg.Draw()
can.SaveAs('hcal_max_pe_xsec_norm'+tag+'.png')

first=True
for s in sum_back_pe_histos:     
    if first :
        sum_back_pe_histos[s].Draw('histo')
        first = False
    else :
        sum_back_pe_histos[s].Draw('histo,SAME')
leg.Draw()
can.SaveAs('back_hcal_sum_pe_xsec_norm'+tag+'.png')

first=True
for s in sum_side_pe_histos:
    if first :
        sum_side_pe_histos[s].Draw('histo')
        first = False
    else :
        sum_side_pe_histos[s].Draw('histo,SAME')
leg.Draw()
can.SaveAs('side_hcal_sum_pe_xsec_norm'+tag+'.png')

first=True
for s in sum_hcal_pe_histos:
    if first :
        sum_hcal_pe_histos[s].Draw('histo')
        first = False
    else :
        sum_hcal_pe_histos[s].Draw('histo,SAME')
leg.Draw()
can.SaveAs('hcal_sum_pe_xsec_norm'+tag+'.png')

# - - - - - - - - - - - - - - 

output_file = r.TFile('output_file'+tag+'.root','RECREATE')
for s in histos:
    histos[s].Write()
    back_pe_histos[s].Write()
    side_pe_histos[s].Write()
    hcal_veto_histos[s].Write()
output_file.Close()

# - - - - - - - - - - - - - - 

first=True
for s in histos:
    histos[s].Scale(1./histos[s].Integral())
    if first : 
        histos[s].Draw('histo')
        first = False
    else :
        histos[s].Draw('histo,SAME')
leg.Draw()
can.SaveAs('recoil_pt'+tag+'.png')

first=True
for s in back_pe_histos:     
    back_pe_histos[s].Scale(1./back_pe_histos[s].Integral())
    if first :
        back_pe_histos[s].Draw('histo')
        first = False
    else :
        back_pe_histos[s].Draw('histo,SAME')
leg.Draw()
can.SaveAs('back_hcal_max_pe'+tag+'.png')

first=True
for s in side_pe_histos:
    side_pe_histos[s].Scale(1./side_pe_histos[s].Integral())
    if first :
        side_pe_histos[s].Draw('histo')
        first = False
    else :
        side_pe_histos[s].Draw('histo,SAME')
leg.Draw()
can.SaveAs('side_hcal_max_pe'+tag+'.png')

first=True
for s in hcal_veto_histos:
    hcal_veto_histos[s].Scale(1./hcal_veto_histos[s].Integral())
    if first :
        hcal_veto_histos[s].Draw('histo')
        first = False
    else :
        hcal_veto_histos[s].Draw('histo,SAME')
leg.Draw()
can.SaveAs('hcal_max_pe'+tag+'.png')

first=True
for s in sum_back_pe_histos:     
    sum_back_pe_histos[s].Scale(1./sum_back_pe_histos[s].Integral())
    if first :
        sum_back_pe_histos[s].Draw('histo')
        first = False
    else :
        sum_back_pe_histos[s].Draw('histo,SAME')
leg.Draw()
can.SaveAs('back_hcal_sum_pe'+tag+'.png')

first=True
for s in sum_side_pe_histos:
    sum_side_pe_histos[s].Scale(1./sum_side_pe_histos[s].Integral())
    if first :
        sum_side_pe_histos[s].Draw('histo')
        first = False
    else :
        sum_side_pe_histos[s].Draw('histo,SAME')
leg.Draw()
can.SaveAs('side_hcal_sum_pe'+tag+'.png')

first=True
for s in sum_hcal_pe_histos:
    sum_hcal_pe_histos[s].Scale(1./sum_hcal_pe_histos[s].Integral())
    if first :
        sum_hcal_pe_histos[s].Draw('histo')
        first = False
    else :
        sum_hcal_pe_histos[s].Draw('histo,SAME')
leg.Draw()
can.SaveAs('hcal_sum_pe'+tag+'.png')

