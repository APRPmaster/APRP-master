# Bitcoin-APRP
Simulate and test the performance of anonymous algorithm APRP, for reproducing the plots from "APRP: An Anonymous Propagation Method in Bitcoin Network".


The two relevant files to run are main.py (for regular tree simulations) and dataset_main.py (for simulations on a real Bitcoin graph topology). Both files take the same input arguments, which are listed below:

	```
	"-r", "--run", type=int, help="changes the filename of saved data"
	"-v", "--verbose", help="increase output verbosity", action="store_true"
	"-w", "--write", help="writes the results to file", action="store_true"
	"-t","--trials", type=int, help="number of trials", default=1
	"-s","--spreading", type=int, help="Which spreading protocol to use (0)APRP trickle, (1)APRP diffusion",(2)APRP trickle, (3)APRP diffusion", default=0
	"-e","--estimator", dest='estimators',default=[], type=int, help="Which estimator to use (0)first-spy, (1)ML (approximate)", action='append'
	"-d", "--degree", type=int, help="fixed degree of tree", default=0  <-- if you don't specify this, the code just runs an array of degrees for regular 
			trees. In dataset_main, this argument is ignored, since the graph is fixed
	```

We include below instructions for running the simulations in paper APRP: An Anonymous Propagation Method in Bitcoin Network.

*Figure 6b*: Trickle vs. APRP(Trickle) estimation on d-regular trees, theta = 1.

`python main.py -t 5000 -s 0 -w -e 0`

`python main.py -t 5000 -s 0 -w -e 1`

`python main.py -t 5000 -s 2 -w -e 0`

`python main.py -t 5000 -s 2 -w -e 1`

*Figure 6c*: Diffusion vs. APRP(Diffusion) estimation on d-regular trees, theta = 1.

`python main.py -t 5000 -s 1 -w -e 0`

`python main.py -t 5000 -s 1 -w -e 1`

`python main.py -t 5000 -s 3 -w -e 0`

`python main.py -t 5000 -s 3 -w -e 1`

*Figure 6d*: Diffusion vs. APRP(Diffusion) estimation on 4-regular trees, sweep theta

`python main.py -t 5000 -s 0 -w -e 0 -d 4 -q`

`python main.py -t 5000 -s 0 -w -e 1 -d 4 -q`

`python main.py -t 5000 -s 2 -w -e 0 -d 4 -q`

`python main.py -t 5000 -s 2 -w -e 1 -d 4 -q`

*Figure 6e*: Diffusion vs. APRP(Diffusion) estimation on 4-regular trees, sweep theta

`python main.py -t 5000 -s 1 -w -e 0 -d 4 -q`

`python main.py -t 5000 -s 1 -w -e 1 -d 4 -q`

`python main.py -t 5000 -s 3 -w -e 0 -d 4 -q`

`python main.py -t 5000 -s 3 -w -e 1 -d 4 -q`

*Figure 6f*: Accuracy estimation over real Bitcoin network

`python dataset_main.py -t 5000 -s 0 -w -e 0`

`python dataset_main.py -t 5000 -s 2 -w -e 0`

Reference:
These programs reference some code used in "Deanonymization in the Bitcoin P2P Network," NIPS 2017.