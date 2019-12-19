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

## set configurable parameters
debug=True
coll="TriggerPadTaggerSimHits" #other options: "TriggerPadUpSimHits", "TriggerPadDownSimHits"
min_pe=3

## intialize contain to read target input file
cont = ldmx_container("~whitbeck/raid/LDMX/trigger_pad_sim/test.root")
cont.setup()

## initialize histograms
hist = r.TH2F("confusion_hist",coll+";True Electrons;Pred Electrons",8,-0.5,7.5,8,-0.5,7.5)
second_hist = r.TH2F("secondCounts_hist",coll+";True-Pred Electrons;Num. Secondaries",9,-4.5,4.5,8,-0.5,7.5)
hist_true = r.TH1F("true_hist",coll+";True Electrons",8,-0.5,7.5)

for i in range(cont.tin.GetEntries()):

    ## initialize container
    cont.getEvent(i)

    ## get true number of electrons
    true_num=cont.count_true(coll)

    #### ALGORITHM 1: COUNT THE NUMBER HITS IN AN ARRAY
    count_hits=cont.count_hits(coll,min_pe)
    count_hits_up=cont.count_hits("TriggerPadUpSimHits",min_pe)
    #### ALGORITHM 2: COUNT THE NUMBER OF HIT CLUSTERS
    count_clusters=cont.count_clusters(coll,min_pe)
    count_clusters_up=cont.count_clusters("TriggerPadUpSimHits",min_pe)

    #### DEBUGGING INFORMATION --- 
    if debug and true_num == 1 and count_hits == 0 : # and cont.get_num_secondaries() == 0 : 

        hit_energy = cont.trigger_pad_edep(coll)
        hit_pe = cont.trigger_pad_pe(coll)
        hit_energy_up = cont.trigger_pad_edep("TriggerPadUpSimHits")
        hit_pe_up = cont.trigger_pad_pe("TriggerPadUpSimHits")

        print "- - - - - - - - - - event: ",i," - - - - - - - - - - - "
        if true_num == count_clusters and true_num != count_hits : 
            print "\033[96m - - - - - - - - - - (",true_num,":",count_hits,":",count_clusters,":",count_clusters_up,") - - - - - - - - - - - \033[00m"
        if true_num == count_clusters and true_num == count_hits : 
            print "\033[92m - - - - - - - - - - (",true_num,":",count_hits,":",count_clusters,":",count_clusters_up,") - - - - - - - - - - - \033[00m"
        if true_num != count_clusters and true_num != count_hits : 
            print "\033[91m - - - - - - - - - - (",true_num,":",count_hits,":",count_clusters,":",count_clusters_up,") - - - - - - - - - - - \033[00m"
        if true_num != count_clusters and true_num == count_hits : 
            print "\033[94m - - - - - - - - - - (",true_num,":",count_hits,":",count_clusters,":",count_clusters_up,") - - - - - - - - - - - \033[00m"

        gen_hits=cont.gen_hits(coll)
        #print "tagger hits"
        #print gen_hits
        print "photo-electrons:"
        print_hits(gen_hits,hit_pe)
        #print "gen edep:"
        #print_hits(gen_hits,hit_energy)

        # print "up-stream hits"
        # print gen_hits_up
        # print "photo-electrons:"
        # print_hits(gen_hits,hit_pe_up)
        # print "gen edep:"
        # print_hits(gen_hits,hit_energy_up)

        print "scoring plane hits:"
        cont.print_sp_hits()

    ## fill histograms
    #hist.Fill(true_num,count_clusters) #alternative min(count_clusters,count_clusters_up))
    hist.Fill(true_num,count_hits) #alternative min(count_clusters,count_clusters_up))
    hist_true.Fill(true_num)
    second_hist.Fill(true_num-count_clusters,cont.get_num_secondaries())

## normalize each num_true electrons column to same area
for x in range(1,hist.GetNbinsX()+1):
    for y in range(1,hist.GetNbinsY()+1):
        if hist_true.GetBinContent(x) != 0 :
            hist.SetBinContent(x,y,hist.GetBinContent(x,y)/hist_true.GetBinContent(x))

## plot histograms
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
