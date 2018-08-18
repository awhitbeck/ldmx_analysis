import ROOT as r
import root_numpy as rn
import numpy as np
import pandas as pd

from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,auc

import matplotlib.pyplot as plt
from array import array

# - - - - - - - - - - - - - - - -
# function for computing ROC 
# and AUC metrics
# - - - - - - - - - - - - - - - - 
def roc(sig_histo,bkg_histo,nbins):
    total_sig = sum(sig_histo)
    eff_sig = array('f',[total_sig]*(nbins-1))
    scan_sig = 0.
    
    total_bkg = sum(bkg_histo)
    eff_bkg = array('f',[total_bkg]*(nbins-1))
    scan_bkg = 0.
    
    for ibin,num_events in enumerate(zip(sig_histo,bkg_histo)):
        eff_sig[ibin]-=scan_sig
        eff_sig[ibin]/=total_sig
        eff_bkg[ibin]-=scan_bkg
        eff_bkg[ibin]/=total_bkg
        scan_sig+=num_events[0]
        scan_bkg+=num_events[1]
    
    graph = r.TGraph(nbins-1,eff_sig,eff_bkg)
    graph.SetLineWidth(3)
    graph.GetXaxis().SetRangeUser(0.001,1)
    graph.GetXaxis().SetTitle("sig. eff.")
    graph.GetYaxis().SetRangeUser(0.001,1)
    graph.GetYaxis().SetTitle("bkg. eff.")
    print "AUC:",auc(eff_sig,eff_bkg)
    return graph

fin = r.TFile("nelsonVar_histos.root","READ")
bkg_tree = fin.Get("bkg_tree")
sig_tree = fin.Get("sig_1000mev_tree")

bkg_np_arr = rn.tree2array(bkg_tree)
sig_np_arr = rn.tree2array(sig_tree)

branches = rn.list_branches("nelsonVar_histos.root","bkg_tree")
print branches

features = []
for branch in branches : 
    if 'cylinder' in branch : 
        features.append(branch)

sig_dic = {}
bkg_dic = {}

for branch,bkg_data,sig_data in zip(branches,zip(*bkg_np_arr),zip(*sig_np_arr)):
    sig_dic[branch] = sig_data
    bkg_dic[branch] = bkg_data

sig_df = pd.DataFrame(sig_dic)
sig_df["label"] = [1]*len(sig_df)
bkg_df = pd.DataFrame(bkg_dic)
bkg_df["label"] = [0]*len(bkg_df)

sig_df["recoil_dr"] = map(lambda x,y:np.sqrt((x[0]-x[1])**2+(y[0]-y[1])**2),sig_df["ele0_x"],sig_df["ele0_y"])
bkg_df["recoil_dr"] = map(lambda x,y:np.sqrt((x[0]-x[1])**2+(y[0]-y[1])**2),bkg_df["ele0_x"],bkg_df["ele0_x"])

df = pd.concat([sig_df,bkg_df])

print df.head()

seed = 12345
test_size = 0.2
df_train, df_test = train_test_split(df,test_size=test_size,random_state=seed)

X_train = df_train[features]
X_test = df_test[features]
y_train = df_train["label"]
y_test = df_test["label"]

model = XGBClassifier()
model.fit(X_train,y_train)

df_train["prob"] = zip(*model.predict_proba(X_train))[1]
df_test["prob"] = zip(*model.predict_proba(X_test))[1]

df_train["pred"] = model.predict(X_train)
df_test["pred"] = model.predict(X_test)

df_train.to_pickle("train_data_post_training.pkl")
df_test.to_pickle("test_data_post_training.pkl")

y_prob = zip(*model.predict_proba(X_test))[1]
y_pred = model.predict(X_test)
#print zip(y_prob,y_pred)

accuracy = accuracy_score(y_test,y_pred)
print "Accuracy: {0}".format(accuracy*100)

sig_prob = zip(*filter(lambda x : x[1]==1,zip(y_prob,y_test)))[0]
bkg_prob = zip(*filter(lambda x : x[1]==0,zip(y_prob,y_test)))[0]

sig_prob_dr_0_25 = zip(*filter(lambda x : x[1]==1 and x[2]<25.,zip(y_prob,y_test,df_test["recoil_dr"])))[0]
bkg_prob_dr_0_25 = zip(*filter(lambda x : x[1]==0 and x[2]<25.,zip(y_prob,y_test,df_test["recoil_dr"])))[0]

sig_prob_dr_25_50 = zip(*filter(lambda x : x[1]==1 and x[2]>15. and x[2]<50. ,zip(y_prob,y_test,df_test["recoil_dr"])))[0]
bkg_prob_dr_25_50 = zip(*filter(lambda x : x[1]==0 and x[2]>15. and x[2]<50. ,zip(y_prob,y_test,df_test["recoil_dr"])))[0]

sig_prob_dr_50 = zip(*filter(lambda x : x[1]==1 and x[2]>50. ,zip(y_prob,y_test,df_test["recoil_dr"])))[0]
bkg_prob_dr_50 = zip(*filter(lambda x : x[1]==0 and x[2]>50. ,zip(y_prob,y_test,df_test["recoil_dr"])))[0]

nbins=100
start=0.
finish=1.
sig_histo = plt.hist(sig_prob,bins=np.arange(start,finish,(finish-start)/nbins),histtype='step')
bkg_histo = plt.hist(bkg_prob,bins=np.arange(start,finish,(finish-start)/nbins),histtype='step')
default_roc = roc(sig_histo[0],bkg_histo[0],nbins)

sig_dr_0_25_histo = plt.hist(sig_prob_dr_0_25,bins=np.arange(start,finish,(finish-start)/nbins),histtype='step')
bkg_dr_0_25_histo = plt.hist(bkg_prob_dr_0_25,bins=np.arange(start,finish,(finish-start)/nbins),histtype='step')
dr_0_25_roc = roc(sig_dr_0_25_histo[0],bkg_dr_0_25_histo[0],nbins)
dr_0_25_roc.SetLineColor(2)

sig_dr_25_50_histo = plt.hist(sig_prob_dr_25_50,bins=np.arange(start,finish,(finish-start)/nbins),histtype='step')
bkg_dr_25_50_histo = plt.hist(bkg_prob_dr_25_50,bins=np.arange(start,finish,(finish-start)/nbins),histtype='step')
dr_25_50_roc = roc(sig_dr_25_50_histo[0],bkg_dr_25_50_histo[0],nbins)
dr_25_50_roc.SetLineColor(4)

sig_dr_50_histo = plt.hist(sig_prob_dr_50,bins=np.arange(start,finish,(finish-start)/nbins),histtype='step')
bkg_dr_50_histo = plt.hist(bkg_prob_dr_50,bins=np.arange(start,finish,(finish-start)/nbins),histtype='step')
dr_50_roc = roc(sig_dr_50_histo[0],bkg_dr_50_histo[0],nbins)
dr_50_roc.SetLineColor(6)

default_roc.Draw("Al")
dr_0_25_roc.Draw("l")
dr_25_50_roc.Draw("l")
dr_50_roc.Draw("l")

plt.yscale('log')
plt.show()
plt.legend(['signal (1 GeV) - all','target PN - all',
            'signal (1 GeV) - dr<25','target PN - dr<25'])

