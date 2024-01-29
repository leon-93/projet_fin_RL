import numpy 				as np
from   app           import app
from   net.packet 		import myPacket, myPacketAck
import queue
from etc import myrandom

class myED():
	def __init__(self, params):
		self.params				= params
		self.PP						= queue.Queue(20)
		self.H						= {tmp:myPacket for tmp in range(self.params.nrBS)}
		self.P						= {tmp:myPacket for tmp in range(self.params.nrBS)}

		self.setActions 	= [(params.freqSet[i], params.sfSet[j], params.powerSet[k], params.bwSet[l], params.crSet[m]) for i in range(len(params.freqSet)) for j in range(len(params.sfSet)) for k in range(len(params.powerSet)) for l in range(len(params.bwSet)) for m in range(len(params.crSet))]
		self.actions			= len(self.setActions)

		self.top          = {tmp:0 for tmp in range(self.params.nrPkt)}
		self.lastid				= 0
		self.ts 					= 0
		self.symboltime 	= 0
		self.minBS				= 0
		self.initial_sf   = 7
		self.model = myrandom.Random(self.params)

	def send(self, bsDict):
		for bsid, bs in bsDict.items():
			#if self.id == 0 and bsid == 0:
			#	print("Simulation ", self.params.i ,": ", self.params.nrBS, self.params.nrED, self.params.algo, self.params.ps, self.params.period_mn, self.packets[bsid].id)
			bs.add(self.packets[bsid].update(self.action))
		self.time = self.packets[bsid].toa
		return self.time

	def receive(self):
		ack = self.bestbs.send(self)
		if not ack:
			self.model.update(self)
		self.action			= self.newaction
		self.app				= self.newapp

	def reload(self):
		self.PP						= queue.Queue(20)
		self.H						= {tmp:myPacket for tmp in range(self.params.nrBS)}
		self.P						= {tmp:myPacket for tmp in range(self.params.nrBS)}
		self.reward				= np.zeros((self.actions, 3))
		self.weights			= np.ones (self.actions)
		self.randompolicy				= np.zeros((3, self.actions))
		for i in range(3):
			self.randompolicy[i]	= [1/self.actions for x in range(self.actions)]
		self.policy				= np.zeros((3, self.actions))
		for i in range(3):
			self.policy[i]	= [1/self.actions for x in range(self.actions)]
		self.app					= self.edapp
		self.newapp				= self.edapp
		self.sf  					= 7
		self.freq					= 868100
		self.ptx 					= 14
		self.bw  					= 125
		self.cr 					= 2
		self.fs						= 0.01
		self.ps2 					= 8
		self.ps3 					= 2
		self.hdr 					= True
		self.crc 					= True
		self.dist    			= {e.id:np.sqrt((e.x - self.x)**2 + (e.y - self.y)**2) for e in self.params.bsDict.values()}
		self.packets 			= {bsid:myPacket(bs, self, self.params) for bsid, bs in self.params.bsDict.items()}
		self.ack 					= {bsid:myPacketAck(bs, self, self.params) for bsid, bs in self.params.bsDict.items()}
		self.period				= self.params.period
		self.ps1 					= self.params.ps
		self.action				= np.random.choice(self.actions, p=self.policy[self.app])
		self.newaction		= self.action

		self.prx_mean		= 0
		self.toa_mean		= 0
		self.etx_mean		= 0
		self.ber_mean		= 0
		self.snr_mean		= 0
		self.dr_mean		= 0
		self.pdr_mean		= 0
		self.T_mean 		= 0
		self.G_mean 		= 0
		self.r_mean			= 0

		self.prx_mean_	= 0
		self.toa_mean_	= 0
		self.etx_mean_	= 0
		self.ber_mean_	= 0
		self.snr_mean_	= 0
		self.dr_mean_		= 0
		self.pdr_mean_	= 0
		self.T_mean_ 		= 0
		self.G_mean_ 		= 0
		self.r_mean_		= 0

		self.prx				= 0
		self.toa				= 0
		self.etx				= 0
		self.ber				= 0
		self.snr				= 0
		self.dr					= 0
		self.ok					= 0
		self.T 					= 0
		self.G 					= 0
		self.r					= 0

		self.prx_				= 0
		self.toa_				= 0
		self.etx_				= 0
		self.ber_				= 0
		self.snr_				= 0
		self.dr_				= 0
		self.ok_				= 0
		self.T_ 				= 0
		self.G_ 				= 0
		self.r_					= 0



