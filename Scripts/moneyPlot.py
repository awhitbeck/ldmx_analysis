from sampleInfo import *
from test import *
from sys import argv

def main(pn_bkg,target_en):
    signals = ['0p001','0p01','0p1','1p0']
    xsec_weight['1p0']*=1000.
    
    # ---- predicted event yields ---
    # target_muons = 0.
    # ecal_muons = 1.*4.0/6.6
    # target_pn = 2.*4.
    # ecal_pn = 26.*4.
    # pn_bkg = target_muons+ecal_muons+target_pn+ecal_pn # 112.61
    # target_en = 13.*4./10. # 5.2
    # - - - - - - - - - - - - - - - -

    plotVar = 'sqrt(recoilTracker_simHit_recoil_py**2+recoilTracker_simHit_recoil_px**2)'

    fixed_eps = False
    histos_hcal_sb = plot_var(plotVar,'recoil_e_pt_hcal_sideband','(50,0.5,100.5)','Recoil-e p_{T} [MeV]','findable_tracks==1&&trigger_energy_sum<1500.&&EcalVeto_BDT>0.94&&max_back_hcal_pe>=3&&max_side_hcal_pe>=3',False,False,True,True)

    histos = plot_var(plotVar,'recoil_e_pt','(50,0.5,100.5)','Recoil-e p_{T} [MeV]','findable_tracks==1&&trigger_energy_sum<1500.&&EcalVeto_BDT>0.94&&max_back_hcal_pe<3&&max_side_hcal_pe<3',False,False,True,True)

    can = r.TCanvas('can','can',500,500)
    can.SetLogy()

    histos_hcal_sb['ecal_pn'].SetLineColor(1)
    histos_hcal_sb['ecal_pn'].SetFillColor(4)
    histos_hcal_sb['ecal_pn'].SetMarkerColor(4)
    histos_hcal_sb['ecal_pn'].SetLineStyle(1)
    histos_hcal_sb['ecal_pn'].SetLineWidth(3)
    histos_hcal_sb['ecal_pn'].Scale(pn_bkg/histos_hcal_sb['ecal_pn'].Integral())
    histos_hcal_sb['ecal_pn'].GetYaxis().SetRangeUser(histos_hcal_sb['ecal_pn'].GetMinimum()/10.,histos_hcal_sb['ecal_pn'].GetMaximum()*10.)
    histos_hcal_sb['ecal_pn'].GetYaxis().SetTitle('Events / 4 #times 10^{14} EoT')

    histos_hcal_sb['target_en'].SetLineColor(1)
    histos_hcal_sb['target_en'].SetFillColor(3)
    histos_hcal_sb['target_en'].SetMarkerColor(3)
    histos_hcal_sb['target_en'].SetLineStyle(1)
    histos_hcal_sb['target_en'].SetLineWidth(3)
    histos_hcal_sb['target_en'].Scale(target_en/histos_hcal_sb['target_en'].Integral())
    histos_hcal_sb['target_en'].GetYaxis().SetRangeUser(histos_hcal_sb['target_en'].GetMinimum()/10.,histos_hcal_sb['target_en'].GetMaximum()*10.)
    histos_hcal_sb['target_en'].GetYaxis().SetTitle('Events / 4 #times 10^{14} EoT')
    
    stack = r.THStack('bkg_stack','bkg_stack')
    stack.Add(histos_hcal_sb['target_en'])
    stack.Add(histos_hcal_sb['ecal_pn'])
    stack.Draw('histo')
    stack.GetXaxis().SetTitle('Recoil-e p_{T} [MeV]')
    stack.GetYaxis().SetTitle('Events / 4 #times 10^{14} EoT')
    if fixed_eps :
        stack.SetMaximum(400000.)
    else :
        stack.SetMaximum(4000.)

    can.RedrawAxis()

    leg = r.TLegend(0.3,.75,.9,.92)
    leg.SetNColumns(2)
    leg.SetBorderSize(0)
    leg.SetFillColor(0)
    leg.AddEntry(histos_hcal_sb['ecal_pn'],'PN bkg.','f')
    leg.AddEntry(histos_hcal_sb['target_en'],'EN bkg.','f')

    ts = can.GetTopMargin()
    rs = can.GetRightMargin();
    bs = can.GetBottomMargin()
    ls = can.GetLeftMargin();
    ldmx_label = r.TLatex();
    ldmx_label.SetNDC();
    ldmx_label.SetTextAngle(0.);
    ldmx_label.SetTextColor(1);
    ldmx_label.SetTextFont(52);
    ldmx_label.SetTextAlign(31);
    ldmx_label.DrawLatex(.95,(1-ts)*1.01,'LDMX preliminary')
    
    for s in signals :
        histos[s].SetLineColor(line_colors[s])
        histos[s].SetMarkerColor(line_colors[s])
        histos[s].SetLineStyle(line_styles[s])
        histos[s].SetLineWidth(3)
        histos[s].Draw('histo,same')
        if s == '1p0' : 
            leg.AddEntry(histos[s],"m_{A'}="+s.replace('p','.')+' (x10^{3})','l')
        else : 
            leg.AddEntry(histos[s],"m_{A'}="+s.replace('p','.'),'l')

    leg.Draw()

    if fixed_eps:
        can.SaveAs('moneyPlot_fixed_epsilon.png')
        can.SaveAs('moneyPlot_fixed_epsilon.pdf')
    else :
        can.SaveAs('moneyPlot_dm_target_norm_{0}_PN_{1}_EN.png'.format(int(pn_bkg),int(target_en)))
        can.SaveAs('moneyPlot_dm_target_norm_{0}_PN_{1}_EN.pdf'.format(int(pn_bkg),int(target_en)))


    total_bkg = r.TH1F(histos_hcal_sb['ecal_pn'])
    total_bkg.Add(histos_hcal_sb['target_en'])
    
    for s in signals:
        datacard = open('card_{0}_{1}_PN_{2}_EN.txt'.format(s,int(pn_bkg),int(target_en)),'w')
        datacard.write('''max    1     number of categories
jmax   *     number of samples minus one
kmax   *     number of nuisance parameters
-------------------------------------------------------------------------------
shapes * * interpretation_histos_{5}_PN_{6}_EN.root $PROCESS $PROCESS
-------------------------------------------------------------------------------
bin                                            sig_reg
observation                                    {0}
-------------------------------------------------------------------------------
bin                                            sig_reg      sig_reg      sig_reg
process                                        0            1            2
process                                        recoil_e_pt_{1}_inc_ovrflw    recoil_e_pt_hcal_sideband_ecal_pn_inc_ovrflw    recoil_e_pt_hcal_sideband_target_en_inc_ovrflw
rate                                           {2}                           {3}                                             {4}
-------------------------------------------------------------------------------
bkg_syst lnN                                   1.00         1.042        1.042'''.format(total_bkg.Integral(),s,histos[s].Integral(),histos_hcal_sb['ecal_pn'].Integral(),histos_hcal_sb['target_en'].Integral(),int(pn_bkg),int(target_en)))
        datacard.close()
    output_file = r.TFile('interpretation_histos_{0}_PN_{1}_EN.root'.format(int(pn_bkg),int(target_en)),'RECREATE')
    for s in histos : 
        histos[s].Write()
        histos_hcal_sb[s].Write()
    total_bkg.Write('data_obs')
    output_file.Close()

if __name__ == "__main__":
    pn_bkg = 1.
    target_en = 1.
    if len(argv) > 1 : 
        pn_bkg = float(argv[1])
    if len(argv) > 2 :
        target_en = float(argv[2])
    main(pn_bkg,target_en)
