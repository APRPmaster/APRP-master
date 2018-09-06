# data_graph_rep.py
# contains the classes for storing and processing spreading on a data-provided graph

import networkx as nx
import random
import codecs
# import matplotlib.pyplot as plt
import numpy as np


class DataGraph(nx.Graph):

        def __init__(self, filename, spreading_time = None, lambda1 = 1):
                super(DataGraph, self).__init__(nx.read_gexf(filename))
                self.lambda1 = lambda1 # spreading rate over the diffusion graph
                
                
                # Read graph and label nodes from 1 to N
                mapping = {}
                for (idx, node) in zip(range(nx.number_of_nodes(self)), self.nodes()):
                        mapping[node] = idx
                nx.relabel_nodes(self, mapping, copy=False)

                self.spreading_time = spreading_time




class DataGraphAPRPTrickle(DataGraph):

        def __init__(self, filename, spreading_time = None):
                ''' NB: Here the spreading_time is actually the number of rings of the graph to infect'''
                super(DataGraphAPRPTrickle, self).__init__(filename, spreading_time)        
                

                
        def spread_message(self, source = 0, first_timestamp_only = False, num_corrupt_cnx = 1):
                '''first_timestamp_only denotes whether this diffusion spread will only be used
                to measure the first timestamp adversary. In that case, some time-saving optimizations
                can be implemented. Most of the time, this flag will be set to false.'''
                
                count = 0
                self.source = source

                adversaries = [-(i+1) for i in range(num_corrupt_cnx)]

                # Empty the observed timestamps
                self.adversary_timestamps = {}          # dictionary of adversary report time indexed by node
                self.received_timestamps = {}           # dictionary of message receipt time indexed by node

                # Initialize the process
                self.received_timestamps[self.source] = 0
                self.active = [source]
                self.infected = [source]

                stopping_time = self.spreading_time
                

                while self.active and count < stopping_time:
                        count += 1
                        # cycle through the active nodes, and spread with an exponential clock
                        for node in self.active:

                                uninfected_neighbors = [neighbor for neighbor in self.neighbors(node) if neighbor not in self.infected]

                                node_degree=dict()
                                for nnn in uninfected_neighbors:
                                        node_degree[nnn]=self.degree(nnn)+num_corrupt_cnx
                                for nnn in adversaries:
                                        node_degree[nnn]=10*num_corrupt_cnx
                                node_d_list=node_degree.items()
                                uninfected_neighbors_degree=sorted(node_d_list, key=lambda e:e[1], reverse=False)
                                ordering=[]
                                for order_node in uninfected_neighbors_degree:
                                        ordering+=[order_node[0]]
                                uninfected_neighbors += adversaries

                                # print 'ordering', ordering
                                signs = [item >= 0 for item in ordering]
                                # print 'signs', signs

                                # find the reporting time for node
                                self.adversary_timestamps[node] = signs.index(False) + 1 + self.received_timestamps[node]

                                if first_timestamp_only and (node == source):
                                        stopping_time = min(stopping_time, self.adversary_timestamps[node])
                                        # print 'stopping_time', stopping_time

                                # assign the received timestamps for the other nodes
                                for idx in range(len(ordering)):
                                        neighbor = ordering[idx]
                                        # if the node at time slot t is not a spy
                                        if neighbor >= 0:
                                                rx_timestamp = self.received_timestamps[node] + 1 + idx
                                                self.received_timestamps[neighbor] = rx_timestamp
                                                self.infected.append(neighbor)
                                                if rx_timestamp < stopping_time:
                                                        self.active.append(neighbor)
                                self.active.remove(node)
                                
class DataGraphTrickle(DataGraph):

	def __init__(self, filename, spreading_time = None):
		''' NB: Here the spreading_time	is actually the number of rings of the graph to infect'''
		super(DataGraphTrickle, self).__init__(filename, spreading_time)	
		

		
	def spread_message(self, source = 0, first_timestamp_only = False, num_corrupt_cnx = 1):
		
		count = 0
		self.source = source

		adversaries = [-(i+1) for i in range(num_corrupt_cnx)]

		# Empty the observed timestamps
		self.adversary_timestamps = {} 		# dictionary of adversary report time indexed by node
		self.received_timestamps = {}		# dictionary of message receipt time indexed by node

		# Initialize the process
		self.received_timestamps[self.source] = 0
		self.active = [source]
		self.infected = [source]

		stopping_time = self.spreading_time
		

		while self.active and count < stopping_time:
			count += 1
			# cycle through the active nodes, and spread with an exponential clock
			for node in self.active:

				uninfected_neighbors = [neighbor for neighbor in self.neighbors(node) if neighbor not in self.infected]
				uninfected_neighbors += adversaries
				# print 'uninfected_neighbors', uninfected_neighbors, adversaries

				# random permutation of neighbors
				ordering = list(np.random.permutation(uninfected_neighbors))
				# print 'ordering', ordering
				signs = [item >= 0 for item in ordering]
				# print 'signs', signs

				# find the reporting time for node
				self.adversary_timestamps[node] = signs.index(False) + 1 + self.received_timestamps[node]

				if first_timestamp_only and (node == source):
					stopping_time = min(stopping_time, self.adversary_timestamps[node])
					# print 'stopping_time', stopping_time

				# assign the received timestamps for the other nodes
				for idx in range(len(ordering)):
					neighbor = ordering[idx]
					# if the node at time slot t is not a spy
					if neighbor >= 0:
						rx_timestamp = self.received_timestamps[node] + 1 + idx
						self.received_timestamps[neighbor] = rx_timestamp
						self.infected.append(neighbor)
						if rx_timestamp < stopping_time:
							self.active.append(neighbor)
				self.active.remove(node)
