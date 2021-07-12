# This module is used to generate the Synthetic datasets with the desired properties
import src.generators.graphs.NetworkGenerator as ng
import math as mt
import logging
import time
models = ['BA','ER','SBM']
nodes = [64,128,256,512,1024,2048,4096,8192,16384]
# p for sparse erdos renyi
probs = [0.1,0.2,0.3,0.4,0.5]
# creating communities using bfs with threshold of log(n)
logging.basicConfig(level=logging.DEBUG)
# Remove comments to generate Erdos-Renyi
'''for n in nodes:
    for p in probs:
        start = time.time()
        th = mt.log(n,2)
        ng.generate_network(network_type='ER', n=n, p=p, communities_structure='bfs',  threshold=th)
        end = time.time() - start

        logging.info("Created Erdos-Renyi n = %r p = %r technique = bfs threshold = %r elapsed time = %r"%(n,p,th,end))'''
# Remove comments to generate ER random graph with (1-epsilon)log n / n = p and (1+epslion) log n / n = p
'''epsilon = 0.00005

for n in nodes:
    start = time.time()
    th = mt.log(n, 2)

    p = (1-epsilon)*(mt.log(n,2)/n)
    ng.generate_network(network_type='ER', n=n, p=p, communities_structure='bfs', threshold=th)
    end = time.time() - start
    logging.info("Created Erdos-Renyi n = %r p = %r technique = bfs threshold = %r elapsed time = %r" % (n, p, th, end))

for n in nodes:
    start = time.time()
    th = mt.log(n, 2)

    p = (1+epsilon)*(mt.log(n,2)/n)

    ng.generate_network(network_type='ER', n=n, p=p, communities_structure='bfs', threshold=th)
    end = time.time() - start
    logging.info("Created Erdos-Renyi n = %r p = %r technique = bfs threshold = %r elapsed time = %r" % (n, p, th, end))
'''
# Generating Barabasi-Albert Graphs....................................................................................
#ng.generate_network(network_type='BA', n=1000, k=10, communities_structure='bfs', threshold=100)

'''ng.generate_network(network_type='BA', n=10000, k=15, communities_structure='bfs', threshold=3)

ng.generate_network(network_type='BA', n=1000, k=10, communities_structure='auto')


# Generating Erdos-Renyi Graphs........................................................................................
ng.generate_network(network_type='ER', n=1000, p=0.3, communities_structure='rd', number_of_communities=10)

# Generating graphs using SBM..........................................................................................
ng.generate_network(network_type='SBM', n=1000, p=0.5, q=0.5, communities_structure='rd', number_of_communities=10)
'''
# Remove comments to generate SBM
'''for n in nodes:
    ng.generate_network(network_type='SBM', n=n, p=0.1, q=0.005, communities_structure='rd', number_of_communities=mt.log(n,2))
for n in nodes:
    for q in [0.05,0.1]:

        ng.generate_network(network_type='SBM', n=n, p=0.2, q=q, communities_structure='rd',
                            number_of_communities=mt.log(n, 2))


for n in nodes:
    for q in [0.05,0.1,0.2,0.3]:

        ng.generate_network(network_type='SBM', n=n, p=0.3, q=q, communities_structure='rd',
                            number_of_communities=mt.log(n, 2))

for n in nodes:
    for q in [0.05,0.1,0.2,0.3]:

        ng.generate_network(network_type='SBM', n=n, p=0.4, q=q, communities_structure='rd',
                            number_of_communities=mt.log(n, 2))


for n in nodes:
    for q in [0.05,0.1,0.2,0.3]:
        ng.generate_network(network_type='SBM', n=n, p=0.5, q=q, communities_structure='rd',
                            number_of_communities=mt.log(n, 2))'''

# Remove comments to generate barabasi albert with logarithmic k
'''for n in nodes:
    start = time.time()
    th = mt.log(n, 2)
    ng.generate_network(network_type='BA', n=n, k=th, communities_structure='bfs', threshold=th)
    end = time.time() - start

    logging.info("Created Barabasi-Albert n = %r k = %r technique = bfs threshold = %r elapsed time = %r" % (n, th, th, end))'''