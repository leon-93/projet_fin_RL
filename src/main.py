#!/usr/bin/python3

import numpy as np
import random
import argparse
import sys
import fileinput
import csv
import simpy
from   app 	import app, init, qos
import os.path
from os import path
import os
from pathlib import Path


class params():
	'''def sim_transmit(env, ed, bsDict, server, algo):
		while True:
			np.random.seed(100)
			yield env.timeout(random.expovariate(1/ed.period))
			if algo == "epsilon_greedy":
				chosen_action = epsilon_greedy.choose_action()
			elif algo == "ucb":
				chosen_action = ucb.choose_action()
        
        	yield env.timeout(ed.send(bsDict, chosen_action))
		
        	for bsid, bs in bsDict.items():
			bs.receive(ed)
        	yield env.timeout(server.send(ed))
        	ed.receive()
            yield env.timeout(ed.period - ed.time - ed.wait)'''

	def log(ed,params,j):
		print(ed.H[ed.bestbs.id].time, params.xesults[j].dr) # ed.H[ed.bestbs.id].id,j
	
	

params.range = 14000
params.d0 = 40.0
params.gamma = 2.2394
params.Lpld0 = 95.0038
params.GL = 0
params.distribution  = [0.1, 0.2, 0.2, 0.2, 0.2, 0.1]

params.algo = "EpsilonGreedy" #, "UCB","markov", "exp3", "random", "bayesUCB", "thompson", "klUCB"])
params.nrBS = 1
params.nrED = 100
params.ps  = 10
params.period_mn = 1

params.bwSet  = [125,250,500]
params.powerSet = [11,12,13,14]
params.crSet  = [1,2,3,4]
params.sfSet  = [7, 8, 9, 10, 11, 12]
params.freqSet = [868100]


params.capture, params.interaction              = qos.getInteractionMatrix(True, True)
params.nrPkt    = 50 #650 # 2min #3.58j chaque 4min
params.tau      = 0.1
params.discount = 0.9
params.alpha    = 0.9
params.snrx   = [-20,-17.5,-15,-12.5,-10,-7.5]
params.drx    = [0.25,0.44,0.98,1.76,3.125,5.47]
params.sensi = qos.getSensi()
params.roopath = "./---"

# 6 simulator
params.objective                                                                            = lambda pkt:pkt.dr_mean
params.topopath                                                                             = "../res/"

class a():
	pass

params.results		= a()
params.xesults		= {i:a() for i in range(4)}
params.zesults		= {i:a() for i in range(4)}

def sim_transmit(env, ed, bsDict, server):
	while True:
		np.random.seed(100)
		yield env.timeout(random.expovariate(1/ed.period))
		yield env.timeout(ed.send(bsDict))
		for bsid, bs in bsDict.items():
			bs.receive(ed)
		yield env.timeout(server.send(ed))
		ed.receive()
		yield env.timeout(ed.period - ed.time - ed.wait)



def run(params):
	params.period	  = int(params.period_mn*60*1000)
	params.sim_time = int(params.period*params.nrPkt*2)
	params.path1     = params.roopath+"/"+str(params.algo)+"/"+str(params.nrBS)+"_"+str(params.nrED)+"_"+format(params.period_mn,'03')+"_"+str(params.ps)

	init.createNetwork(params)
	params.env      = simpy.Environment()
	
	for bs in params.bsDict.values():
		bs.reload()
	for ed in params.edDict.values():
		ed.reload()
	params.server.reload()

# run
	for ed in params.edDict.values():
		params.env.process(sim_transmit(params.env, ed, params.bsDict, params.server))
	params.env.run(until=params.sim_time)

params.cluster = np.loadtxt(params.topopath+'clustering/fcm.csv', dtype='int'  , delimiter=',', skiprows=0)
params.i = 0
np.set_printoptions(precision=2, suppress=True)
np.random.seed(100)
run(params)


