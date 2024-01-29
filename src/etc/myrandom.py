import csv
import sys
import random
import math
import copy
import queue
import numpy as np

class Random():
	def __init__(self, params):
		self.params      =  params
		self.memberships =  params.cluster 

	def update(self, ed):
		ed.newaction	= np.random.choice(ed.actions, p=ed.randompolicy[ed.app])
		ed.newapp	= np.argmax(self.memberships[ed.newaction])

