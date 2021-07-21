import networkit as nk
import random
# from src.measures.groupCentralities.GroupHarmonicCentrality import GroupHarmonicCentrality
from src.measures.FairHarmonicCentrality import FairGroupHarmonicCentrality, GroupHarmonicCentrality
from src.generators.graphs.ErdosRenyi import ErdosRenyi
from src.generators.graphs.BarabasiAlbert import BarabasiAlbert
from src.generators.graphs.SBM import SBM
from src.experiments.Closeness import Closeness
import math as mt
import time
import logging

logging.basicConfig(level=logging.DEBUG)

sizes = [10, 10, 10, 10, 10]
n = 50
p = 0.5
k = 3
'''instance = {
    "type" : "Synthetic",

    "graphs" : [{"name":"Barabasi-Albert",
            "parameters":{"n":1000,
                      "k":10,
            "cs_":"bfs",
            "c_threshold":3
            }},
            {"name":"Barabasi-Albert",
            "parameters":{"n":10000,
                      "k":15,
            "cs_":"bfs",
            "c_threshold":3
            }}],

    "experiments" : {
                    "mod": "rnd",
                    "sSize": [20],
                    "nRun":10,
                    }
}'''
# Run Harmonic Experiments on Erdos Renyi graph
# 64,128,256,512,1024,2048,4096,8192,16384
nodes = [64, 128, 256, 512, 1024, 2048]
# p for sparse erdos renyi
epsilon = 0.00005

probs = [0.1, 0.2, 0.3, 0.4, 0.5]
lista = []
# techniques = ['rnd','pr','siec','mh','cl','md','mdiec','mhciec']
techniques = ['siec']

# Erdos-Renyi
for tech in techniques:
    lista = []

    for n in nodes:
        i = 2
        j = 2
        sizes = []
        while(j< n):
            sizes.append(j)
            j = 2**i
            i+=1
        instance = {
            "type": "Synthetic",

            "graphs": [],
            "experiments": {
                "mod": tech,
                "sSize": sizes,
                "nRun": 100,
            }

        }
        prib = probs.copy()
        prib.extend([(1 - epsilon) * (mt.log(n, 2) / n),(1 + epsilon) * (mt.log(n, 2) / n)])
        for p in prib:
            start = time.time()
            th = mt.log(n,2)
            instance['graphs'].append(
                {
                    "name": "Erdos-Renyi",
                    'parameters':{
                        'n':n,
                        'p':p,
                        'cs_':'bfs',
                        'c_threshold': mt.log(n,2)
                    }
                }
            )
            end = time.time() - start

            logging.info("Define Erdos-Renyi parameters n = %r p = %r technique = bfs threshold = %r elapsed time = %r"%(n,p,th,end))
        lista.append(instance)
    i = 0
    for instance in lista:
        start = time.time()
        exp = Closeness(instance=instance)
        exp.run()
        print(len(lista), i)
        print(instance['graphs'])
        n = instance['graphs'][i]['parameters']['n']
        exp.save_results_to_json(
            "./src/outputs/jsons/" + "results_" + instance['graphs'][i]['name'] + "_n_" + str(n) + "_exp_" +
            instance['experiments']['mod'])
        end = time.time() - start

        logging.info(" Experiment on instance number %r completed! Elapsed time: %r" % (i, end))

        i += 1
# Barabasi-Albert

for tech in techniques:
    lista = []
    for n in nodes:
        i = 2
        j = 2
        sizes = []
        while(j< n):
            sizes.append(j)
            j = 2**i
            i+=1
        instance = {
            "type": "Synthetic",

            "graphs": [],
            "experiments": {
                "mod": tech,
                "sSize": sizes,
                "nRun": 100,
            }

        }
        # Barabasi-Albert

        start = time.time()
        th = mt.log(n, 2)
        instance['graphs'].append(
            {
                "name": "Barabasi-Albert",
                'parameters': {
                    'n': n,
                    'k': th,
                    'cs_': 'bfs',
                    'c_threshold': th
                }
            }
        )
        end = time.time() - start

        logging.info("Defined Barabasi-Albert n = %r k = %r technique = bfs threshold = %r elapsed time = %r" % (n, th, th,end))

        lista.append(instance)

    for instance in lista:
        start = time.time()
        exp = Closeness(instance= instance)
        exp.run()

        n = instance['graphs'][0]['parameters']['n']
        exp.save_results_to_json("./src/outputs/jsons/"+"results_"+instance['graphs'][0]['name']+"_n_"+str(n)+"_exp_"+instance['experiments']['mod'])
        end = time.time() - start

        logging.info(" Experiment on instance completed! Elapsed time: %r"%(end))

        

