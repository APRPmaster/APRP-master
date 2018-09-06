# dataset_main.py
# Simulates diffusion and trickle on a dataset

from dataset_graph_rep import *
from dataset_estimators import *
from utils import *
import time
import numpy as np


thetas = xrange(1,20,2)
check_ml = True

filename = 'data/bitcoin.gexf'

args = parse_arguments()

first_timestamp_only = 1

accuracies_first = []
accuracies_ml = []


APRPtrickle = (args.spreading == 0)

trickle = (args.spreading == 2)



# We used arbitrary spreading times that generally ensured that the message had spread long enough
spreading_time = 8
if trickle:
        G = DataGraphTrickle(filename, spreading_time = spreading_time)
elif APRPtrickle:
        G = DataGraphAPRPTrickle(filename, spreading_time = spreading_time)
	
	

# Dataset stats (comment out for actual runs)
# degrees = [G.degree(n) for n in G.nodes()]
# median_degree = np.median(degrees)
# print 'Median degree is', median_degree
# print 'mean degree is ', np.mean(degrees)
# print 'median degree is ', np.median(degrees)
# print 'histogram is ', np.histogram(degrees, bins = range(100))
# exit(0)

for theta in thetas:
	print 'On theta ', theta

	count_first = 0
	count_ml = 0
	for trial in range(args.trials):

		if (trial % 10) == 0:
			print 'On trial ', trial+1, ' out of ', args.trials

		
		source = random.choice(G.nodes())
	

		# Spread the message
		G.spread_message(source, first_timestamp_only = first_timestamp_only, num_corrupt_cnx = theta)

		# Estimate the source
		#if FIRST_timestamp in args.estimators:	
		est = FirstTimestampEstimator(G, source, args.verbose)
		result = est.estimate_source()
		acc = est.compute_accuracy(result)
		count_first += acc
		acc_fs = acc


	accuracies_first += [float(count_first) / args.trials]


print 'The first-timestamp estimator accuracy: ', accuracies_first
