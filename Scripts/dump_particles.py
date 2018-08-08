from ROOT import *
from ldmx_container import *
from numpy import arctan

r.gROOT.ProcessLine(".L ~/tdrstyle.C")
r.gROOT.ProcessLine("setTDRStyle()")

tag="target"
s = ldmx_container("/nfs/slac/g/ldmx/users/whitbeck/dos_electrones/root_files/2ele_PN_"+tag+"_biased_*.root")
s.setup()
totEvents = s.tin.GetEntries()

h_energy = r.TH2F("energy",";E_{#gamma,1} [MeV];E_{#gamma,2} [MeV]",20,0,4000,20,0,4000)
h_energy.GetXaxis().SetNdivisions(505)
h_isPN = r.TH2F("isPN",";isPN #gamma_{1} [MeV];isPN #gamma_{2} [MeV]",2,-0.5,1.5,2,-0.5,1.5)
h_isPN.GetXaxis().SetNdivisions(502)
h_isPN.GetYaxis().SetNdivisions(502)

h_vertex1 = r.TH2F("vertex1",";x [mm];y [mm]",100,-10,10,100,-20,20)
h_vertex2 = r.TH2F("vertex2",";x [mm];y [mm]",100,-10,10,100,-20,20)
h_z1 = r.TH1F("z1",";z [mm]",100,-2,2)
h_z2 = r.TH1F("z2",";z [mm]",100,-2,2)
h_dr_vs_ele1_mom = r.TH2F("dr_vs_ele1_energy",";#Delta R [mm];Mom. [MeV]",100,0,50,100,0,3500)
h_dr_vs_ele2_mom = r.TH2F("dr_vs_ele2_energy",";#Delta R [mm];Mom. [MeV]",100,0,50,100,0,4500)
h_dr = r.TH1F("dr",";#Delta R [mm];Events",100,0,50)

h_brem1_r = r.TH1F("brem1_r",";r_{#gamma,1} [mm];Events",100,0,50)
h_brem2_r = r.TH1F("brem2_r",";r_{#gamma,2} [mm];Events",100,0,50)

for i in xrange(totEvents):
    s.getEvent(i)
    recoil_hits = s.get_recoil_electrons_hcalSP_hits()
    brem_hits = s.get_brem_hcalSP_hits()
    if None in recoil_hits : 
        print "ahhhh!"
    else :
        hit_energy = map(lambda x : sqrt(sum(map(lambda y:y*y,x.getMomentum()))),recoil_hits)
        #print "recoil electron energies",hit_energy
        hit_r = map(lambda x : sqrt(x.getPosition()[0]*x.getPosition()[0]+x.getPosition()[1]*x.getPosition()[1]),recoil_hits)
        #print "recoil r:",hit_r
        hit_theta = map(lambda x : 180./3.1415*arctan(x.getPosition()[1]/x.getPosition()[0]),recoil_hits)
        #print "recoil theta:",hit_theta
        hit_x = map(lambda x : x.getPosition()[0],recoil_hits)
        #print "recoil x:",hit_x
        hit_y = map(lambda x : x.getPosition()[1],recoil_hits)
        #print "recoil y:",hit_y
        hit_z = map(lambda x : x.getPosition()[2],recoil_hits)
        #print "recoil z:",hit_z
        hit_mom = map(lambda x : sqrt(x.getMomentum()[0]**2+x.getMomentum()[1]**2+x.getMomentum()[2]**2),recoil_hits)
        #print "energies",hit_mom

        #print "separation:",sqrt((hit_x[1]-hit_x[0])**2+(hit_y[1]-hit_y[0])**2)
        h_dr.Fill(sqrt((hit_x[1]-hit_x[0])**2+(hit_y[1]-hit_y[0])**2))
        h_dr_vs_ele1_mom.Fill(sqrt((hit_x[1]-hit_x[0])**2+(hit_y[1]-hit_y[0])**2),hit_mom[0])
        h_dr_vs_ele2_mom.Fill(sqrt((hit_x[1]-hit_x[0])**2+(hit_y[1]-hit_y[0])**2),hit_mom[1])

    #s.dump_sim_particles(0.)
    #s.check_brems()
    isPN = s.check_photonuclear()
    #print isPN
    eles = s.get_beam_electrons()    
    h_vertex1.Fill(eles[0].getVertex()[0],eles[0].getVertex()[1])
    h_vertex2.Fill(eles[1].getVertex()[0],eles[1].getVertex()[1])
    h_z1.Fill(eles[0].getVertex()[2])
    h_z2.Fill(eles[1].getVertex()[2])

    brems = s.get_primary_brems()
    #print map(lambda x : x.getEnergy(),brems)
    
    e_brem1=0.
    e_brem2=0.
    r_brem1=0.
    r_brem2=0.
    if brems[0] != None : 
        e_brem1 = brems[0].getEnergy()
        r0 = brems[0].getVertex()
        p0 = brems[0].getMomentum()
        x1 = r0[0]+p0[0]*200/p0[2] 
        y1 = r0[1]+p0[1]*200/p0[2] 
        r_brem1 = sqrt(x1**2+y1**2)
    if brems[1] != None :
        e_brem2 = brems[1].getEnergy()
        r0 = brems[1].getVertex()
        p0 = brems[1].getMomentum()
        x1 = r0[0]+p0[0]*200/p0[2] 
        y1 = r0[1]+p0[1]*200/p0[2] 
        r_brem2 = sqrt(x1**2+y1**2)
    h_brem1_r.Fill(r_brem1)
    h_brem2_r.Fill(r_brem2)
    h_energy.Fill(e_brem1,e_brem2)
    h_isPN.Fill(isPN[0],isPN[1])
    #break
    #print "isPN:",isPN
    #print "brem energy:",e_brem1,e_brem2
    #print "--------"

can = r.TCanvas("can","can",500,500)
can.SetRightMargin(.2)
h_energy.Draw("colz")
can.SaveAs("brem_energies_"+tag+".png")

h_isPN.Draw("colz")
can.SaveAs("brem_isPN_"+tag+".png")

h_vertex1.Draw("colz")
can.SaveAs("ele1_vertex_"+tag+".png")
h_vertex2.Draw("colz")
can.SaveAs("ele2_vertex_"+tag+".png")

h_z1.Draw()
can.SaveAs("ele1_z_"+tag+".png")
h_z2.Draw()
can.SaveAs("ele2_z_"+tag+".png")

h_dr.Draw()
can.SaveAs("h_dr_"+tag+".png")

h_dr_vs_ele1_mom.Draw("colz")
can.SaveAs("h_dr_vs_ele1_mom_"+tag+".png")

h_dr_vs_ele2_mom.Draw("colz")
can.SaveAs("h_dr_vs_ele2_mom_"+tag+".png")

h_brem1_r.Draw()
can.SaveAs("h_brem1_r_"+tag+".png")

h_brem2_r.Draw()
can.SaveAs("h_brem2_r_"+tag+".png")
