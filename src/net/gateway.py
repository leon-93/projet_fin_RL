#!/usr/bin/env python
import numpy as np
import copy
from   app import app

class myBS():
	def __init__ (self, params):
		self.params			= params

	def receive(self, ed):
		x   = self.check(ed.packets[self.id])
		measure = ed.packets[self.id].measure()
		self.clear(ed.packets[self.id])
		ed.H[self.id] = measure
		if x:
			ed.P[self.id] = measure
			self.params.server.receive(ed.packets[self.id])

	def send(self, ed):
		x = self.check(ed.ack[self.id])
		self.clear(ed.ack[self.id])
		return x

	def add(self, pkt):
		for channel, signal in pkt.s.items():
			self.S[channel]             += signal
			self.P[channel][pkt.ed.id]   = pkt
			self.G[pkt.freq][pkt.sf-7]  += pkt.load
			self.gm_                     = self.gm
			self.gm                      = np.mean([self.G[i][j-7] for i in self.params.freqSet for j in self.params.sfSet])
			self.tm                      = app.G2S(self.gm)

	def clear(self, pkt):
		for channel, signal in pkt.s.items():
			self.S[channel] 						-= signal
			self.P[channel].pop(pkt.ed.id)
			self.G[pkt.freq][pkt.sf-7]  -= pkt.load
			self.gm_                     = self.gm
			self.gm                      = np.mean([self.G[i][j-7] for i in self.params.freqSet for j in self.params.sfSet])
			self.tm                      = app.G2S(self.gm)

	def check(self, pkt):
		pkt.ok_ = pkt.ok
		for tmp in self.P[pkt.freq].values():
			if not tmp.lost:
				a1 							=  tmp.s[pkt.freq][tmp.sf - 7]
				a2 							= self.S[pkt.freq][tmp.sf - 7]
				w1 							= 1 + self.params.capture if self.params.capture !=0 else 1
				w2 							=     self.params.capture if self.params.capture !=0 else 1
				tmp.lost				= 1 if np.any(w1 * a1 < self.params.interaction[tmp.sf - 7] * a2) else tmp.lost
				tmp.collision		= 1 if w1 * a1 < w2 * a2 or a1 < a2 else tmp.collision
			tmp.ok						= 0 if tmp.lost or tmp.collision else tmp.ok
		if pkt.ok:
			return 1
		return 0

	def reload(self):
		self.P	     = {freq:{}               for freq in self.params.freqSet}
		self.S	     = {freq:np.zeros((6, 1)) for freq in self.params.freqSet}
		self.G	     = {freq:np.zeros((6, 1)) for freq in self.params.freqSet}
		self.gm      = 0
		self.tm      = 0
		self.tm_     = 0















#		self.T	     = {freq:np.zeros((6, 1)) for freq in self.params.freqSet}
#		self.TH      = list()
#		self.TH.append(self.T)
#		self.TM      = list()
#		self.TM.append(self.tm)
#		self.GH      = list()
#		self.GH.append(self.G)
#		self.GM      = list()
#		self.GM.append(self.gm)
		#		if np.all(np.sqrt(np.sum(np.square([(b.x, b.y) for b in bsDic.values()] - np.array([self.x,self.y]).reshape(1,2)), axis=1)) > params.range*1.5):

