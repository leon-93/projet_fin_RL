#!/usr/bin/env python
import numpy	as np
import math
import copy
from   app import app, qos

class myPacket():
	def __init__(self, bs, ed ,params):
		self.params			= params
		self.ed					= ed
		self.bs					= bs
		self.ps1				= self.params.ps
		self.ps2 				= ed.ps2
		self.ps3 				= ed.ps3
		self.hdr 				= ed.hdr
		self.crc 				= ed.crc
		self.id					= -1
		self.r					= 0
		self.dist				= ed.dist[bs.id]
		self.fs 				= 5
		self.prx				= 0
		self.s					= 0
		self.toa				= 0
		self.etx				= 0
		self.snr				= 0
		self.ber				= 0
		self.dr					= 0
		self.load				= 0
		self.G					= 0
		self.T					= 0

	def update(self, action):
		self.time 			= self.params.env.now/3600000
		self.id				 += 1
		self.lost				= 0
		self.collision	= 0
		self.ok					= 1
		self.app 				= self.ed.app
		self.action			= self.ed.action
		self.ed.freq, self.ed.sf, self.ed.ptx	, self.ed.bw	, self.ed.cr		= self.ed.setActions[action]
		self.freq   , self.sf   , self.ptx		, self.bw			, self.cr 			= self.ed.setActions[action]

		self.prx_				= self.prx
		self.s_					= self.s
		self.toa_				= self.toa
		self.etx_				= self.etx
		self.snr_				= self.snr
		self.ber_				= self.ber
		self.dr_				= self.dr
		self.load_			= self.load

		self.prx				= qos.getPRX(self)
		self.s					= qos.getRSSI(self)
		self.toa				= qos.getToA(self)
		self.etx				= qos.getEnergy(self)
		self.snr				= qos.getSNR(self)
		self.ber				= qos.getBER(self)
		self.dr					= qos.getDR(self)
		self.load				= qos.getG(self)
		return self

	def update2(self, action):
		self.time 			= self.params.env.now/3600000
		self.id				 += 1
		self.lost				= 0
		self.collision	= 0
		self.ok					= 1
		self.app 				= self.ed.app
		self.action			= self.ed.action
		self.ed.freq, self.ed.sf, self.ed.ptx	, self.ed.bw	, self.ed.cr		= self.ed.setActions[action]
		self.freq   , self.sf   , self.ptx		, self.bw			, self.cr 			= self.ed.setActions[action]
		
		msgRx	      		= app.randomE(self.ps1, self.sf)
		msgTx	      		= modulation.css_rx(self.sf, self.bw, self.fs, self.ps2, self.ps3, modulation.css_tx(self.sf, self.bw, self.fs, self.ps2, self.ps3, msgRx))
		
		self.prx				= qos.getPRX(self)
		self.s					= qos.getRSSI(self)
		self.toa				= qos.getToA(self)
		self.etx				= qos.getEnergy(self)
		self.snr				= qos.getSNR(self)
		self.ber				= sum(sum(abs(msgRx-msgTx))) / (self.ps1 * self.sf)
		self.dr					= qos.getDR(self)
		self.load				= qos.getG(self)
		return self

	def measure(self):
