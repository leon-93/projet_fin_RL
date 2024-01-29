#!/usr/bin/env python
import numpy as np
import math
import random
import os
import copy
from   random import randint
from   os.path import join, exists
from   os import makedirs
from   net.gateway	import myBS
from   net.device	import myED
from   app				import app, qos
from   net.server	import myServer

def createBS(params, grid):
	xRange   = [grid[0]*0.1, grid[0]*0.9]
	yRange   = [grid[1]*0.1, grid[1]*0.9]
	bsDic    = {}
	tools.createFile(params.topopath+str(params.nrBS)+"_"+str(params.nrED)+"_bs.csv", "ID, X, Y")
	for n in range(params.nrBS):
		bs         = myBS(params)
		bs.id      = n
		bs.x       = random.uniform(xRange[0], xRange[1]) if params.nrBS != 1 else grid[0]*0.5
		bs.y       = random.uniform(yRange[0], yRange[1]) if params.nrBS != 1 else grid[1]*0.5
		bsDic[bs.id] = bs
		tools.writeLine(params.topopath+str(params.nrBS)+"_"+str(params.nrED)+"_bs.csv", logs.logBSpositions(bs))
		if params.nrBS == 1:
			tools.writeLine(params.topopath+str(params.nrBS)+"_"+str(params.nrED)+"_bs.csv", logs.logBSpositions(bs))
	return bsDic

def createED(params, bsDict, grid):
	distMatrix  = qos.getMaxTransmitDistance(params, (1, 90, 8, 4.25, False, True))
	edDict      = {}
	xRange    	= [0, grid[0]]
	yRange    	= [0, grid[1]]
	temp 	  	  = 0
	tools.createFile(params.topopath+str(params.nrBS)+"_"+str(params.nrED)+"_ed.csv", "ID, APP, DR, X, Y")
	for idx in range(len(params.distribution)):
		number_nodes = int(params.nrED * params.distribution[idx])
		for n in range(number_nodes):
			while True:
				x   = random.uniform(xRange[0], xRange[1])
				y   = random.uniform(yRange[0], yRange[1])
				tmp = np.sum(np.square([(bs.x, bs.y) for bs in bsDict.values()] - np.array([x,y]).reshape(1,2)), axis=1)
				if np.any(tmp <= params.range**2) and np.any(tmp <= distMatrix[idx]**2):
					ed				= myED(params)
					ed.id  			= n+temp
					ed.drx			= (5-idx)
					ed.x   			= x
					ed.y   			= y
					ed.edapp		= randint(0, 2)
					edDict[ed.id] 	= ed
					tools.writeLine(params.topopath+str(params.nrBS)+"_"+str(params.nrED)+"_ed.csv", logs.logEDpositions(ed))
					break
		temp += number_nodes
	#plot_Locations(bsDict, edDict, grid[0], grid[1], distMatrix)
	return edDict


def getBS(params):
	bsDict          = {}
	df              = np.genfromtxt(params.topopath+str(params.nrBS)+"_"+str(params.nrED)+"_bs.csv", delimiter=",", dtype="float", skip_header=1)          # load the CSV file as a numpy matrix
	for n in range(params.nrBS):
		bs            = myBS(params)
		bs.id         = df[n][0].astype(int)
		bs.x          = df[n][1]
		bs.y          = df[n][2]
		bsDict[bs.id] = bs
	return bsDict

def getED(params):
	edDict          = {}
	df              = np.genfromtxt(params.topopath+str(params.nrBS)+"_"+str(params.nrED)+"_ed.csv", delimiter=",", dtype="float", skip_header=1)          # load the CSV file as a numpy matrix
	for n in range(params.nrED):
		ed            = myED(params)
		ed.id         = df[n][0].astype(int)
		ed.edapp      = df[n][1].astype(int)
		ed.drx        = df[n][2].astype(int)
		ed.x          = df[n][3]
		ed.y          = df[n][4]
		edDict[ed.id] = ed
	return edDict

def createNetwork(params):
#	params.grid			= params.range * params.nrBS
#	grid				= [params.grid, params.grid]
#	params.bsDict		= createBS(params, grid)
#	params.edDict		= createED(params, params.bsDict, grid)
	params.bsDict		= getBS(params)
	params.edDict		= getED(params)
	params.server		= myServer(params)
	params.capture, params.interaction              = qos.getInteractionMatrix(True, True)
	params.snrx     = [-20,-17.5,-15,-12.5,-10,-7.5]
	params.drx      = [0.25,0.44,0.98,1.76,3.125,5.47]



