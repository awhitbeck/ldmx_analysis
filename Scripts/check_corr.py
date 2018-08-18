import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

df = pd.read_pickle("test_data_post_training.pkl")

df["recoil_px"] = zip(*df["ele0_px"].values)[1]
df["recoil_py"] = zip(*df["ele0_py"].values)[1]
df["recoil_pz"] = zip(*df["ele0_pz"].values)[1]

df["recoil_mom"]=map(lambda x : np.sqrt(x[0]**2+x[1]**2+x[2]**2),zip(df["recoil_px"],df["recoil_py"],df["recoil_pz"]))

df["recoil_pt"]=map(lambda x : np.sqrt(x[0]**2+x[1]**2),zip(df["recoil_px"],df["recoil_py"]))

#plt.hist2d(df["recoil_pt"],df["prob"],bins=[np.arange(0,100,2),np.arange(0,1,0.01)], norm=mpl.colors.LogNorm())

for f in df.columns : 
    print f,'cylinder' in f
    if not 'cylinder' in f and not 'recoil' in f : continue

    print f

    plt.scatter(df[df["label"]==1][f],df[df["label"]==1]["prob"],alpha=0.1,s=4)
    plt.scatter(df[df["label"]==0][f],df[df["label"]==0]["prob"],alpha=0.1,s=4)
    plt.xlabel(f)
    plt.ylabel('BDT prob.')
    #plt.show()
    plt.savefig(f+'_versus_bdt_prob.png')
    
    plt.clf()