# SBM

for exp_type in techniques:
    lista = []
    # exp_type = "mhciec"
    for n in nodes:
        q = 0.005
        p = 0.1
        i = 2
        j = 2
        sizes = []
        while (j < n):
            sizes.append(j)
            j = 2 ** i
            i += 1
        instance = {
            "type": "Synthetic",

            "graphs": [],
            "experiments": {
                "mod": exp_type,
                "sSize": sizes,
                "nRun": 100,
            }

        }

        start = time.time()
        th = mt.log(n, 2)
        instance['graphs'].append(
            {
                "name": "Stochastic-Block-Model",
                'parameters': {
                    'n': n,
                    'p': p,
                    'q': q,
                    'cs_': 'rd',
                    'c': th
                }
            }
        )
        end = time.time() - start

        logging.info(
            "Defined SBM n = %r p = %r q = %r technique = rdn communities = %r elapsed time = %r" % (n, p, q, th, end))

        lista.append(instance)
    for n in nodes:
        p = 0.2
        i = 2
        j = 2
        sizes = []
        while (j < n):
            sizes.append(j)
            j = 2 ** i
            i += 1
        instance = {
            "type": "Synthetic",

            "graphs": [],
            "experiments": {
                "mod": exp_type,
                "sSize": sizes,
                "nRun": 100,
            }

        }
        for q in [0.05, 0.1]:
            start = time.time()
            th = mt.log(n, 2)
            instance['graphs'].append(
                {
                    "name": "Stochastic-Block-Model",
                    'parameters': {
                        'n': n,
                        'p': p,
                        'q': q,
                        'cs_': 'rd',
                        'c': th
                    }
                }
            )
            end = time.time() - start

            logging.info(
                "Defined SBM n = %r p = %r q = %r technique = rdn communities = %r elapsed time = %r" % (
                n, p, q, th, end))

        lista.append(instance)

    for n in nodes:
        p = 0.3
        i = 2
        j = 2
        sizes = []
        while (j < n):
            sizes.append(j)
            j = 2 ** i
            i += 1
        instance = {
            "type": "Synthetic",

            "graphs": [],
            "experiments": {
                "mod": exp_type,
                "sSize": sizes,
                "nRun": 100,
            }

        }
        for q in [0.05, 0.1, 0.2, 0.3]:
            start = time.time()
            th = mt.log(n, 2)
            instance['graphs'].append(
                {
                    "name": "Stochastic-Block-Model",
                    'parameters': {
                        'n': n,
                        'p': p,
                        'q': q,
                        'cs_': 'rd',
                        'c': th
                    }
                }
            )
            end = time.time() - start

            logging.info(
                "Defined SBM n = %r p = %r q = %r technique = rdn communities = %r elapsed time = %r" % (
                n, p, q, th, end))

        lista.append(instance)

    for n in nodes:
        p = 0.4
        i = 2
        j = 2
        sizes = []
        while (j < n):
            sizes.append(j)
            j = 2 ** i
            i += 1
        instance = {
            "type": "Synthetic",

            "graphs": [],
            "experiments": {
                "mod": exp_type,
                "sSize": sizes,
                "nRun": 100,
            }

        }
        for q in [0.05, 0.1, 0.2, 0.3]:
            start = time.time()
            th = mt.log(n, 2)
            instance['graphs'].append(
                {
                    "name": "Stochastic-Block-Model",
                    'parameters': {
                        'n': n,
                        'p': p,
                        'q': q,
                        'cs_': 'rd',
                        'c': th
                    }
                }
            )
            end = time.time() - start

            logging.info(
                "Defined SBM n = %r p = %r q = %r technique = rdn communities = %r elapsed time = %r" % (
                n, p, q, th, end))

        lista.append(instance)

    for n in nodes:
        p = 0.5
        i = 2
        j = 2
        sizes = []
        while (j < n):
            sizes.append(j)
            j = 2 ** i
            i += 1
        instance = {
            "type": "Synthetic",

            "graphs": [],
            "experiments": {
                "mod": exp_type,
                "sSize": sizes,
                "nRun": 100,
            }

        }
        for q in [0.05, 0.1, 0.2, 0.3]:
            start = time.time()
            th = mt.log(n, 2)
            instance['graphs'].append(
                {
                    "name": "Stochastic-Block-Model",
                    'parameters': {
                        'n': n,
                        'p': p,
                        'q': q,
                        'cs_': 'rd',
                        'c': th
                    }
                }
            )
            end = time.time() - start

            logging.info(
                "Defined SBM n = %r p = %r q = %r technique = rdn communities = %r elapsed time = %r" % (
                n, p, q, th, end))

        lista.append(instance)
    i = 0
    for instance in lista:
        start = time.time()
        exp = Closeness(instance=instance)
        exp.run()
        print(instance['graphs'])
        n = instance['graphs'][0]['parameters']['n']
        print(n)

        exp.save_results_to_json(
            "./src/outputs/jsons/" + "results_" + instance['graphs'][0]['name'] + "_n_" + str(n) + "_exp_" +
            instance['experiments']['mod'])
        end = time.time() - start

        logging.info(" Experiment on instance completed! Elapsed time: %r" % (end))

        i += 1

