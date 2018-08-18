import ROOT as r 
r.gROOT.SetBatch(True)
from ldmx_container import *
import numpy as np
from array import array

r.gROOT.ProcessLine(".L ~/tdrstyle.C")
r.gROOT.ProcessLine("setTDRStyle()")

debug = False
generate_histos = False

sample_names=["bkg","sig_1000mev","sig_100mev","sig_10mev","sig_5mev"]
line_color=[1,2,3,4,6]
leg_label=["trgt PN","mA'=1 GeV","mA'=100 MeV","mA'=10MeV","mA'=5 MeV"]

s = {"bkg":ldmx_container("/nfs/slac/g/ldmx/users/whitbeck/dos_electrones/root_files/bkup/2ele_PN_target_biased_all.root"),
     "sig_1000mev":ldmx_container("/nfs/slac/g/ldmx/data/mc/v9-magnet/2e_signal/4pt0_gev_signal_ap_mass_1000mev.root"),
     "sig_100mev":ldmx_container("/nfs/slac/g/ldmx/data/mc/v9-magnet/2e_signal/4pt0_gev_signal_ap_mass_100mev.root"),
     "sig_10mev":ldmx_container("/nfs/slac/g/ldmx/data/mc/v9-magnet/2e_signal/4pt0_gev_signal_ap_mass_10mev.root"),
     "sig_5mev":ldmx_container("/nfs/slac/g/ldmx/data/mc/v9-magnet/2e_signal/4pt0_gev_signal_ap_mass_5mev.root")}

histos = {}
trees = {}
tree_bank = {}

if generate_histos : 
    for sample_name in s : 
        print 'sample:',sample_name
        s[sample_name].setup()
        totEvents = s[sample_name].tin.GetEntries()
        
        histos[sample_name]={}
        trees[sample_name] = r.TTree(sample_name+"_tree",sample_name+"_tree")
        tree_bank[sample_name] = {}

        for i in xrange(totEvents):
            s[sample_name].getEvent(i)
            if i % 1000 == 0 : print i,"/",totEvents
            eles = s[sample_name].get_recoil_electrons_hcalSP_hits()
            eles = filter(lambda x : x!=None,eles)
            if len(eles) != 2 : continue
            if sqrt(sum(map(lambda x : x**2,eles[1].getMomentum()))) > sqrt(sum(map(lambda x : x**2,eles[0].getMomentum()))) :
                eles[0],eles[1] = eles[1],eles[0]
            if sqrt(sum(map(lambda x : x**2,eles[1].getMomentum()))) > 2500. : break 

            if not 'ele0_px' in histos[sample_name] : 
                histos[sample_name]['ele0_px'] = r.TH1F("ele0_px_"+sample_name,";ele0_px;Events",200,0,50)
                histos[sample_name]['ele0_px'].Fill(eles[0].getMomentum()[0])
                tree_bank[sample_name]['ele_px'] = array('f',[0.]*2)
                trees[sample_name].Branch('ele0_px',tree_bank[sample_name]['ele_px'],"ele_px[2]/F")
                tree_bank[sample_name]['ele_px'][0] = eles[0].getMomentum()[0]
                tree_bank[sample_name]['ele_px'][1] = eles[1].getMomentum()[0]
                
                histos[sample_name]['ele0_py'] = r.TH1F("ele0_py_"+sample_name,";ele0_py;Events",200,0,50)
                histos[sample_name]['ele0_py'].Fill(eles[0].getMomentum()[1])
                tree_bank[sample_name]['ele_py'] = array('f',[0.]*2)
                trees[sample_name].Branch('ele0_py',tree_bank[sample_name]['ele_py'],"ele_py[2]/F")
                tree_bank[sample_name]['ele_py'][0] = eles[0].getMomentum()[1]
                tree_bank[sample_name]['ele_py'][1] = eles[1].getMomentum()[1]
                
                histos[sample_name]['ele0_pz'] = r.TH1F("ele0_pz_"+sample_name,";ele0_pz;Events",200,0,50)
                histos[sample_name]['ele0_pz'].Fill(eles[0].getMomentum()[2])
                tree_bank[sample_name]['ele_pz'] = array('f',[0.]*2)
                trees[sample_name].Branch('ele0_pz',tree_bank[sample_name]['ele_pz'],"ele_pz[2]/F")
                tree_bank[sample_name]['ele_pz'][0] = eles[0].getMomentum()[2]
                tree_bank[sample_name]['ele_pz'][1] = eles[1].getMomentum()[2]
                
                histos[sample_name]['ele0_x'] = r.TH1F("ele0_x_"+sample_name,";ele0_x;Events",200,0,50)
                histos[sample_name]['ele0_x'].Fill(eles[0].getPosition()[0])
                tree_bank[sample_name]['ele_x'] = array('f',[0.]*2)
                trees[sample_name].Branch('ele0_x',tree_bank[sample_name]['ele_x'],"ele_x[2]/F")
                tree_bank[sample_name]['ele_x'][0] = eles[0].getPosition()[0]
                tree_bank[sample_name]['ele_x'][1] = eles[1].getPosition()[0]

                histos[sample_name]['ele0_y'] = r.TH1F("ele0_y_"+sample_name,";ele0_y;Events",200,0,50)
                histos[sample_name]['ele0_y'].Fill(eles[0].getPosition()[1])
                tree_bank[sample_name]['ele_y'] = array('f',[0.]*2)
                trees[sample_name].Branch('ele0_y',tree_bank[sample_name]['ele_y'],"ele_y[2]/F")
                tree_bank[sample_name]['ele_y'][0] = eles[0].getPosition()[1]
                tree_bank[sample_name]['ele_y'][1] = eles[1].getPosition()[1]

                histos[sample_name]['ele0_z'] = r.TH1F("ele0_z_"+sample_name,";ele0_z;Events",200,0,50)
                histos[sample_name]['ele0_z'].Fill(eles[0].getPosition()[2])
                tree_bank[sample_name]['ele_z'] = array('f',[0.]*2)
                trees[sample_name].Branch('ele0_z',tree_bank[sample_name]['ele_z'],"ele_z[2]/F")
                tree_bank[sample_name]['ele_z'][0] = eles[0].getPosition()[2]
                tree_bank[sample_name]['ele_z'][1] = eles[1].getPosition()[2]
            else :
                histos[sample_name]['ele0_px'].Fill(eles[0].getMomentum()[0])
                tree_bank[sample_name]['ele_px'][0] = eles[0].getMomentum()[0]
                tree_bank[sample_name]['ele_px'][1] = eles[1].getMomentum()[0]

                histos[sample_name]['ele0_py'].Fill(eles[0].getMomentum()[1])
                tree_bank[sample_name]['ele_py'][0] = eles[0].getMomentum()[1]
                tree_bank[sample_name]['ele_py'][1] = eles[1].getMomentum()[1]

                histos[sample_name]['ele0_pz'].Fill(eles[0].getMomentum()[2])
                tree_bank[sample_name]['ele_pz'][0] = eles[0].getMomentum()[2]
                tree_bank[sample_name]['ele_pz'][1] = eles[1].getMomentum()[2]

                histos[sample_name]['ele0_x'].Fill(eles[0].getPosition()[0])
                tree_bank[sample_name]['ele_x'][0] = eles[0].getPosition()[0]
                tree_bank[sample_name]['ele_x'][1] = eles[1].getPosition()[0]

                histos[sample_name]['ele0_y'].Fill(eles[0].getPosition()[1])
                tree_bank[sample_name]['ele_y'][0] = eles[0].getPosition()[1]
                tree_bank[sample_name]['ele_y'][1] = eles[1].getPosition()[1]

                histos[sample_name]['ele0_z'].Fill(eles[0].getPosition()[2])
                tree_bank[sample_name]['ele_z'][0] = eles[0].getPosition()[2]
                tree_bank[sample_name]['ele_z'][1] = eles[1].getPosition()[2]

            for iele,ele in enumerate(eles):
                shower_vars = s[sample_name].shower_vars(ele)
                for var in shower_vars : 
                    temp_var = var+"_ele_"+str(iele)
                    if not temp_var in histos[sample_name] : 
                        histos[sample_name][temp_var] = r.TH1F(temp_var+"_"+sample_name,";"+temp_var+";Events",200,0,50)
                        histos[sample_name][temp_var].Fill(shower_vars[var])
                        tree_bank[sample_name][temp_var] = array('f',[0.])
                        trees[sample_name].Branch(temp_var,tree_bank[sample_name][temp_var],temp_var+"/F")
                        tree_bank[sample_name][temp_var][0] = shower_vars[var]
                    else :
                        histos[sample_name][temp_var].Fill(shower_vars[var])
                        tree_bank[sample_name][temp_var][0] = shower_vars[var]
            trees[sample_name].Fill()

