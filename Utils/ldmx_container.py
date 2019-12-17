import sys
import ROOT as r
from math import sqrt
from Queue import Queue
from itertools import groupby
from operator import itemgetter
import numpy as np

# Get the Event library
r.gSystem.Load("~/LDMX/ldmx-sw/ldmx-sw-install/lib/libEvent.so")

######################################################################
class ldmx_container:

        def __init__(self, fn, fns=''):

		self.fn = fn
		self.fns = fns

                self.tin = r.TChain("LDMX_Events")
                self.tin_sec = r.TChain("LDMX_Events_resim")
                self.fin = self.tin.Add(fn)
		if fns != '' :
			self.tin_sec.Add(fns)
                self.evHeader = r.ldmx.EventHeader()

		self.simParticles=None
		self.HcalSimHits=None
		self.collection_type = {}
		self.collection_type_sec = {}

		if fns != '' :
			self.collection_type={'simParticles':('ldmx::SimParticle','SimParticles_sim'),
					      'HcalSimHits':('ldmx::SimCalorimeterHit','HcalSimHits_sim'),
					      'TriggerPadUpSimHits':('ldmx::SimCalorimeterHit','TriggerPadUpSimHits_sim'),
					      'TriggerPadDownSimHits':('ldmx::SimCalorimeterHit','TriggerPadDownSimHits_sim'),
					      'TriggerPadTaggerSimHits':('ldmx::SimCalorimeterHit','TriggerPadTaggerSimHits_sim'),
					      'TrigScintScoringPlaneHits':('ldmx::SimTrackerHit','TrigScintScoringPlaneHits_sim')
					      }

			self.collection_type_sec={
						  }
		else :
			self.collection_type={'simParticles':('ldmx::SimParticle','SimParticles_sim'),
					      'HcalSimHits':('ldmx::SimCalorimeterHit','HcalSimHits_sim'),
					      'TriggerPadUpSimHits':('ldmx::SimCalorimeterHit','TriggerPadUpSimHits_sim'),
					      'TriggerPadDownSimHits':('ldmx::SimCalorimeterHit','TriggerPadDownSimHits_sim'),
					      'TriggerPadTaggerSimHits':('ldmx::SimCalorimeterHit','TriggerPadTaggerSimHits_sim'),
					      'TrigScintScoringPlaneHits':('ldmx::SimTrackerHit','TrigScintScoringPlaneHits_sim')

					      }

	def dump_sim_particles(self,energy_threshold=100.):
		print "- - - - - - - - new event - - - - - - - - - "
		for p in self.simParticles : 
			if p.getGenStatus() == 1 : 
				offset=""
				particle_queue = Queue()
				particle_queue.put(p)
				visited = []
				visited.append(p)
				print "id:",p.getPdgID(),"energy:",p.getEnergy()
				while not particle_queue.empty():
					q = particle_queue.get()
					offset+="-"
					for idau in xrange(p.getDaughterCount()):
						d = p.getDaughter(idau)
						if d.getEnergy() < energy_threshold : continue
						if not d in visited :
							particle_queue.put(d)
							visited.append(d)
							print offset,"id:",d.getPdgID(),"parent id:",d.getParent(0).getPdgID(),"energy:",d.getEnergy(),"processType:",d.getProcessType()
				del particle_queue
				del visited

	def dump(self,coll=''):
		print '[ldmx_container::dump]'
		if coll == '' :
			for collection in self.collection_type:
				for x in getattr(self,collection) : 
					x.Print()
			for collection in self.collection_type_sec:
				for x in getattr(self,collection) :
					if collection == 'hcalDigis' : 
						print "noise:",x.getNoise()
					x.Print()

		else : 
			for x in getattr(self,coll) :
				x.Print()
			
	def setup(self):		
		print '[ldmx_container::setup]'
		for collection in self.collection_type_sec:
			setattr(self,collection,r.TClonesArray(self.collection_type_sec[collection][0]))
			self.tin_sec.SetBranchAddress(self.collection_type_sec[collection][1], r.AddressOf( getattr(self,collection) ))
		for collection in self.collection_type:
			setattr(self,collection,r.TClonesArray(self.collection_type[collection][0]))
			self.tin.SetBranchAddress(self.collection_type[collection][1], r.AddressOf( getattr(self,collection) ))

        def getEvent(self,i=0):
                self.tin.GetEntry(i)
		if(self.fns != ''):
			self.tin_sec.GetEntry(i)


        ## grab all  beam electrons
        # returns: empty dictionary  (key: x position of vertex)
	def beam_electrons(self):
		electrons={}
		for p in getattr(self,"simParticles"):
			if p.getGenStatus()==1 and p.getPdgID() == 11 :
				electrons[p.getVertex()[1]]=[]
		return electrons
        
        ## counts the number of beam electrons
        # returns: integer
	def num_beam_electrons(self):
		count_particles=0
		for p in getattr(self,"simParticles"):
			if p.getGenStatus()==1 and p.getPdgID() == 11 : 
				count_particles+=1
		return count_particles

        ## get number of beam electrons that hit target array
        def count_true(self,coll):
                electrons=self.gen_hits(coll)
                true_electrons=0
                for e in electrons:
                        if len(electrons[e])>0:
                                true_electrons+=1
                return true_electrons

        
        ## gets a list of energy deposits in each bars
        ## NOTE: number of cells is hard coded!
        # takes: string corresponding to the collection for which hits are deposited in
        # returns: list of floats
	def trigger_pad_edep(self,coll="TriggerPadUpSimHits"):
		hits=[0.]*62
		for x in getattr(self,coll):
			hit_id = x.getID()>>4
			hits[hit_id-2]+=x.getEdep()
		return hits

        ## gets a list of number of PEs deposited in each cell
        ## NOTE: number of cells is hard coded!
        # takes: string corresponding to the collection for which hits are deposited in
        # returns: lsit of floats
	def trigger_pad_pe(self,coll="TriggerPadUpSimHits"):
		hits=[0.]*62
		for x in getattr(self,coll):
			hit_id = x.getID()>>4
			hits[hit_id-2]+=x.getEdep()
		for i,edep in enumerate(hits) : 
			hits[i] = np.random.poisson(edep/.4 * 10. + 0.02)
		return hits

        
	def scan_trigger_pad_hits(self,coll="TriggerPadUpSimHits"):
		hits={}
		hit_ids=[]
		for x in getattr(self,coll):
			hit_id = x.getID()>>4
			if not hit_id in hits : 
				hits[hit_id]=[0.,0.]
			for i in range(x.getNumberOfContribs()):
				if x.getContrib(i).particle.getGenStatus()==1:
					hits[hit_id][0]+=x.getContrib(i).edep
				else : 
					print "hit_id",hit_id,":",x.getContrib(i).particle.getPdgID(),"parent",x.getContrib(i).particle.getParent(0).getPdgID(),x.getContrib(i).particle.getParent(0).getGenStatus()
					hits[hit_id][1]+=x.getContrib(i).edep

		print hits

        ## get list of electrons that hit cells in target collection
        # takes: string refering to name of target collection
        # return: dictionary of hits for each gen electron
	def gen_hits(self,coll="TriggerPadUpSimHits"):
		electrons=self.beam_electrons()
		for x in getattr(self,coll):
			hit_id = x.getID()>>4
			for i in range(x.getNumberOfContribs()):
				#print x.getContrib(i).particle.getPdgID(),x.getContrib(i).particle.getGenStatus()
				#print x.getContrib(i).particle.getVertex()[1]
				#print "electrons",electrons
				#if x.getContrib(i).particle in electrons :
				if x.getContrib(i).particle.getVertex()[1] in electrons:
					electrons[x.getContrib(i).particle.getVertex()[1]].append(hit_id)
		return electrons

        def count_hits(self,coll,min_pe):
                pes=self.trigger_pad_pe(coll)
                pes=map(lambda x: int(x>=min_pe),pes)
                num=reduce(lambda x,y:x+y,pes)
                return np.ceil(num/2)
        
        ## count the number of zero-suppressed hits within 2 cells of each other
        # takes: target collection ; minimum number of PE per cell to suppress
        # return: int, number of clusters
	def count_clusters(self,coll,min_pe=3):
		count=0
		hit_pe=self.trigger_pad_pe(coll)
		for j,pe in enumerate(hit_pe):
			if j == 0 :
				if pe>=min_pe : 
					count+=1            
			else :
				if pe>=min_pe and hit_pe[j-1]<min_pe and hit_pe[j-2]<min_pe:
					count+=1
		return count

	def print_sp_hits(self):
		for x in getattr(self,'TrigScintScoringPlaneHits') :
			print x.Print()

	def get_num_secondaries(self):
		count=0
		for x in getattr(self,'TrigScintScoringPlaneHits') :
			if x.getEnergy() < 3500. : 
				count+=1
		return count

######################################################################
