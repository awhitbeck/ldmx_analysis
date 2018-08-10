import ROOT as r
r.gROOT.SetBatch(True)
from ldmx_container import *
import numpy as np

r.gROOT.ProcessLine(".L ~/tdrstyle.C")
r.gROOT.ProcessLine("setTDRStyle()")

debug = False

s = ldmx_container("/nfs/slac/g/ldmx/users/whitbeck/shower_shape/root_files/electrons_4.0_gev_all.root")
s.setup()
totEvents = s.tin.GetEntries()

# - - - - - - 
# histograms
# - - - - - - 
showerProfile_layer = []
showerProfile_layer_rawPos = []
showerProfile_2d = []

for i in xrange(33) :
    showerProfile_layer.append( r.TH1F("shower_profile_layer"+str(i),";r [mm];Hits*E_{dep} [MeV]",99,-98.149,98.149) )
    showerProfile_layer_rawPos.append( r.TH2F("shower_profile_rawPos_layer"+str(i),";r [mm];Hits*E_{dep} [MeV]",200,-40,40,200,-40,40) )
    showerProfile_2d.append( r.TH2F("showerProfile_2d_layer"+str(i),";x;y;E",200,-40,40,200,-40,40) )

for ievt in xrange(totEvents):
    s.getEvent(ievt)
    
    beam_eles = s.get_beam_electrons()
    recoil_eles = s.get_recoil_electrons_hcalSP_hits()
    recoil_ele_pos = [recoil_eles[0].getPosition()[0],recoil_eles[0].getPosition()[1],recoil_eles[0].getPosition()[2]]
    recoil_ele_mom = [recoil_eles[0].getMomentum()[0],recoil_eles[0].getMomentum()[1],recoil_eles[0].getMomentum()[2]]
    
    if debug : 
        for e in beam_eles:
            e.Print()
        print recoil_eles
        print "recoil electron positions:",zip(recoil_eles_x,recoil_eles_y,recoil_eles_z)

    for h in s.ecalSimHits:
        layer=s.compute_layer(h.getID()) 
        if layer < 0 or layer >= 33 : continue
        pos = h.getPosition()
        ray_x_pos = recoil_ele_pos[0]+recoil_ele_mom[0]/recoil_ele_mom[2]*(pos[2]-recoil_ele_pos[2])
        ray_y_pos = recoil_ele_pos[1]+recoil_ele_mom[1]/recoil_ele_mom[2]*(pos[2]-recoil_ele_pos[2])
        rel_pos = [pos[0]-ray_x_pos,pos[1]-ray_y_pos,0.]
        #signed_r = rel_pos[0]/abs(rel_pos[0])*sqrt(rel_pos[0]**2+rel_pos[1]**2)
        signed_r = sqrt(rel_pos[0]**2+rel_pos[1]**2)
        if( debug ) :
            print "position:"," ".join(map(str,pos))
            print "relative position:"," ".join(map(str,rel_pos))
            print "signed_r:",signed_r
        if abs(pos[1])<2. : 
            showerProfile_layer[layer].Fill(rel_pos[0],h.getEdep())
        showerProfile_layer_rawPos[layer].Fill(pos[0],pos[1],h.getEdep())
        showerProfile_2d[layer].Fill(rel_pos[0],rel_pos[1],h.getEdep())    

    if debug : 
        break

can = r.TCanvas("can","can",500,500)
can.SetRightMargin(0.2)
outputFile = r.TFile("showerShape_histos.root","RECREATE")

running_sum = 0.

for i in xrange(33):
    if not debug : 

        can.SetLogy(False)

        showerProfile_2d[i].Scale(62./9.7/totEvents)
        showerProfile_2d[i].Write()
        showerProfile_2d[i].Draw("colz")
        can.SaveAs(showerProfile_2d[i].GetName()+".png")

        can.SetLogz(True)
        showerProfile_layer_rawPos[i].Draw("colz")
        can.SaveAs(showerProfile_2d[i].GetName()+"_LogZ.png")
        can.SetLogz(False)

        showerProfile_layer_rawPos[i].Scale(62./9.7/totEvents)
        showerProfile_layer_rawPos[i].Write()
        can.SaveAs(showerProfile_layer_rawPos[i].GetName()+".png")

        can.SetLogz(True)        
        can.SaveAs(showerProfile_layer_rawPos[i].GetName()+"_LogZ.png")
        can.SetLogz(False)

        running_sum+=62./9.7*showerProfile_layer[i].Integral()
        print "integral",62./9.7*showerProfile_layer[i].Integral()
        print "totEvents",totEvents

        showerProfile_layer[i].Scale(62./9.7/totEvents)
        showerProfile_layer[i].GetYaxis().SetRangeUser(0.01,showerProfile_layer[i].GetMaximum()*1.5)

        can.SetLogz(False)
        showerProfile_layer[i].Draw()
        can.SaveAs(showerProfile_layer[i].GetName()+".png")
        showerProfile_layer[i].Write()

        can.SetLogy(True)
        showerProfile_layer[i].GetYaxis().SetRangeUser(0.01,showerProfile_layer[i].GetMaximum()*10)
        showerProfile_layer[i].Draw()
        can.SaveAs(showerProfile_layer[i].GetName()+"_LogY.png")
        showerProfile_layer[i].Write()

print "total_edep",running_sum

outputFile.Close()
