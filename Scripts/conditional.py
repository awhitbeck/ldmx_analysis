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

plotVar1='sqrt(recoilTracker_simHit_recoil_py**2+recoilTracker_simHit_recoil_px**2)'
#plotVar2='sqrt(targetSP_recoil_px**2+targetSP_recoil_py**2)'
plotVar2='max(max_back_hcal_pe,max_side_hcal_pe)'

can = r.TCanvas('can','can',500,500)
#can.SetLogz()
can.SetRightMargin(0.3)

input_file = {}
tree = {}
histo = {}
for f in files :
    print f
    input_file[f] = r.TFile(base_dir+files[f],'READ')
    tree[f] = input_file[f].Get('analysis_tree')
    tree[f].Draw(plotVar1+':'+plotVar2+'>>'+f+'(200,0,500,40,0,100)','findable_tracks==1','colz')
    histo[f] = r.gDirectory.Get(f)
    norm_vert(histo[f])
    histo[f].Draw('colz')
    can.SaveAs('conditional_'+f+'.png')