'''instance = {
    "type" : "Synthetic",

    "graphs" : [
                {"name":"Erdos-Renyi",
            "parameters":{"n":64,
                      "p":0.2,
            "cs_":"bfs",
            "c_threshold":6.0
            }},
                {"name":"Erdos-Renyi",
            "parameters":{"n":64,
                      "p":0.1,
            "cs_":"bfs",
            "c_threshold":6.0
            }}],


    "experiments" : {
                    "mod": "rnd",
                    "sSize": [8,16,32],
                    "nRun":100,
                    }
}'''

'''instance = {
    "type" : "Synthetic",

    "graphs" : [{"name":"Erdos-Renyi",
            "parameters":{"n":1000,
                    "p":0.3,

            "cs_":"rd",
            "c":10
            }}],


    "experiments" : {
                    "mod": "rnd",
                    "sSize": [64,128,256,512],
                    "nRun":100,
                    }
}'''
'''instance = {
    "type" : "Real",
    "inputPathGraph": "./datasets/real/dblp/com-dblp.ungraph.txt",
    "inputPathCommunities": "datasets/real/dblp/com-dblp.all.cmty.txt",
    "graph":"com-dblp",
    "experiments" : {
                    "mod": "rnd",
                    "sSize": [64,128,256,512,1024,2048],
                    "nRun":100,
                    }

}
lista.append(instance)'''
# Erdos Renyi
'''i = 0
for instance in lista:
    start = time.time()
    exp = Closeness(instance=instance)
    exp.run()
    print(len(lista),i)
    print(instance['graphs'])
    n = instance['graphs'][i]['parameters']['n']
    exp.save_results_to_json("./src/outputs/jsons/"+"results_"+instance['graphs'][i]['name']+"_n_"+str(n)+"_exp_"+instance['experiments']['mod'])
    end = time.time() - start

    logging.info(" Experiment on instance number %r completed! Elapsed time: %r"%(i,end))

    i+=1'''
# exp.save_results_to_csv("./src/outputs/csvs/")
# Barabasi Albert

'''for instance in lista:
    start = time.time()
    exp = Closeness(instance=instance)
    exp.run()

    n = instance['graphs'][0]['parameters']['n']
    exp.save_results_to_json("./src/outputs/jsons/"+"results_"+instance['graphs'][0]['name']+"_n_"+str(n)+"_exp_"+instance['experiments']['mod'])
    end = time.time() - start

    logging.info(" Experiment on instance completed! Elapsed time: %r"%(end))
'''
# SBM

'''i =0
for instance in lista:
    start = time.time()
    exp = Closeness(instance=instance)
    exp.run()
    print(instance['graphs'])
    n = instance['graphs'][0]['parameters']['n']
    print(n)

    exp.save_results_to_json("./src/outputs/jsons/"+"results_"+instance['graphs'][0]['name']+"_n_"+str(n)+"_exp_"+instance['experiments']['mod'])
    end = time.time() - start

    logging.info(" Experiment on instance completed! Elapsed time: %r"%(end))

    i+=1

    #exp.save_results_to_csv("./src/outputs/csvs/")'''

