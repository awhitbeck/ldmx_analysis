import sys
import ROOT as r
from math import sqrt

# Get the Event library
r.gSystem.Load("/u/hp/whitbeck//hcal_noise/ldmx-sw/ldmx-sw-install/lib/libEvent.so")

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
		self.ecalSPHits=None
		self.targetSPHits=None
		self.hcalDigis=None
		self.hcalVeto=None
		self.recoilHits=None
		self.findableTracks=None
		self.ecalVeto=None
		self.pnWeight=None
		self.trigger=None

		self.collection_type = {}
		self.collection_type_sec = {}

		if fns != '' :
			self.collection_type={'simParticles':('ldmx::SimParticle','SimParticles_sim'),
					      'ecalSPHits':('ldmx::SimTrackerHit','EcalScoringPlaneHits_sim'),
					      'targetSPHits':('ldmx::SimTrackerHit','TargetScoringPlaneHits_sim'),
					      'recoilHits':('ldmx::SimTrackerHit','RecoilSimHits_sim'),
					      'findableTracks':('ldmx::FindableTrackResult','FindableTracks_reco'),
					      'pnWeight':('ldmx::PnWeightResult','PNweight_reco'),
					      'ecalVeto':('ldmx::EcalVetoResult','EcalVeto_reco'),
					      'trigger':('ldmx::TriggerResult','Trigger_reco'),
					      }

			self.collection_type_sec={'hcalDigis':('ldmx::HcalHit','hcalDigis_reco'),
						  'hcalVeto':('ldmx::HcalVetoResult','HcalVeto_reco'),
						  }
		else :
			self.collection_type={'simParticles':('ldmx::SimParticle','SimParticles_sim'),
					      'ecalSPHits':('ldmx::SimTrackerHit','EcalScoringPlaneHits_sim'),
					      'targetSPHits':('ldmx::SimTrackerHit','TargetScoringPlaneHits_sim'),
					      'recoilHits':('ldmx::SimTrackerHit','RecoilSimHits_sim'),
					      'findableTracks':('ldmx::FindableTrackResult','FindableTracks_reco'),
					      'pnWeight':('ldmx::PnWeightResult','PNweight_reco'),
					      'ecalVeto':('ldmx::EcalVetoResult','EcalVeto_reco'),
					      'pnWeight':('ldmx::PnWeightResult','PNweight_reco'),
                                              'ecalVeto':('ldmx::EcalVetoResult','EcalVeto_reco'),
					      'hcalDigis':('ldmx::HcalHit','hcalDigis_reco'),
					      'hcalVeto':('ldmx::HcalVetoResult','HcalVeto_reco'),
					      'trigger':('ldmx::TriggerResult','Trigger_reco'),
					      }
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

	def getRecoil(self, scoringPlane = "ecalSPHits"):
		findable_tracks = self.findableTracks
		findable_dic = {}
		for findable_track in findable_tracks:
			#print 'findable?',findable_track.is4sFindable(),findable_track.is3s1aFindable(),findable_track.is2s2aFindable()
			if findable_track.is4sFindable() or findable_track.is3s1aFindable() or findable_track.is2s2aFindable() : 
				findable_dic[findable_track.getSimParticle()] = findable_track

		if len(findable_dic) != 1 : return [0.,0.,0.]
		
		findable_track = findable_dic.itervalues().next()
		sim_particle = findable_track.getSimParticle()
		#print 'sim pt',sqrt(sim_particle.getMomentum()[0]**2+sim_particle.getMomentum()[1]**2)
		p_find = sqrt(sum(map(lambda x: x*x,sim_particle.getMomentum())))
		pvec=[0.,0.,0.]
		p_max=0.
		for hit in getattr(self,scoringPlane):
			if scoringPlane=="ecalSPHits" and hit.getID()!=26 : continue
			if scoringPlane=="recoilHits" and hit.getLayerID()!=1 : continue
			if hit.getSimParticle() != sim_particle : continue
			mom = sqrt(sum(map(lambda x: x*x,hit.getMomentum())))
			#print 'hit mom:',mom
			#print '    pt:',sqrt(hit.getMomentum()[0]**2+hit.getMomentum()[1]**2)
			if mom > p_max : 
				p_max = mom
				pvec = hit.getMomentum()
			# if ( p_find - sqrt(sum(map(lambda x: x*x,hit.getMomentum()))) ) < min_mom_diff :
			# 	pvec = hit.getMomentum()

		return pvec

	def findable_tracks(self):
		return sum(map(lambda x : x.is4sFindable() or x.is3s1aFindable() or x.is2s2aFindable(),s.findableTracks))

	def recoil_hit_counts(self,res):
		for ir,r in enumerate(res) : 
			res[ir]=0
		#hit_counter=[0]*10
		for h in self.recoilHits:
			#hit_counter[h.getLayerID()-1]+=1
			res[h.getLayerID()-1]+=1
		#return hit_counter

	def recoil_hit_charges(self,res):
		for ir,r in enumerate(res) : 
			res[ir]=0.
		#hit_charge=[0]*10
		for h in self.recoilHits:
			#hit_charge[h.getLayerID()-1]+=h.getEdep()
			res[h.getLayerID()-1]+=h.getEdep()
		#return hit_charge
######################################################################
