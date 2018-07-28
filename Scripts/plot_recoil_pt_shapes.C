

void plot_recoil_pt_shapes(){

  gROOT->ProcessLine(".L ~/tdrstyle.C");
  gROOT->ProcessLine("setTDRStyle()");
  
  TCanvas* can = new TCanvas("can","can",500,500);
  can->SetLogy();

  TFile* inputFile = new TFile("interpretation_histos_112_PN_5_EN.root","READ");
  inputFile->ls();

  TH1F* en_hist = (TH1F*) inputFile->Get("ecoil_e_pt_hcal_sideband_target_en_inc_ovrflw");
  //cout << en_hist << endl;
  en_hist->SetFillStyle(3353);
  en_hist->GetYaxis()->SetTitle("Events (a.u.)");
    
  TH1F* pn_hist = (TH1F*) inputFile->Get("ecoil_e_pt_hcal_sideband_ecal_pn_inc_ovrflw");
  //pn_hist->GetYaxis()->SetTitle("Events (a.u.)");
    
  //pn_hist->DrawNormalized("HIST");
  //en_hist->DrawNormalized("SAME,HIST");
    
  // TLegend* leg = new TLegend(.6,.6,.9,.9);
  // leg->SetBorderSize(0);
  // leg->SetFillColor(0);
  // leg->AddEntry(en_hist,"EN","lf");
  // leg->AddEntry(pn_hist,"PN","lf");
    
  //leg->Draw();
    
  //can->SaveAs("en_pn_pt_shapes.png");

}
