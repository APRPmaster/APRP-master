# dataset_estimators.py
import networkx as nx
import random
from sortedcontainers import SortedDict
import itertools
import math
import numpy as np
from utils import *

class Estimator(object):

	def  __init__(self, G, source, verbose = False):
		self.G = G
		self.verbose = verbose
		self.source = source

	def compute_accuracy(self, candidates):
		if self.source in candidates:
			return 1.0 / len(candidates)
		else:
			return 0.0	

class FirstTimestampEstimator(Estimator):

	def __init__(self, G, source, verbose = False, regular_degree = None):
		super(FirstTimestampEstimator, self).__init__(G, source, verbose)
		self.regular_degree = regular_degree

	def estimate_source(self):
		if self.verbose:
			print 'Edges: ', self.G.edges()
			# print 'Timestamps: ', self.G.adversary_timestamps
			print 'Receive Timestamps: ', self.G.received_timestamps

		if self.regular_degree:
			initial = [node for node in self.G.nodes() if self.G.degree(node) >= self.regular_degree and node in self.G.adversary_timestamps]
			min_ts_initial = min([self.G.adversary_timestamps[t] for t in initial])
			candidates = [node for node in initial
								if self.G.adversary_timestamps[node] == min_ts_initial]
		else:
			candidates = [node for node in self.G.adversary_timestamps.keys() 
								if self.G.adversary_timestamps[node] == min(self.G.adversary_timestamps.values())]
		
		# if self.verbose:
		print 'First timestamp candidates: ', [(candidate, self.G.adversary_timestamps[candidate]) for candidate in candidates]
 
		# # For lower bound in Sigemtrics submission, uncomment the next two lines
		# if len(candidates) > 1:
		# 	candidates = []

		return candidates
