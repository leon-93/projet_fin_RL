import numpy as np
import math
import scipy.stats as stats
from   app.app import dBmTomW, dBmTonW

# DR
def getDR(pkt):
	return (pkt.sf*(pkt.bw/2**pkt.sf)*(4/(3+pkt.cr))) #/ed.ps1

# SNR
def getSNR(pkt):
	return pkt.prx  +174 - 10*math.log10(pkt.bw*1000) - 6

# PTX
def getPTX(pRX, distance, params):
	return pkt.prx + pkt.params.Lpld0 + 10.0 * pkt.params.gamma * np.log10(pkt.dist/pkt.params.d0)
def getEnergy(pkt):
	return 1000*pkt.toa * dBmTomW(pkt.ptx) * (3.0) /1e6 # V = 3.0	 # voltage

# BER
def getBER_reynders(eb_no, sf): # packet error model assumming independent Bernoulli	 """Given the energy per bit to noise ratio (in db), compute the bit error for the SF"""
	return stats.norm.sf(math.log(sf, 12)/math.sqrt(2)*eb_no)
def getBER_reynders_snr(snr, sf, bw, cr): #	 """Compute the bit error given the SNR (db) and SF"""
	Temp  = [4.0/5,4.0/6,4.0/7,4.0/8]
	CR    = Temp[cr-1]
	BW    = bw*1000.0
	eb_no =  snr - 10*math.log10(BW/2**sf) - 10*math.log10(sf) - 10*math.log10(CR) + 10*math.log10(BW)
	return getBER_reynders(eb_no, sf)
def getBER(pkt):
	return 1 - (1 - getBER_reynders_snr(pkt.snr, pkt.sf, pkt.bw*1000, pkt.cr))**(pkt.ps1*8) #	snr = rssi  +174 - 10*math.log10(ed.bw*1000) - 6
def getBER_(pkt):
	return sum(sum(abs(pkt.msgRx - pkt.msgTx))) / (pkt.ps1 * pkt.sf)

# ToA
def getToA_(sf, cr, bw, pl, preambleLength, syncLength, H, crc):
	DE            = 1 if bw == 125 and sf in [11, 12] else 0
	H             = 1 if sf == 6 else H
	Tsym          = (2.0 ** sf) / bw
	Tpream        = (preambleLength + syncLength) * Tsym
	payloadSymbNB = 8 + max(math.ceil((8.0 * pl - 4.0 * sf + 28 + 16 - 20 * H) / (4.0 * (sf - 2 * DE))) * (cr + 4), 0)
	Tpayload      = payloadSymbNB * Tsym
	return (Tpream + Tpayload)
def getToA(pkt): #	dr            = obj.dc/toa
	return getToA_(pkt.sf, pkt.cr, pkt.bw, pkt.ps1, pkt.ps2, pkt.ps3, pkt.hdr, pkt.crc)

# RSSI
def getPRX(pkt): 
	return pkt.ptx - pkt.params.GL - pkt.params.Lpld0 - 10.0 * pkt.params.gamma * np.log10(pkt.dist/pkt.params.d0) #rssi = -174 + 10 * np.log10(BW[bw]) + NF + SNR_dB[snr]
def getRSSI(pkt):
	signal          = np.zeros((6, 1))
	signal[pkt.sf - 7]  = dBmTonW(pkt.prx)
	signalLevel     = {pkt.freq: signal}
	signalLevel     = {x: signalLevel[x] for x in signalLevel.keys() & pkt.bs.S.keys()}
	return signalLevel

# G
def getG(pkt):
#	return pkt.dr * pkt.toa/1000 
	return ((1/(pkt.params.period_mn*60)) * (pkt.toa/100)) #+ ((1/300) * 1)

