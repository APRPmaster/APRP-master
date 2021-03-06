# utils.py
import argparse


# Estimator Constants
FIRST_TIMESTAMP = 0
MAX_LIKELIHOOD = 1

# Graph constraints
SWEEP_THETA = 1
SWEEP_D = 0


def write_results(results_names, results_data, param_types, params, run_num = None):
	''' Writes a file containing the parameters, then prints each
	result name with the corresponding data '''

	filename = 'results/results' + "_".join([str(i) for i in params[0]])

	if not (run_num is None):
		filename += '_run' + str(run_num)


	f = open(filename, 'w')

	for (param_type, param) in zip(param_types, params):
		f.write(param_type)
		f.write(': ')
		for item in param:
		  f.write("%s " % item)		
		f.write('\n')

	for (result_type, result) in zip(results_names, results_data):
		f.write(result_type)
		f.write('\n')

		for item in result:
		  f.write("%s " % item)
	  	f.write('\n')

	f.close()

def parse_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument("-r", "--run", type=int,
	                    help="changes the filename of saved data")
	parser.add_argument("-v", "--verbose", help="increase output verbosity",
	                    action="store_true")
	parser.add_argument("-w", "--write", help="writes the results to file",
	                    action="store_true")
	parser.add_argument("-t","--trials", type=int, help="number of trials",
						default=1)
	parser.add_argument("-s","--spreading", type=int, help="Which spreading protocol to use (0)APRPtrickle, (1)APRPdiffusion, (2)trickle, (3)diffusion",
						default=0)
	parser.add_argument("-e","--estimator", default=0, type=int, 
						help="Which estimator to use (0)first-timestamp, (1)ML")
	parser.add_argument("--measure_time", help="measure runtime?",
						action="store_true")
	parser.add_argument("-d", "--degree", type=int, help="fixed degree of tree", default=0)
	parser.add_argument("-q", "--theta", help="sweep theta?", action="store_true")
	args = parser.parse_args()

	if not (args.run is None):
		args.write = True

	print '---Selected Parameters---'
	print 'verbose: ', args.verbose
	print 'write to file: ', args.write
	print 'spreading mechanism: ', args.spreading
	print 'estimator: ', args.estimator
	print 'run: ', args.run
	print 'num trials: ', args.trials, '\n'
	return args
