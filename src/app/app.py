#!/usr/bin/env python

import numpy as np
import os
import shutil

def creatDir(path):
	if os.path.exists(path):
		shutil.rmtree(path)
	try:
		os.makedirs(path)
	except OSError:
		print ("error")

def createFile(path, line, erase=True):
	if erase or not erase and not os.path.exists(path):
		with open(path, "w") as hisfile:
			hisfile.write(line)
		hisfile.close()

def writeLine(path, line):
	with open(path, "a") as hisfile:
		hisfile.write(line)
	hisfile.close()

def files(logdir, exp_name):
	if not os.path.exists(logdir):
		os.makedirs(logdir)
	simu_dir	= join(logdir, exp_name)
	if not os.path.exists(simu_dir):
		os.makedirs(simu_dir)
	return simu_dir



def flatten(input):
    new_list = []
    for i in input:
        for j in i:
            new_list.append(j)
    return new_list

def randomE(payload, SF=8):
    total_sym           = SF * payload # total bits to be transmitted in LoRa message
    rows                = SF
    columns             = np.ceil(total_sym / SF)
    random_number_input = np.round(0.75 * np.random.uniform(0,1,size=int(rows * columns))).astype(int)
    msg                 = np.reshape(random_number_input, (-1, SF))
    return msg #, columns

def randomA(payload, SF=8):
    total_sym           = SF * payload # total bits to be transmitted in LoRa message
    rows                = SF
    columns             = np.ceil(total_sym / SF)
    random_number_input = np.round(0.75 * np.random.uniform(0,1,size=int(rows * columns))).astype(int)
    msg                 = np.reshape(random_number_input, (-1, SF))
    return random_number_input #, columns


def G2S(G):
	return G * np.exp(-2 * G)

def dBmTomW(pdBm):
	pmW = 10.0**(pdBm/10.0)
	return pmW

def dBmTonW(pdBm):
	#pfW = 10 ** ((pdBm + 90.0) / 10.0)
	#pmW = 10 ** (pdBm / 10.0)
	pnW = 10.0**((pdBm+90.0)/10.0)
	return pnW

def guards(skewrate):
	gs = [0 for i in PcktLength_SF]
	for sf in range(0,6):
		gs[sf] = math.ceil(1000*skewrate*airtime(sf+7,CodingRate,PcktLength_SF[sf]+LorawanHeader,Bandwidth)*(max(SFdistribution[sf],1.0/Dutycycle)*math.ceil(datasize/(ChanlperSF[sf]*PcktLength_SF[sf]))+(ChanlperSF[sf]-1))) # msec
	return gs

def getDistanceFromPL(pLoss, logDistParams):
	gamma, Lpld0, d0 = logDistParams
	d = d0*(10.0**((pLoss-Lpld0)/(10.0*gamma)))
	return d

def getDistanceFromPL2(pTX, pRX):
	d = d0 * (10 ** ((pTX - pRX - Lpld0) / (10.0 * gamma)))
	return d

def getDistanceFromPower(pTX, pRX, logDistParams):
	return getDistanceFromPL(pTX - pRX, logDistParams)


def local_peaks_indexes(P):
	P_vec = np.array(P)
	p = []
	for i in range(1, len(P_vec)):
		if P_vec[i] > P_vec[i-1]:
			p.append(i)
	p.append(6)
	return p

#import matplotlib.pyplot as plt
#from   seaborn import scatterplot  as scatter
#import mpl_toolkits.mplot3d.axes3d as p3
#from itertools import cycle, islice