# real
'''for instance in lista:
    start = time.time()
    exp = Closeness(instance=instance)
    exp.run()

    #n = instance['graphs'][0]['parameters']['n']
    exp.save_results_to_json("./src/outputs/jsons/"+"results_"+instance['graphs']+"_exp_"+instance['experiments']['mod'])
    end = time.time() - start

    logging.info(" Experiment on instance completed! Elapsed time: %r"%(end))
'''
'''exit(1)
FGH = FairGroupHarmonicCentrality(exp.get_graphs()[0],exp.get_communities()[0],10)
FGH.computeGroupsCentralities()
print("<<<<<<<<<<<<<<<<<<<<<<<<<<")
print(FGH.get_S())

#FGH.computeFairGroupHarmonicCentrality([GH.get_max_group()] )
#FGH.sampleInEachCommunity()
#FGH.computeFairGroupHarmonicCentrality()
FGH.maxHitting()
OverallHarmonic = FGH.get_GHC_max_group()
print(OverallHarmonic)
print("overall HC of S ",OverallHarmonic)
fairHCentrality = FGH.get_FGHC()
print(fairHCentrality)
exit(1)
ba =  BarabasiAlbert(n, k,communities_number = 50,communities_structure = "bfs",communities_size= [],treshold = 40)
ba.run()
ba.save_graph()
print(ba.get_n())
print(ba.get_communities())
exit(1)
print("Detected")
ba.communityDetection('plm')

print(ba.get_detectedCommunities())
print("Syntetic")
print(ba.get_communities())
er = ErdosRenyi(n,p,communities_number = 50,communities_structure = "bfs",communities_size = sizes,treshold = 40)
er.run()
print("ERDOS")
#print("Detected")
#er.communityDetection("plm")
#print(er.get_detectedCommunities())
print("Syntetic")
print(er.get_communities())
n = 500
k = 10
p_in = 0.7
p_out = 0.4
sbm = SBM(n,p_in,p_out,k)
print("SBM")
print(sbm.get_communities())
sbm.save_graph()


G = nk.graphio.SNAPGraphReader().read("./datasets/real/dblp/com-dblp.ungraph.txt")
communities = []
with open("datasets/real/dblp/com-dblp.all.cmty.txt", 'r') as f:
    data =f.read()

    for line in data.split("\n"):
        community = []
        for elem in line.split("\t"):
            community.append(int(elem))
        communities.append(community)

   # perform file operations
# Kadabra is apx betweennes
n = 500
k = 10
p_in = 0.7
p_out = 0.4
Clustered = nk.generators.ClusteredRandomGraphGenerator(n,k,p_in,p_out)
clustered = Clustered.generate()
C =  Clustered.getCommunities()
idCommunities =  C.getSubsetIds()
Communities = []
for id in idCommunities:
    Communities.append(list(C.getMembers(id)))

nodi = [u for u in clustered.iterNodes()]
S= [random.sample(nodi, k)]




FGH = FairGroupHarmonicCentrality(clustered,Communities,10)
#FGH.samplePageRankS(50)

FGH.computeGroupsCentralities()
print("<<<<<<<<<<<<<<<<<<<<<<<<<<")
print(FGH.get_S())
#FGH.computeFairGroupHarmonicCentrality([GH.get_max_group()] )
#FGH.sampleInEachCommunity()
FGH.computeFairGroupHarmonicCentrality()
print(FGH.get_S())
OverallHarmonic = FGH.get_GHC_max_group()
print("FGHC of S ",FGH.get_FGHC())
print("overall HC of S ",OverallHarmonic)


exit(1)
kadabra = nk.centrality.KadabraBetweenness(G,0.05,0.8)
kadabra.run()
# The exhaustive Harmonic is really expensive and slow on big graphs,
# Top Harmonic is an apx version that finds only the top k = 10 nodes
harmonic = nk.centrality.TopHarmonicCloseness(G,10,useNBbound= False)
harmonic.run()
print("HARMONIC")
print(harmonic.topkNodesList())
print(harmonic.topkScoresList())
print("KADABRA")
print(kadabra.ranking()[:10])'''