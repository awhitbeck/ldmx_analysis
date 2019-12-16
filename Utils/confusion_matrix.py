import ROOT as r
from ldmx_container_v2 import *

cont = ldmx_container("/u/hp/whitbeck/trigger_scint/ldmx-sw/ldmx_sim_events.root","","ldmx_sim_events_config.txt")
#cont.setup()
cont.getEvent(0)
cont.dump("HcalSimHits_sim")
cont.dump_sim_particles()