def getInteractionMatrix(captureEffect, interSFInterference):
	# The spreading factor interaction matrix derived from lab tests and Semtech documentation SFs are not perfectly orthogonal: a signal at SF_m faces interferences from all signals on other SFs
	if interSFInterference == True:
		capture= dBmTomW(6) if captureEffect == True else 0#  dB capturEffect threashold
		interactionMatrix = np.array([
			[capture,		dBmTomW(-7.5),  dBmTomW(-7.5), dBmTomW(-7.5),  dBmTomW(-7.5),  dBmTomW(-7.5)],
			[dBmTomW(-9),	capture,		dBmTomW(-9),   dBmTomW(-9),	dBmTomW(-9),	dBmTomW(-9)],
			[dBmTomW(-13.5), dBmTomW(-13.5), capture,	   dBmTomW(-13.5), dBmTomW(-13.5), dBmTomW(-13.5)],
			[dBmTomW(-15),   dBmTomW(-15),   dBmTomW(-15),  capture,		dBmTomW(-15),   dBmTomW(-15)],
			[dBmTomW(-18),   dBmTomW(-18),   dBmTomW(-18),  dBmTomW(-18),   capture,		dBmTomW(-18)],
			[dBmTomW(-22.5), dBmTomW(-22.5), dBmTomW(-22.5),dBmTomW(-22.5), dBmTomW(-22.5), capture]])
	else:
		capture= dBmTomW(6) if captureEffect == True else  1#  dB
		interactionMatrix = np.array([
			[capture,	0,		  0,			 0,		  0,		  0		 ],
			[0,		  capture   , 0,			 0,		  0,		  0		 ],
			[0,		  0		 , capture,	   0,		  0,		  0		 ],
			[0,		  0		 , 0,			 capture,	0,		  0		 ],
			[0,		  0		 , 0,			 0,		  capture,	0		 ],
			[0,		  0		 , 0,			 0,		  0,		  capture]])
	return capture, interactionMatrix


def getSensi():
	# sensitivity
	sf7  = np.array([7, -123.0,-121.5,-118.5])
	sf8  = np.array([8, -126.0,-124.0,-121.0])
	sf9  = np.array([9, -129.5,-126.5,-123.5])
	sf10 = np.array([10,-132.0,-129.0,-126.0])
	sf11 = np.array([11,-134.5,-131.5,-128.5])
	sf12 = np.array([12,-137.0,-134.0,-131.0])
	return np.array([sf7,sf8,sf9,sf10,sf11,sf12]) # array of sensitivity values

def getMaxTransmitDistance(params, phyParams):
#	obj.maxdist			= getDistanceFromPower(self.pTXmax, params.interferenceThreshold, params.logDistParams)
	maxPtx = max(params.powerSet)
	cr, packetLength, headerEnable, preambleLength, syncLength, crc = phyParams
	PTx125				= min(maxPtx,14) # in dBm
	PTx250				= min(maxPtx,14) # in dBm
	Lpl125				= PTx125 - getSensi()[:,1]
	Lpl250				= PTx250 - getSensi()[:,2]
	LplMatrix			= np.concatenate((Lpl125.reshape((6,1)), Lpl250.reshape((6,1))), axis=1)
	distMatrix			= np.dot(params.d0, np.power(10, np.divide(LplMatrix - params.Lpld0, 10*params.gamma)))
	packetAirtimeValid 	= np.zeros((6,2))
	for i in range(6):
		# set packet airtime valid <= 400
		packetAirtimeValid[i,0] = (getToA_(i+7, cr, 125, packetLength, preambleLength, syncLength, headerEnable, crc) <= 9999)
		packetAirtimeValid[i,1] = (getToA_(i+7, cr, 250, packetLength, preambleLength, syncLength, headerEnable, crc) <= 9999)
	Index = np.argmax(np.multiply(distMatrix, packetAirtimeValid))
	sfInd, bwInd = np.unravel_index(Index, (6,2))
	if packetAirtimeValid[sfInd, bwInd] == 0:
		raise ValueError("Packet length too large!")
	maxSF = sfInd + 7
	maxBW = 125 if bwInd == 0 else 250
	print ("\tMax range = {} at SF = {}, BW = {}".format(distMatrix[sfInd,bwInd], maxSF, maxBW))
	return distMatrix[:, bwInd] #, distMatrix[sfInd,bwInd], maxSF, maxBW