outputFile = r.TFile("nelsonVar_histos.root","RECREATE" if generate_histos else "READ")

if generate_histos : 
    for sample in sample_names :
        trees[sample].Write()
else : 
    obj_list = outputFile.GetListOfKeys()
    obj_iter = r.TIter(obj_list)
    key = obj_iter.Next()  
    while key : 
        obj = key.ReadObj()
        if obj.InheritsFrom("TH1") :
            name = obj.GetName()
            if 'bkg' in name :
                sample = 'bkg'
                hist_name = '_'.join(name.split('_')[:-1])
            if 'sig' in name : 
                sample = '_'.join(name.split('_')[-2:])
                hist_name = '_'.join(name.split('_')[:-2])
            print "---",sample
            print " - ",hist_name
            if sample in histos : 
                histos[sample][hist_name]=outputFile.Get(name)
            else : 
                histos[sample]={}
                histos[sample][hist_name]=outputFile.Get(name)
                
        key = obj_iter.Next()

can = r.TCanvas("can","can",500,500)
for h in histos["bkg"] : 
    leg = r.TLegend(.6,.6,.9,.9)
    leg.SetBorderSize(0)
    leg.SetFillColor(0)
    for isample,sample in enumerate(sample_names) : 
        if 'sig_100mev' in sample or 'sig_10mev' in sample or 'sig_5mev' in sample : continue
        histos[sample][h].SetLineColor(line_color[isample])
        histos[sample][h].SetLineWidth(2)
        leg.AddEntry(histos[sample][h],leg_label[isample],"l")
        if histos[sample][h].Integral()>0 :
            histos[sample][h].Scale(1./histos[sample][h].Integral())
        if isample == 0 :
            histos[sample][h].Draw()
        else : 
            histos[sample][h].Draw("SAME")
        if generate_histos : 
            histos[sample][h].Write()
    leg.Draw()
    can.SaveAs(h+".png")

outputFile.Close()
    
