import sys,os
sys.path.append(os.getcwd()+'/../Utils/')

from theoryUtils import *
import ROOT as r

xsec = DMxsec()
target = DMthermalTarget()

base_dir='/nfs/slac/g/ldmx/users/whitbeck/recoil/analysis/root_files_v5/'

files={'0p001':'signal_mA_0p001_recon.root',
       '0p01':'signal_mA_0p01_recon.root',
       '0p1':'signal_mA_0p1_recon.root',
       '1p0':'signal_mA_1p0_recon.root',
       'ecal_pn':'ecal_pn_v5_magnet_bdt_skim_recon.root',
       #'ecal_pn_inc':'ecal_pn_v5_magnet_recon.root',
       'target_pn':'target_pn_v5_magnet_recon.root',
       'target_en':'reco_e_target_en_v3_magnet_4pt0_gev_recon.root'
       }

is_bkg={'0p001':False,'0p01':False,'0p1':False,'1p0':False,'ecal_pn':True,'ecal_pn_inc':False,'target_pn':True,'target_en':True}

xsec_weight={'0p001':xsec.get_xsec(0.001)*0.88*1e-7/1801407.,
             '0p01':xsec.get_xsec(0.01)*0.88*1e-7/2880916.,
             '0p1':xsec.get_xsec(0.1)*0.88*1e-7/1653273.,
             '1p0':xsec.get_xsec(1.0)*0.88*1e-7/1622770.,
             'ecal_pn':4./1.16,
             'ecal_pn_inc':1.,
             'target_pn':4./1.27,
             'target_en':4./3.16
             }

print 'termal target 0p001:',target.get_epsilon_squared(0.001/3.),', cross section:',xsec.get_xsec(0.001)
print 'termal target 0p01:',target.get_epsilon_squared(0.01/3.),', cross section:',xsec.get_xsec(0.01)
print 'termal target 0p1:',target.get_epsilon_squared(0.1/3.),', cross section:',xsec.get_xsec(0.1)
print 'termal target 1p0:',target.get_epsilon_squared(1.0/3.),', cross section:',xsec.get_xsec(1.0)

dm_target_weight = {'0p001':xsec.get_xsec(0.001)*0.88*target.get_epsilon_squared(0.001/3.)/1801407.,
                     '0p01':xsec.get_xsec(0.01)*0.88*target.get_epsilon_squared(0.01/3.)/2880916.,
                     '0p1':xsec.get_xsec(0.1)*0.88*target.get_epsilon_squared(0.1/3.)/1653273.,
                     '1p0':xsec.get_xsec(1.0)*0.88*target.get_epsilon_squared(1.0/3.)/1622770.*1000.,
                     'ecal_pn':4./1.16,
                     'ecal_pn_inc':1.,
                     'target_pn':4./1.27,
                     'target_en':4./3.16
                     }

line_colors={'0p001':2,'0p01':2,'0p1':6,'1p0':6,'ecal_pn':3,'ecal_pn_inc':3,'target_pn':4,'target_en':4}
line_styles={'0p001':1,'0p01':2,'0p1':1,'1p0':2,'ecal_pn':1,'ecal_pn_inc':2,'target_pn':1,'target_en':2}
line_widths={'0p001':2,'0p01':2,'0p1':2,'1p0':2,'ecal_pn':2,'ecal_pn_inc':2,'target_pn':2,'target_en':2}

def get_trees():
    trees = {}
    for s in files : 
        trees[s] = r.TChain("analysis_tree")
        trees[s].Add(base_dir+files[s])

    return trees
