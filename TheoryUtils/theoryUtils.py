import sys,os
sys.path.append(os.getcwd())
import ROOT as r
from array import array 

class DMxsec():

    def __init__(self,file_name='xsectable.dat'):
        print '[DMxsec::DMxsec]'

        self.xsecs={} ## multiple samples
        self.xsec=[]  ## average of multiple samples
        self.mass=[]
        self.graph=None

        input_file = open(os.getcwd()+'/../Utils/'+file_name)
        for line in input_file.readlines() : 
            words = line[:-1].split(' ')
            while '' in words : 
                words.remove('')
            words = map(float,words)
            mass = words[0]
            if mass in self.xsecs : 
                self.xsecs[mass].append(words[1])
            else : 
                self.xsecs[mass]=[words[1]]

        for m in self.xsecs : 
            num = len(self.xsecs[m])
            self.xsec.append((m,(sum(self.xsecs[m])/num)))
        self.xsec.sort(key=lambda t : t[0])
        self.mass,self.xsec =  map(list,zip(*self.xsec))
        print self.xsec
        print self.mass
        
        self.graph = r.TGraph(len(self.mass),array('f',self.mass),array('f',self.xsec))

        input_file.close()

    def get_xsec(self,mass=1.5) : 
        return self.graph.Eval(mass)

class DMthermalTarget():

    def __init__(self,file_name='ScalarRelicTarget_ratio3.dat'):
        print '[DMthermalTarget::DMthermalTarget]'
        
        self.y=[]
        self.mchi=[]
        self.graph=None
        self.mAp_over_mchi=1./3.
        self.alphaDark=0.5

        input_file = open(os.getcwd()+'/../Utils/'+file_name)
        for line in input_file.readlines() :
            words = line[:-1].split('\t')
            while '' in words : 
                words.remove('')
            words = map(float,words)
            self.y.append(words[1])
            self.mchi.append(words[0])
        self.graph = r.TGraph(len(self.mchi),array('f',self.mchi),array('f',self.y))

        input_file.close()

    def get_y(self,mass=1.5):
        return self.graph.Eval(mass)
    
    def get_epsilon_squared(self,mass):
        return self.graph.Eval(mass)/(self.mAp_over_mchi**4)/self.alphaDark
