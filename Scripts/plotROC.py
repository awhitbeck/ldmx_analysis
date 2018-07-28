import ROOT as r
from sampleInfo import *
from array import array

def make_roc(sig,bkg):

    sig_int = sig.Integral(0,sig.GetNbinsX()+2)
    bkg_int = bkg.Integral(0,bkg.GetNbinsX()+2)
    sig_eff=array('f',[])
    bkg_eff=array('f',[])

    for i in xrange(sig.GetNbinsX()+2):
        sig_eff.append(sig.Integral(0,i)/sig_int)
        bkg_eff.append(bkg.Integral(0,i)/bkg_int)

    return r.TGraph(len(sig_eff),sig_eff,bkg_eff)

def make_demi_roc(sig,bkg):

    sig_int = sig.Integral(0,sig.GetNbinsX()+2)
    sig_eff=array('f',[])
    bkg_eff=array('f',[])

    for i in xrange(sig.GetNbinsX()+2):
        sig_eff.append(sig.Integral(0,i)/sig_int)
        bkg_eff.append(bkg.Integral(0,i))

    return r.TGraph(len(sig_eff),sig_eff,bkg_eff)


histo_file=r.TFile('output_file.root','READ')
back_pe_histos={}
back_pe_totalBkg=None
side_pe_histos={}
side_pe_totalBkg=None
hcal_veto_histos={}
hcal_veto_totalBkg=None
for s in files : 
    back_pe_histos[s]=histo_file.Get('back_pe_histo_'+s+'_inc_ovrflw')
    side_pe_histos[s]=histo_file.Get('side_pe_histo_'+s+'_inc_ovrflw')
    hcal_veto_histos[s]=histo_file.Get('hcal_veto_histo_'+s+'_inc_ovrflw')
    if back_pe_totalBkg == None and is_bkg[s]: 
        back_pe_totalBkg=back_pe_histos[s]
    elif is_bkg[s] :
        back_pe_totalBkg.Add(back_pe_histos[s])

    if side_pe_totalBkg == None and is_bkg[s]: 
        side_pe_totalBkg=side_pe_histos[s]
    elif is_bkg[s] :
        side_pe_totalBkg.Add(side_pe_histos[s])

    if hcal_veto_totalBkg == None and is_bkg[s]: 
        hcal_veto_totalBkg=hcal_veto_histos[s]
    elif is_bkg[s] :
        hcal_veto_totalBkg.Add(hcal_veto_histos[s])

can = r.TCanvas('can','can',500,500)

#totalBkg.SetFillColor(4)
#totalBkg.Draw('histo')
#histos['ecal_pn'].Draw()
#histos['0p1'].Draw("histo,SAME")

back_pe_roc = make_demi_roc(back_pe_histos['0p1'],back_pe_totalBkg)
back_pe_roc.SetMarkerStyle(8)
back_pe_roc.SetMarkerColor(2)

side_pe_roc = make_demi_roc(side_pe_histos['0p1'],side_pe_totalBkg)
side_pe_roc.SetMarkerStyle(8)
side_pe_roc.SetMarkerColor(6)

hcal_veto_roc = make_demi_roc(hcal_veto_histos['0p1'],hcal_veto_totalBkg)
hcal_veto_roc.SetMarkerStyle(8)
hcal_veto_roc.SetMarkerColor(4)

leg = r.TLegend(.2,.6,.4,.9)
leg.SetBorderSize(0)
leg.SetFillColor(0)
leg.AddEntry(back_pe_roc,'Sum PE (back)','p')
leg.AddEntry(side_pe_roc,'Sum PE (side)','p')
leg.AddEntry(hcal_veto_roc,'Max PE','p')

back_pe_roc.Draw("Ap")
side_pe_roc.Draw("p")
hcal_veto_roc.Draw("p")

leg.Draw()
