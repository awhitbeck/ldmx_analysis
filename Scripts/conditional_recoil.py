from sampleInfo import *
from test import *

def norm_vert(hist):

    num_bins_x = hist.GetNbinsX()
    num_bins_y = hist.GetNbinsY()

    for x in xrange(num_bins_x):
        running_sum=0.
        for y in xrange(num_bins_y):
            running_sum+=hist.GetBinContent(x+1,y+1)
        if running_sum>0. :
            for y in xrange(num_bins_y):
                hist.SetBinContent(x+1,y+1,hist.GetBinContent(x+1,y+1)/running_sum)

    return hist

r.gROOT.SetBatch(True)
r.gROOT.ProcessLine('.L ~/tdrstyle.C')
r.gROOT.ProcessLine('setTDRStyle()')

#plotVar1='sqrt(recoilTracker_simHit_recoil_px**2+recoilTracker_simHit_recoil_py**2)'
#plotVar2='sqrt(targetSP_recoil_px**2+targetSP_recoil_py**2)'

#plotVar1='recoilTracker_simHit_recoil_py'
#plotVar2='targetSP_recoil_py'
#binning='(200,-10,10,200,-10,10)'

plotVar1='recoilTracker_simHit_recoil_px-targetSP_recoil_px'
plotVar2='sqrt(targetSP_recoil_py**2+targetSP_recoil_px**2+targetSP_recoil_pz**2)'
binning='(200,0,100,200,-10,10)'

can = r.TCanvas('can','can',500,500)
can.SetLogz()
can.SetRightMargin(0.2)

input_file = {}
tree = {}
histo = {}
fs = ['0p001','0p01','0p1']
for f in fs :  
    input_file[f] = r.TFile(base_dir+files[f],'READ')
    tree[f] = input_file[f].Get('analysis_tree')
    tree[f].Draw(plotVar1+':'+plotVar2+'>>'+f+binning,'findable_tracks==1','colz')
    histo[f] = r.gDirectory.Get(f)
    norm_vert(histo[f])
    histo[f].GetXaxis().SetTitle('p at target')
    histo[f].GetYaxis().SetTitle('#delta p_{x} at first tracker layer')
    histo[f].Draw('colz')
    can.SaveAs('conditional_recoil_dpx_vs_p_m_A_'+f+'.png')

f='ecal_pn'
input_file[f] = r.TFile(base_dir+files[f],'READ')
tree[f] = input_file[f].Get('analysis_tree')
tree[f].Draw(plotVar1+':'+plotVar2+'>>'+f+binning,'findable_tracks==1','colz')
histo[f] = r.gDirectory.Get(f)
norm_vert(histo[f])
histo[f].GetXaxis().SetTitle('p at target')
histo[f].GetYaxis().SetTitle('#delta p_{x} at first tracker layer')
histo[f].Draw('colz')
can.SaveAs('conditional_recoil_dpx_vs_p_'+f+'.png')
