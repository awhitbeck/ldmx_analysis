import ROOT as r
import sys

def plot_var(var_name,axis_label):

    r.gROOT.ProcessLine('.L ~/tdrstyle.C')
    r.gROOT.ProcessLine('setTDRStyle()')

    can = r.TCanvas('can','can',500,500)
    can.SetLogy()

    in_file = r.TFile('output_file.root','READ')
    histo={}
    histo['ecal_pn'] = in_file.Get(var_name+'_'+'ecal_pn_inc_ovrflw')
    histo['ecal_pn'].Scale(1./histo['ecal_pn'].Integral())
    histo['ecal_pn'].SetLineColor(3)
    histo['ecal_pn'].SetLineStyle(1)
    histo['ecal_pn'].SetLineWidth(2)
    histo['ecal_pn'].GetXaxis().SetTitle(axis_label)
    histo['ecal_pn'].GetYaxis().SetRangeUser(histo['ecal_pn'].GetMinimum(),2.)
    histo['ecal_pn'].DrawNormalized("hist")
    histo['0p01'] = in_file.Get(var_name+'_'+'0p01_inc_ovrflw')
    histo['0p01'].SetLineColor(2)
    histo['0p01'].SetLineStyle(1)
    histo['0p01'].SetLineWidth(2)
    histo['0p01'].DrawNormalized("hist,same")
    histo['0p001'] = in_file.Get(var_name+'_'+'0p001_inc_ovrflw')
    histo['0p001'].SetLineColor(2)
    histo['0p001'].SetLineStyle(2)
    histo['0p001'].SetLineWidth(2)
    histo['0p001'].DrawNormalized("hist,same")
    histo['0p1'] = in_file.Get(var_name+'_'+'0p1_inc_ovrflw')
    histo['0p1'].SetLineColor(6)
    histo['0p1'].SetLineStyle(1)
    histo['0p1'].SetLineWidth(2)
    histo['0p1'].DrawNormalized("hist,same")
    histo['1p0'] = in_file.Get(var_name+'_'+'1p0_inc_ovrflw')
    histo['1p0'].SetLineColor(6)
    histo['1p0'].SetLineStyle(2)
    histo['1p0'].SetLineWidth(2)
    histo['1p0'].DrawNormalized("hist,same")

    can.SaveAs(var_name+'_norm.png')

if __name__ == "__main__":
    plot_var(sys.argv[1],sys.argv[2])
