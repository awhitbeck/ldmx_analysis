import ROOT as r
from ldmx_container import *
import pandas as pd

r.gStyle.SetOptStat(0)
r.gROOT.ProcessLine(".L ~/tdrstyle.C")
r.gROOT.ProcessLine("setTDRStyle()")
import numpy as np
#import pandas as pd

r.gROOT.SetBatch(True)

def print_hits(electrons, hits):
    colored_print=["\033[91m{0}\033[00m",
                   "\033[92m{0}\033[00m",
                   "\033[94m{0}\033[00m",
                   "\033[95m{0}\033[00m",
                   "\033[96m{0}\033[00m",
                   "\033[97m{0}\033[00m",
                   "\033[93m{0}\033[00m",
                   "\033[101m{0}\033[00m",
                   "\033[104m{0}\033[00m",
                   "\033[105m{0}\033[00m"]

    output = map(str,hits)
    for electron in electrons:
        for i in electrons[electron]:
            output[i-2] = colored_print[0].format(output[i-2])
        colored_print.pop(0)

    print " ".join(output[::2])
    print " ".join(output[1::2])

def count_true(electrons):
    true_electrons=0
    for e in electrons:
        if len(electrons[e])>0:
            true_electrons+=1
    return true_electrons

coll="TriggerPadTaggerSimHits"
#coll="TriggerPadUpSimHits"
#coll="TriggerPadDownSimHits"

data=[]

cont = ldmx_container("~/nfs/test.root")
cont.setup()
hist = r.TH2F("confusion_hist",coll+";True Electrons;Pred Electrons",8,-0.5,7.5,8,-0.5,7.5)
second_hist = r.TH2F("secondCounts_hist",coll+";True-Pred Electrons;Num. Secondaries",9,-4.5,4.5,8,-0.5,7.5)
hist_true = r.TH1F("true_hist",coll+";True Electrons",8,-0.5,7.5)
hist_edep = r.TH1F("edep_hist",coll+";E_{dep}",100,0.,2.)
hist_pe = r.TH1F("pe_hist",coll+";PE",30,0.5,30.5)
for i in range(cont.tin.GetEntries()):
    cont.getEvent(i)
    #cont.dump("TrigScintScoringPlaneHits")
    #continue
    true_num = cont.num_beam_electrons()
    hit_energy = cont.trigger_pad_edep(coll)
    hit_pe = cont.trigger_pad_pe(coll)
    hit_energy_up = cont.trigger_pad_edep("TriggerPadUpSimHits")
    hit_pe_up = cont.trigger_pad_pe("TriggerPadUpSimHits")
    count_hits=reduce(lambda x,y:x+y,map(lambda x: int(x>=2),hit_pe))
    count_clusters=cont.count_clusters(coll)
    count_clusters_up=cont.count_clusters("TriggerPadUpSimHits")
    if true_num == 2 and count_clusters > 2 and cont.get_num_secondaries() == 0 : 
        #cont.dump_sim_particles() 
        gen_hits=cont.gen_hits(coll)
        gen_hits_up=cont.gen_hits("TriggerPadUpSimHits")
        true_num=count_true(gen_hits)
        print "- - - - - - - - - - event: ",i," - - - - - - - - - - - "
        if true_num == count_clusters and true_num != count_hits : 
            print "\033[96m - - - - - - - - - - (",true_num,":",count_hits,":",count_clusters,":",count_clusters_up,") - - - - - - - - - - - \033[00m"
        if true_num == count_clusters and true_num == count_hits : 
            print "\033[92m - - - - - - - - - - (",true_num,":",count_hits,":",count_clusters,":",count_clusters_up,") - - - - - - - - - - - \033[00m"
        if true_num != count_clusters and true_num != count_hits : 
            print "\033[91m - - - - - - - - - - (",true_num,":",count_hits,":",count_clusters,":",count_clusters_up,") - - - - - - - - - - - \033[00m"
            #cont.scan_trigger_pad_hits(coll)
        if true_num != count_clusters and true_num == count_hits : 
            print "\033[94m - - - - - - - - - - (",true_num,":",count_hits,":",count_clusters,":",count_clusters_up,") - - - - - - - - - - - \033[00m"
            #cont.scan_trigger_pad_hits(coll)
        print "tagger hits"
        print gen_hits
        print "photo-electrons:"
        print_hits(gen_hits,hit_pe)
        print "gen edep:"
        print_hits(gen_hits,hit_energy)

        print "up-stream hits"
        print gen_hits_up
        print "photo-electrons:"
        print_hits(gen_hits,hit_pe_up)
        print "gen edep:"
        print_hits(gen_hits,hit_energy_up)

        print "scoring plane hits:"
        cont.print_sp_hits()

    if true_num == 1 : 
        for edep in hit_energy:
            if edep != 0. : 
                hist_edep.Fill(edep)
        for pe in hit_pe : 
            if pe != 0 : 
                hist_pe.Fill(pe)
    #if cont.get_num_secondaries() == 0 : 
    hist.Fill(true_num,min(count_clusters,count_clusters_up))
    hist_true.Fill(true_num)
    second_hist.Fill(true_num-count_clusters,cont.get_num_secondaries())
    data.append([true_num,hit_pe])

for x in range(1,hist.GetNbinsX()+1):
    for y in range(1,hist.GetNbinsY()+1):
        if hist_true.GetBinContent(x) != 0 :
            hist.SetBinContent(x,y,hist.GetBinContent(x,y)/hist_true.GetBinContent(x))

can=r.TCanvas("can","can",500,500)
can.SetRightMargin(0.15)
hist.Draw("colz,text")

leg = r.TLegend(.2,.7,.5,.9,coll)
leg.SetBorderSize(0)
leg.Draw()
can.SaveAs("conf_matrix.png")

second_hist.Draw("colz")
can.SetLogz()
can.SaveAs("secondaries.png")

can_edep=r.TCanvas("can_edep","can_edep",500,500)
hist_edep.Draw()
leg.Draw()

can_true=r.TCanvas("can_true","can_true",500,500)
hist_true.Draw()
leg.Draw()

can_pe=r.TCanvas("can_pe","can_pe",500,500)
hist_pe.Draw()
leg.Draw()





df = pd.DataFrame(data,columns=['true_num','PEs'])

print df.head()
#df.to_pickle('data.pkl')
