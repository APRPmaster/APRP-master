# main.py
# Simulates APRP diffusion, APRP trickle, diffusion and trickle on a regular tree
# Can check ML estimator and/or first-timestamp estimators

from graph_rep import *
from estimators import *
from utils import *
import time

if __name__ == "__main__":

	args = parse_arguments()

	if args.degree == SWEEP_D:

		degrees = [2,3,4,5,6] # range of regular tree degrees to test
	else:
		degrees = [4] 
	
	if args.theta == SWEEP_THETA:
		thetas = xrange(1,20,2)
	else:
		thetas = [1]  # number of connections to the eavesdropper per node
	

	print 'degrees', degrees, 'thetas', thetas

	check_ml = (args.estimator == MAX_LIKELIHOOD) 
	
	APRPtrickle = (args.spreading == 0)
	APRPdiffusion = (args.spreading == 1)
        trickle = (args.spreading == 2)
	diffusion = (args.spreading == 3)

	accuracies_first = []
	accuracies_first_diff = []
	accuracies_ml = []
	accuracies_rc = []
	accuracies_cone = []
	accuracies_neighbor_cone = []

	if args.measure_time:
		start = time.time()
		end = start


	# cnt = 0
	for degree in degrees:
		for theta in thetas:
			# Set the spreading time
			if trickle or APRPtrickle:
				# We limit the spreading time to degree + 1 for efficiency
				# 	if the first timestamp estimator succeeds, it will always do 
				#	so by this time
				spreading_time = degree + 1
			else:
				spreading_time = 2

			print 'On degree ', degree
			print 'On theta', theta

			count_first = 0
			count_first_diff = 0
			count_ml = 0
			count_rc = 0
			count_cone = 0
			count_neighbor_cone = 0

			for i in range(args.trials):
				if (i % 100) == 0:
					print 'On trial ', i+1, ' out of ', args.trials

				if APRPtrickle:
					# Trickle trials
					G = RegularTreeAPRPTrickle(degree,spreading_time, theta = theta)
					G.spread_message(first_timestamp_only = (not check_ml))
					
					# First Timestamp estimator
					est_first = FirstTimestampEstimator(G)
					result_first = est_first.estimate_source()
					acc_first = est_first.compute_accuracy(G.source, result_first)
					count_first += acc_first

					if check_ml:
						# ML estimator general
						est_ml = MLEstimatorMP(G, args.verbose)
						result_ml = est_ml.estimate_source()
						acc_ml = est_ml.compute_accuracy(G.source, result_ml)
						count_ml += acc_ml

				if APRPdiffusion:
					# Diffusion trials
					G = RegularTreeAPRPDiffusion(degree, spreading_time, theta=theta)
					G.spread_message(first_timestamp_only = (not check_ml))


					# First timestamp estimator
					est_first = FirstTimestampEstimator(G, args.verbose)
					result_first = est_first.estimate_source()
					acc_first = est_first.compute_accuracy(G.source, result_first)
					count_first += acc_first

					if check_ml:
						# Reporting centrality estimator
						est_ml = ReportingCentralityEstimator(G, args.verbose)
						result_ml = est_ml.estimate_source()
						acc_ml = est_ml.compute_accuracy(G.source, result_ml)
						count_ml += acc_ml
				if trickle:
					# Trickle trials
					G = RegularTreeTrickle(degree,spreading_time, theta = theta)
					G.spread_message(first_timestamp_only = (not check_ml))
					
					# First  estimator
					est_first = FirstTimestampEstimator(G)
					result_first = est_first.estimate_source()
					acc_first = est_first.compute_accuracy(G.source, result_first)
					count_first += acc_first

					if check_ml:
						# ML estimator general
						est_ml = MLEstimatorMP(G, args.verbose)
						result_ml = est_ml.estimate_source()
						acc_ml = est_ml.compute_accuracy(G.source, result_ml)
						count_ml += acc_ml

				if diffusion:
					# Diffusion trials
					G = RegularTreeDiffusion(degree, spreading_time, theta=theta)
					G.spread_message(first_timestamp_only = (not check_ml))


					# First timestamp estimator
					est_first = FirstTimestampEstimator(G, args.verbose)
					result_first = est_first.estimate_source()
					acc_first = est_first.compute_accuracy(G.source, result_first)
					count_first += acc_first

					if check_ml:
						# Reporting centrality estimator
						est_ml = ReportingCentralityEstimator(G, args.verbose)
						result_ml = est_ml.estimate_source()
						acc_ml = est_ml.compute_accuracy(G.source, result_ml)
						count_ml += acc_ml


			accuracies_first += [float(count_first) / args.trials]
			accuracies_ml += [float(count_ml) / args.trials]
			
			if args.verbose:
				print 'Accuracies, FT:', accuracies_first
				print 'Accuracies, ML:', accuracies_ml
			
			if args.write:
				result_types = ['FT accuracy', 'ML accuracy']
				param_types = ['degrees']
				results = [[accuracies_first], [accuracies_ml]]
				params = [[i for i in degrees]]
				write_results(result_types, results, param_types, params, args.run)
        if not check_ml:
                print 'The FT estimator accuracy: ', accuracies_first
        else:
                print 'The ML estimator accuracy: ', accuracies_ml
	
	if args.measure_time:
		end = time.time()
		print 'The runtime is ', end-start
