from ROOT import *
from optparse import OptionParser
from array import array

# - - - - - ROOT STYLE - - - - - - 
gROOT.SetBatch(True)
gROOT.ProcessLine(".L ~/tdrstyle.C")
gROOT.ProcessLine("setTDRStyle()")

def build_model():

    return x,model,[core_mu,core_sigma,tail_mu,tail_sigma,frac]

def run_fit(hist,label,init_values=[0.5]*5) :
    #x,model,params = build_model()
    x = RooRealVar("x","x [mm]",0.,100.)

    exp_d = RooRealVar("exp_d","d",0.5,0.,1.)
    exp_c = RooRealVar("exp_c","c",0.5,0.,1.)
    exp_b = RooRealVar("exp_b","b",0.5,0.,1.)
    exp_a = RooRealVar("exp_a","a",0.5,0.,1.)
    poly = RooBernstein("poly","poly",x,RooArgList(exp_a,exp_b,exp_c,exp_d))
    c = RooRealVar("c","c",1.,0.,99999.)

    model = RooExponential("exp","exp",poly,c)
    params = [exp_d,exp_c,exp_b,exp_a,c]

    for ip,param in enumerate(params) : 
        param.setVal(init_values[ip])

    # core_mu = RooRealVar("core_mu","mu",0.,-10.,10.)
    # #core_mu.setConstant(True)
    # core_sigma = RooRealVar("core_sigma","sigma",3.,0.0,10.)
    
    # tail_mu = RooRealVar("tail_mu","mu",0.,-10.,10.)
    # #tail_mu.setConstant(True)
    # tail_sigma = RooRealVar("tail_sigma","sigma",10.,3.,500.)
    
    # core_gaus = RooGaussian("core_gaus","core_guas",x,core_mu,core_sigma)
    # tail_gaus = RooGaussian("tail_gaus","tail_guas",x,tail_mu,tail_sigma)

    # frac = RooRealVar("frac","frac",1.,0.,1.)
    
    # model = RooAddPdf("model","model",core_gaus,tail_gaus,frac)
    # params = [core_mu,core_sigma,tail_mu,tail_sigma,frac]

    hist.GetYaxis().SetRangeUser(0.0001,hist.GetMaximum()*10.)
    dataHist = RooDataHist("dataHist","dataHist",RooArgList(x),hist)

    model.fitTo(dataHist)

    can = TCanvas("can","can",500,500)
    
    fitPad = TPad("fit","fit",0.01,0.3,0.99,0.99)
    fitPad.SetTopMargin(.1)
    fitPad.Draw()
    ratioPad = TPad("ratio","ratio",0.01,0.01,0.99,0.29)
    ratioPad.SetBottomMargin(.07)
    ratioPad.SetTopMargin(0.)
    ratioPad.Draw()
    
    fitPad.cd()
    fitPad.SetLogy()

    plot = x.frame()
    dataHist.plotOn(plot)
    model.plotOn(plot)
    plot.GetYaxis().SetTitle("Avg. E_{dep} [MeV]")
    plot.Draw()
    fitPad.Modified()
    fitPad.Update()

    ratioPad.cd()
   
    plot_r = x.frame(RooFit.Title("residuals"))
    residuals  = plot.residHist()
    plot_r.addPlotable(residuals,"P")
    plot_r.GetYaxis().SetRangeUser(-0.05,0.05)
    plot_r.GetYaxis().SetLabelSize(0.1)
    plot_r.GetYaxis().SetTitleSize(0.15)
    plot_r.GetYaxis().SetTitleOffset(0.5)
    plot_r.GetYaxis().SetNdivisions(503)
    plot_r.GetYaxis().SetTitle("Resid.")

    plot_r.GetXaxis().SetLabelSize(0.1)
    plot_r.GetXaxis().SetTitleSize(0.15)
    plot_r.GetXaxis().SetTitleOffset(0.5)
    plot_r.GetXaxis().SetTitle("x [mm]")

    plot_r.Draw()
    ratioPad.Modified()
    ratioPad.Update()

    can.SaveAs("fitter_shower_shape_layer"+label+".png")

    return map(lambda x : (x.GetName(),x.getVal(),x.getError()),params)

if __name__ == "__main__" : 

    inputFile = TFile("showerShape_histos.root","READ")
    res = []
    for i in xrange(30,-1,-1):
        h = inputFile.Get("shower_profile_layer"+str(i))
        if len(res) == 0 :
            res.append( run_fit(h,str(i)) )
        else : 
            res.append( run_fit(h,str(i),map(lambda x : x[1],res[-1])) )


    x = array('f',range(20))
    x_err = array('f',[0.]*20)            
    can2 = TCanvas("can2","can2",500,500)
    
    val_dic = {}
    err_dic = {}
    for i,r in enumerate(res) :
        for v in r : 
            if not v[0] in val_dic : 
                val_dic[v[0]] = [v[1]]
                err_dic[v[0]] = [v[2]]
            else : 
                val_dic[v[0]].append(v[1])
                err_dic[v[0]].append(v[2])

    for var in val_dic : 
        val_array = array('f',val_dic[var])
        err_array = array('f',err_dic[var])

        graph = TGraphErrors(20,x,val_array,x_err,err_array)
        graph.Draw("Ap")
        can2.SaveAs(var+".png")

