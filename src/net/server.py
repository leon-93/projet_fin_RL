#!/usr/bin/env python

import numpy as np

from etc import myann
from etc import myrandom
from etc import myqlearning
from etc import mypolicyiteration
from etc import myexp3
from etc import mythompson
from etc import myucb
from etc import myklucb
from etc import myepsilongreedy

class myServer:
	def __init__(self, params):
		self.params			= params

	def reload(self):
		self.idx = 0
		self.grix				= np.empty((self.params.nrED, self.params.nrBS))
		self.grix[:]		= np.nan
		self.grid				= np.zeros((self.params.nrED, self.params.nrBS))


		if self.params.algo   == "Random":
			self.model = myrandom.Random(self.params)
		if self.params.algo   == "ANN":
			self.model = myann.ANN(self.params)
		elif self.params.algo == "Q-learning":
			self.model = myqlearning.Qlearning(self.params)
		elif self.params.algo   == "PolicyIteration":
			self.model = mypolicyiteration.PolicyIteration(self.params)
		elif self.params.algo == "EXP3":
			self.model = myexp3.EXP3(self.params)
		elif self.params.algo == "Thompson":
			self.model = mythompson.Thompson(self.params)
		elif self.params.algo == "UCB":
			self.model = myucb.UCB(self.params)
		elif self.params.algo == "klUCB":
			self.model = myklucb.klUCB(self.params)
		elif self.params.algo == "EpsilonGreedy":
			self.model = myepsilongreedy.EpsilonGreedy(self.params)
		else:
			print("invalid algorithm")
			exit(0)


	def receive(self, pkt):
		self.grid[pkt.ed.id][pkt.bs.id] = pkt.prx
		self.grix[pkt.ed.id][pkt.bs.id] = 1


	def send(self, ed):
		a																= self.grid[ed.id] * self.grix[ed.id]
		b																= 0 if np.isnan(a).all() else np.nanargmax(a)
		ed.bestbs												= self.params.bsDict[b]
		ed.prx_mean											= ed.H[ed.bestbs.id].prx_mean
		ed.toa_mean											= ed.H[ed.bestbs.id].toa_mean
		ed.etx_mean											= ed.H[ed.bestbs.id].etx_mean
		ed.ber_mean											= ed.H[ed.bestbs.id].ber_mean
		ed.snr_mean											= ed.H[ed.bestbs.id].snr_mean
		ed.dr_mean											= ed.H[ed.bestbs.id].dr_mean
		ed.pdr_mean											= ed.H[ed.bestbs.id].pdr_mean
		ed.T_mean 											= ed.H[ed.bestbs.id].T_mean
		ed.G_mean 											= ed.H[ed.bestbs.id].G_mean
		ed.r_mean												= ed.H[ed.bestbs.id].r_mean
#		app.writeLine(self.params.path2+"/"+str(ed.edapp)+"_"+str(ed.id)+".csv", logs.pktlog(ed.H[ed.bestbs.id]))

		if ed.id == 0:
			self.idx+=1
			for j in range(1):
				tmp  = [(ed.pdr_mean, ed.toa_mean, ed.ber_mean, ed.etx_mean, ed.prx_mean, ed.snr_mean, ed.dr_mean, ed.T_mean, ed.G_mean, ed.r_mean) for ed in self.params.edDict.values() if ed.edapp == j or j == 3]
				tmp = np.array(tmp)
				self.params.xesults[j].pdr  = np.mean(tmp[:,0])
				self.params.xesults[j].toa  = np.mean(tmp[:,1])
				self.params.xesults[j].ber  = np.mean(tmp[:,2])
				self.params.xesults[j].etx  = np.mean(tmp[:,3])
				self.params.xesults[j].prx  = np.mean(tmp[:,4])
				self.params.xesults[j].snr  = np.mean(tmp[:,5])
				self.params.xesults[j].dr   = np.mean(tmp[:,6])
				self.params.xesults[j].T    = np.mean(tmp[:,7])
				self.params.xesults[j].G    = np.mean(tmp[:,8])
				self.params.xesults[j].r    = np.mean(tmp[:,9])
				
				self.params.zesults[j].pdr  = np.mean([self.params.zesults[j].pdr, self.params.xesults[j].pdr]) if self.idx != 1 else self.params.xesults[j].pdr
				self.params.zesults[j].toa  = np.mean([self.params.zesults[j].toa, self.params.xesults[j].toa]) if self.idx != 1 else self.params.xesults[j].toa
				self.params.zesults[j].ber  = np.mean([self.params.zesults[j].ber, self.params.xesults[j].ber]) if self.idx != 1 else self.params.xesults[j].ber
				self.params.zesults[j].etx  = np.mean([self.params.zesults[j].etx, self.params.xesults[j].etx]) if self.idx != 1 else self.params.xesults[j].etx
				self.params.zesults[j].prx  = np.mean([self.params.zesults[j].prx, self.params.xesults[j].prx]) if self.idx != 1 else self.params.xesults[j].prx
				self.params.zesults[j].snr  = np.mean([self.params.zesults[j].snr, self.params.xesults[j].snr]) if self.idx != 1 else self.params.xesults[j].snr
				self.params.zesults[j].dr   = np.mean([self.params.zesults[j].dr,  self.params.xesults[j].dr])  if self.idx != 1 else self.params.xesults[j].dr
				self.params.zesults[j].T    = np.mean([self.params.zesults[j].T,   self.params.xesults[j].T])   if self.idx != 1 else self.params.xesults[j].T
				self.params.zesults[j].G    = np.mean([self.params.zesults[j].G,   self.params.xesults[j].G])   if self.idx != 1 else self.params.xesults[j].G
				self.params.zesults[j].r    = np.mean([self.params.zesults[j].r,   self.params.xesults[j].r])   if self.idx != 1 else self.params.xesults[j].r
				self.params.log(ed, self.params, j)

		if not np.isnan(a).all():
			if ed.PP.full():
				ed.PP.get()
				ed.PP.put(ed.P[ed.bestbs.id])
			else:
				ed.PP.put(ed.P[ed.bestbs.id])
		self.grid[ed.id] 								= np.zeros(self.params.nrBS)
		self.grix[ed.id] 								= np.empty(self.params.nrBS)
		self.grix[ed.id]								= np.nan
		ed.reward[ed.action][ed.app]		= ed.packets[ed.bestbs.id].r
		self.model.update(ed)
		ed.bestbs.add(ed.ack[ed.bestbs.id].update(ed.newaction))
		ed.wait = ed.ack[ed.bestbs.id].toa
		return ed.wait
















