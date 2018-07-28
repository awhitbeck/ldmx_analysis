from sampleInfo import *

def include_overflow(histo):
    temp=r.TH1F(histo.GetName()+"_inc_ovrflw",histo.GetTitle(),histo.GetNbinsX()+1,histo.GetBinLowEdge(1),histo.GetBinLowEdge(histo.GetNbinsX())+2*histo.GetBinWidth(histo.GetNbinsX()))
    for i in xrange(1,histo.GetNbinsX()+2):
        temp.SetBinContent(i,histo.GetBinContent(i))
        temp.SetBinError(i,histo.GetBinError(i))
    return temp

def plot_var(draw_var,var_tag,binning,xaxis_label,cut,norm=True,log=True,overflow=True,use_dm_target=False):

    print '[plot_var] -- parameters --'
    print 'draw_var',draw_var
    print 'var_tag',var_tag
    print 'binning',binning
    print 'xaxis_label',xaxis_label
    print 'cut',cut
    print 'norm',norm
    print 'log',log
    print 'overflow',overflow
    print '---------------------------'

    r.gROOT.SetBatch(True)
    r.gROOT.ProcessLine('.L ~/tdrstyle.C')
    r.gROOT.ProcessLine('setTDRStyle()')

    trees = get_trees()
    histos = {}

    bin_max=0.
    bin_min=99999999.

    for s in trees : 
        print 'Sample:',s
        #if s == 'ecal_pn_inc' : continue
        #if s == '1p0' : continue
        if use_dm_target : 
            trees[s].Draw(draw_var+'>>'+var_tag+'_'+s+binning,'('+cut+')*PN_weight*'+str(dm_target_weight[s]))
        else :
            trees[s].Draw(draw_var+'>>'+var_tag+'_'+s+binning,'('+cut+')*PN_weight*'+str(xsec_weight[s]))


        histos[s] = r.gDirectory.Get(var_tag+'_'+s)
        if histos[s] == None : 
            print 'AHHHH',s
        if overflow : 
            histos[s] = include_overflow(histos[s])
        histos[s].GetXaxis().SetTitle(xaxis_label)
        if norm : 
            histos[s].GetYaxis().SetTitle('Events')
        else :
            histos[s].GetYaxis().SetTitle('Events/4e14 EoT')
        histos[s].SetLineColor(line_colors[s])
        histos[s].SetMarkerColor(line_colors[s])
        histos[s].SetLineStyle(line_styles[s])
        histos[s].SetLineWidth(line_widths[s])

        if norm and histos[s].Integral() > 0.: 
            histos[s].Scale(1./histos[s].Integral())

        if histos[s].GetMaximum() > bin_max : 
            bin_max=histos[s].GetMaximum()
        if histos[s].GetMinimum() < bin_min and histos[s].GetMinimum() != 0. : 
            bin_min=histos[s].GetMinimum()

        #histos[s].Print('all')

    if bin_min == 99999999. : bin_min = 0.1
    print 'bin_max:',bin_max
    print 'bin_min:',bin_min
        
    can = r.TCanvas('can','can',500,500)
    if log : 
        can.SetLogy()

    leg = r.TLegend(0.2,.85,.9,.92)
    leg.SetNColumns(5)
    leg.SetBorderSize(0)
    leg.SetFillColor(0)
    
    first=True
    for s in histos:
        leg.AddEntry(histos[s],s,'l')
        if first : 
            histos[s].GetYaxis().SetRangeUser(bin_min/10.,bin_max*( 10. if log else 1.2 ) )
            histos[s].Draw('hist,e1')
            first = False
        else : 
            histos[s].Draw('hist,e1,same')

    leg.Draw()
    can.SaveAs('../plots/dm_target_norm/'+var_tag+('_norm'if norm else '')+('_linear' if not log else '')+'.png')
    #can.SaveAs('../plots/'+var_tag+('_norm'if norm else '')+('_linear' if not log else '')+'.png')

    return histos

if __name__ == '__main__':
    if len(sys.argv) == 5 :
        plot_var(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
    elif len(sys.argv) == 5 :
        plot_var(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
    else:
        plot_var(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6])