#		print(self.bs.tm_, self.bs.tm, self.ok)
		self.G_					= self.G
		self.T_					= self.T
		self.G					= self.bs.gm
		self.T					= self.bs.tm
		self.policy			= self.ed.policy

		self.prx_mean		= np.mean([self.prx		, self.ed.prx_mean]) 	if self.id !=0 and self.id !=1 else self.prx
		self.toa_mean		= np.mean([self.toa		, self.ed.toa_mean]) 	if self.id !=0 and self.id !=1 else self.toa
		self.etx_mean		= np.mean([self.etx		, self.ed.etx_mean]) 	if self.id !=0 and self.id !=1 else self.etx
		self.ber_mean		= np.mean([self.ber		, self.ed.ber_mean]) 	if self.id !=0 and self.id !=1 else self.ber
		self.snr_mean		= np.mean([self.snr		, self.ed.snr_mean]) 	if self.id !=0 and self.id !=1 else self.snr
		self.dr_mean		= np.mean([self.dr		, self.ed.dr_mean ]) 	if self.id !=0 and self.id !=1 else self.dr
		self.pdr_mean		= np.mean([self.ok 		, self.ed.pdr_mean]) 	if self.id !=0 and self.id !=1 else self.ok
		self.T_mean 		= np.mean([self.T 		, self.ed.T_mean  ]) 	if self.id !=0 and self.id !=1 else self.T
		self.G_mean 		= np.mean([self.G 		, self.ed.G_mean  ]) 	if self.id !=0 and self.id !=1 else self.G
		self.r					= self.params.objective(self)
		self.r_mean			= np.mean([self.r			, self.ed.r_mean	]) 	if self.id !=0 and self.id !=1 else self.r

		return copy.copy(self)


class myPacketAck():
	def __init__(self, bs, ed ,params):
		self.params			= params
		self.ed					= ed
		self.bs					= bs
		self.ps1				= 5
		self.ps2 				= ed.ps2
		self.ps3 				= ed.ps3
		self.hdr 				= ed.hdr
		self.crc 				= ed.crc
		self.id					= -1
		self.r					= 0
		self.dist				= ed.dist[bs.id]

	def update(self, action):
		self.time 			= self.params.env.now/3600000
		self.id				 += 1
		self.lost				= 0
		self.collision	= 0
		self.ok					= 1
		self.app 				= self.ed.app
		self.action			= self.ed.action
		self.ed.freq, self.ed.sf, self.ed.ptx	, self.ed.bw	, self.ed.cr		= self.ed.setActions[action]
		self.freq   , self.sf   , self.ptx		, self.bw			, self.cr 			= self.ed.setActions[action]
		self.prx				= qos.getPRX(self)
		self.s					= qos.getRSSI(self)
		self.toa				= qos.getToA(self)
		self.etx				= qos.getEnergy(self)
		self.snr				= qos.getSNR(self)
		self.ber				= qos.getBER(self)
		self.dr					= qos.getDR(self)
		self.load				= qos.getG(self)
		return self

	def measure(self):
		self.G_					= self.G
		self.T_					= self.T
		self.G					= self.bs.gm
		self.T					= self.bs.tm
		self.policy			= self.ed.policy

		self.prx_mean		= np.mean([self.prx		, self.ed.prx_mean]) 	if self.id !=0 and self.id !=1 else self.prx
		self.toa_mean		= np.mean([self.toa		, self.ed.toa_mean]) 	if self.id !=0 and self.id !=1 else self.toa
		self.etx_mean		= np.mean([self.etx		, self.ed.etx_mean]) 	if self.id !=0 and self.id !=1 else self.etx
		self.ber_mean		= np.mean([self.ber		, self.ed.ber_mean]) 	if self.id !=0 and self.id !=1 else self.ber
		self.snr_mean		= np.mean([self.snr		, self.ed.snr_mean]) 	if self.id !=0 and self.id !=1 else self.snr
		self.dr_mean		= np.mean([self.dr		, self.ed.dr_mean ]) 	if self.id !=0 and self.id !=1 else self.dr
		self.pdr_mean		= np.mean([self.ok 		, self.ed.pdr_mean]) 	if self.id !=0 and self.id !=1 else self.ok
		self.T_mean 		= np.mean([self.T 		, self.ed.T_mean  ]) 	if self.id !=0 and self.id !=1 else self.T
		self.G_mean 		= np.mean([self.G 		, self.ed.G_mean  ]) 	if self.id !=0 and self.id !=1 else self.G
		self.r					= self.params.objective(self)
		self.r_mean			= np.mean([self.r			, self.ed.r_mean	]) 	if self.id !=0 and self.id !=1 else self.r

		return copy.copy(self)


