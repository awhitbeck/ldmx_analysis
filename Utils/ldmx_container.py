import sys
import ROOT as r
from math import sqrt
from Queue import Queue

# Get the Event library
r.gSystem.Load("/nfs/slac/g/ldmx/users/whitbeck/dos_electrones/ldmx-sw/ldmx-sw-install/lib/libEvent.so")

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
		self.hcalSPHits=None
		self.targetSPHits=None
		self.hcalDigis=None
		self.hcalVeto=None
		self.recoilHits=None
		self.findableTracks=None
		self.ecalVeto=None
		self.pnWeight=None
		self.trigger=None
		self.ecalSimHits=None

		self.collection_type = {}
		self.collection_type_sec = {}

		if fns != '' :
			self.collection_type={'simParticles':('ldmx::SimParticle','SimParticles_sim'),
					      'ecalSPHits':('ldmx::SimTrackerHit','EcalScoringPlaneHits_sim'),
					      'hcalSPHits':('ldmx::SimTrackerHit','HcalScoringPlaneHits_sim'),
					      'targetSPHits':('ldmx::SimTrackerHit','TargetScoringPlaneHits_sim'),
					      'recoilHits':('ldmx::SimTrackerHit','RecoilSimHits_sim'),
					      'findableTracks':('ldmx::FindableTrackResult','FindableTracks_reco'),
					      'pnWeight':('ldmx::PnWeightResult','PNweight_reco'),
					      'ecalVeto':('ldmx::EcalVetoResult','EcalVeto_reco'),
					      'trigger':('ldmx::TriggerResult','Trigger_reco'),
					      'ecalSimHits':('ldmx::SimCalorimeterHit','EcalSimHits_sim')
					      }

			self.collection_type_sec={'hcalDigis':('ldmx::HcalHit','hcalDigis_reco'),
						  'hcalVeto':('ldmx::HcalVetoResult','HcalVeto_reco'),
						  }
		else :
			self.collection_type={'simParticles':('ldmx::SimParticle','SimParticles_sim'),
					      'ecalSPHits':('ldmx::SimTrackerHit','EcalScoringPlaneHits_sim'),
					      'hcalSPHits':('ldmx::SimTrackerHit','HcalScoringPlaneHits_sim'),
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
					      'ecalSimHits':('ldmx::SimCalorimeterHit','EcalSimHits_sim')
					      }

	def shower_vars(self,ele,mol_rad=23):
		ele_mom = ele.getMomentum()
		ele_pos = ele.getPosition()

		cylinder_0_1 = [0.]*33
		cylinder_1_3 = [0.]*33
		cylinder_3_5 = [0.]*33
		cylinder_5 = [0.]*33
		
		for h in self.ecalSimHits : 
			layer = self.compute_layer(h.getID())
			if layer < 0 or layer >= 33 : continue
			hit_pos = h.getPosition()
			ray_x_pos = ele_pos[0]+ele_mom[0]/ele_mom[2]*(hit_pos[2]-ele_pos[2]))
			ray_y_pos = ele_pos[1]+ele_mom[1]/ele_mom[2]*(hit_pos[2]-ele_pos[2]))
			rel_pos = [hit_pos[0]-ray_x_pos,pos[1]-ray_y_pos,0.]
			r=sqrt(rel_pos[0]**2+rel_pos[1]**2)
			
			if r < mol_rad : 
				cylinder_0_1[layer]+=hit.getEdep()
			elif r < 3*mol_rad : 
				cylinder_1_3[layer]+=hit.getEdep()
			elif r < 5*mol_rad : 
				cylinder_3_5[layer]+=hit.getEdep()
			else : 
				cylinder_5[layer]+=hit.getEdep()
		results={'cylinder_0_1_layer_0_0':sum(cylinder[:1]),
			 'cylinder_0_1_layer_1_2':sum(cylinder[1:3]),
			 'cylinder_0_1_layer_3_6':sum(cylinder[3:7]),
			 'cylinder_0_1_layer_7_14':sum(cylinder[7:15]),
			 'cylinder_0_1_layer_15':sum(cylinder[15:]),

			 'cylinder_1_3_layer_0_0':sum(cylinder[:1]),
			 'cylinder_1_3_layer_1_2':sum(cylinder[1:3]),
			 'cylinder_1_3_layer_3_6':sum(cylinder[3:7]),
			 'cylinder_1_3_layer_7_14':sum(cylinder[7:15]),
			 'cylinder_1_3_layer_15':sum(cylinder[15:]),

			 'cylinder_3_5_layer_0_0':sum(cylinder[:1]),
			 'cylinder_3_5_layer_1_2':sum(cylinder[1:3]),
			 'cylinder_3_5_layer_3_6':sum(cylinder[3:7]),
			 'cylinder_3_5_layer_7_14':sum(cylinder[7:15]),
			 'cylinder_3_5_layer_15':sum(cylinder[15:]),

			 'cylinder_5_layer_0_0':sum(cylinder[:1]),
			 'cylinder_5_layer_1_2':sum(cylinder[1:3]),
			 'cylinder_5_layer_3_6':sum(cylinder[3:7]),
			 'cylinder_5_layer_7_14':sum(cylinder[7:15]),
			 'cylinder_5_layer_15':sum(cylinder[15:])}
		
		return results

	def compute_layer(self,detID) :
		return (detID>>4)&255

	def get_recoil_electrons_hcalSP_hits(self):
		eles = self.get_beam_electrons()
		sp_hits = []
		for ele in eles : 
			max_momentum=0.
			max_SPhit=None
			for h in self.hcalSPHits : 
				temp_momentum = sqrt(sum(map(lambda x:x*x,h.getMomentum())))
				if ele == h.getSimParticle() and max_momentum < temp_momentum : 
					max_momentum = temp_momentum
					max_SPhit = h
			sp_hits.append(max_SPhit)
		return sp_hits

	def get_brem_hcalSP_hits(self):
		phos = self.get_primary_brems()
		sp_hits = []
		for pho in phos : 
			max_momentum=0.
			max_SPhit=None
			for h in self.hcalSPHits : 
				temp_momentum = sqrt(sum(map(lambda x:x*x,h.getMomentum())))
				if pho == h.getSimParticle() and max_momentum < temp_momentum : 
					max_momentum = temp_momentum
					max_SPhit = h
			sp_hits.append(max_SPhit)
		return sp_hits

	def get_beam_electrons(self):
		eles=[]
		for p in self.simParticles : 
			if p.getGenStatus() == 1 : 
				eles.append(p)
		return eles

	def get_primary_brems(self):
		brems = []
		eles = self.get_beam_electrons()
		for ele in eles : 
			dau_photons = []
			for idau in xrange(ele.getDaughterCount()):
				d = ele.getDaughter(idau)
				if d.getPdgID() == 22 : 
					dau_photons.append(d)
			target_dau_photons_energy = map(lambda x : x.getEnergy() if x.getVertex()[2]>-1.2 and x.getVertex()[2]<1.2 else 0.,dau_photons)
			dau_photons_energy = map(lambda x : x.getEnergy(),dau_photons)
			dau_photons_vertex = map(lambda x : x.getVertex()[2],dau_photons)
			#print 'energy:' , dau_photons_energy
			#print 'vertex:' , dau_photons_vertex
			#print 'energy (target only):' , target_dau_photons_energy
			if len(target_dau_photons_energy)==0: 
				brems.append(None)
			else : 
				brems.append(dau_photons[target_dau_photons_energy.index(max(target_dau_photons_energy))])

		return brems
	def check_ecalSP(self):
		for h in self.ecalSPHits:
			pos = h.getPosition()
			mom = h.getMomentum()
			print "position"," ".join(map(str,pos))
			print "momentum"," ".join(map(str,mom))

	def check_photonuclear(self):
		pn=[]
		brems = self.get_primary_brems()
		for p in brems:
			isPN=False
			if p != None :
				for idau in xrange(p.getDaughterCount()) :
					if p.getDaughter(idau).getProcessType() == 9 : 
						isPN=True
			pn.append(isPN)			
		return pn

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
