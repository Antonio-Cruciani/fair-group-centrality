import itertools
import logging

import networkit as nk
from src.generators.graphs.SBM import SBM
from src.generators.graphs.ErdosRenyi import ErdosRenyi
from src.generators.graphs.BarabasiAlbert import BarabasiAlbert
from src.measures.FairHarmonicCentrality import FairGroupHarmonicCentrality,GroupHarmonicCentrality
class Harmonic:
    '''
    instance= {
         type = "Syntetic or Real"
         graph = [{ "name": ,
                "parameters":{"n": ,
                            "k":,
                            "structure": ,
                            "threshold"; ,
                            }   }],
        experiments = {"mod": rnd\pagerank\maxHitting\classic\maxDeg\sampleInEachCommunity\maxDegreeInEachCommunity\maxHCInEachCommunity,
                        "Ssize": [ ] ,
                        "nRun": ,
                    }

     }
    '''
    def __init__(self,instance):

        self.instance = instance
        self.graphs = []
        self.communities = []


    def run(self):
        if(self.instance['type'] in ['synthetic','Synthetic']):
            self.runSynteticExperiments()
        if(self.instance['type'] in ['real','Real']):
            self.runRealExperiments()
        if(self.instance['experiments']['mod'] in ['rnd','random','rd']):
            fairSetSizes = self.instance['experiments']['sSize']
            trials = self.instance['experiments']['nRun']
            results = []
            communityIndex = 0
            for graph in self.graphs:

                FGH = FairGroupHarmonicCentrality(graph,self.communities[communityIndex], None)

                for size in fairSetSizes:
                    FGH.set_k(size)
                    FGH.sampleS(trials)
                    FGH.computeGroupsCentralities()
                    FGH.computeFairGroupHarmonicCentrality(FGH.get_S())
                    #print("Group that maximizes GHC ",FGH.get_S())
                    #print("GH ",FGH.get_GHC_max_group())
                    PoF = FGH.get_price_of_fairness()
                    logging.debug("Max Group Harmonic Centrality: %r"%FGH.get_GHC_max_group())
                    if(PoF == -1):
                        logging.debug("PoF: Undefined")
                    else:
                        logging.debug("PoF: %r"%PoF)

        elif(self.instance['experiments']['mod'] in ['pr','PageRank','pagerank']):
            fairSetSizes = self.instance['experiments']['sSize']
            trials = self.instance['experiments']['nRun']
            results = []
            communityIndex = 0
            for graph in self.graphs:

                FGH = FairGroupHarmonicCentrality(graph,self.communities[communityIndex], None)

                for size in fairSetSizes:
                    FGH.set_k(size)
                    FGH.samplePageRankS(trials)
                    FGH.computeGroupsCentralities()
                    FGH.computeFairGroupHarmonicCentrality(FGH.get_S())
                    #print("Group that maximizes GHC ",FGH.get_S())
                    #print("GH ",FGH.get_GHC_max_group())
                    PoF = FGH.get_price_of_fairness()
                    logging.debug("Max Group Harmonic Centrality: %r"%FGH.get_GHC_max_group())
                    if(PoF == -1):
                        logging.debug("PoF: Undefined")
                    else:
                        logging.debug("PoF: %r"%PoF)
        elif (self.instance['experiments']['mod'] in ['sampleInEachCommunity', 'siec']):
            fairSetSizes = self.instance['experiments']['sSize']
            trials = self.instance['experiments']['nRun']
            results = []
            communityIndex = 0
            for graph in self.graphs:

                FGH = FairGroupHarmonicCentrality(graph, self.communities[communityIndex], None)

                for size in fairSetSizes:
                    FGH.set_k(size)
                    FGH.sampleInEachCommunity()
                    FGH.computeFairGroupHarmonicCentrality(FGH.get_S())
                    # print("Group that maximizes GHC ",FGH.get_S())
                    # print("GH ",FGH.get_GHC_max_group())
                    PoF = FGH.get_price_of_fairness()
                    logging.debug("Group Harmonic Centrality: %r" % FGH.get_GH())
                    print(len(FGH.get_S()))
                    if (PoF == -1):
                        logging.debug("PoF: Undefined")
                    else:
                        logging.debug("PoF: %r" % PoF)

    def runRealExperiments(self):
        logging.info("Loading Communities")
        communities = []
        with open(self.instance['inputPathCommunities'], 'r') as f:
            data = f.read()

            for line in data.split("\n"):
                community = []
                for elem in line.split("\t"):
                    community.append(int(elem))
                communities.append(community)
        logging.info("Loading Communities: Completed")
        logging.info("Loading Graph")
        self.graphs.append(nk.graphio.SNAPGraphReader().read(self.instance['inputPathGraph']))
        logging.info("Loading Graph: Completed")

        self.communities.append(communities)

    # Method that load the datasets and run the experiments

    def runSynteticExperiments(self):
        for elem in self.instance['graphs']:

            # listOfParameters = []
            #
            # for parameter in self.instance['graphs'][elem]:
            #
            #     listOfParameters.append(parameter)
            #
            # parametersCombination =list(itertools.product(*listOfParameters))
            # paraKeys = list(self.instance['graphs'][elem].keys())
            # Loading the graphs
            if(elem['name'] in ['Erdos-Renyi','ER','er','Erdos Renyi','ErdosRenyi']):
                inputPath = "datasets/synthetic/erdos_renyi/"
                edgeListName = "Erdos-Renyi.ungraph.txt"
                communitiesName = "Erdos-Renyi.all.cmty.txt"

            elif(elem['name'] in ['Barabasi-Albert','BA','ba','BarabasiAlbert','Barabasi Albert']):
                inputPath = "datasets/synthetic/barabasi_albert/"
                edgeListName = "Barabasi-Albert.ungraph.txt"
                communitiesName = "Barabasi-Albert.all.cmty.txt"
            elif(elem in ['SBM','sbm']):
                inputPath = "datasets/synthetic/sbm/"
                edgeListName = "SBM.ungraph.txt"
                communitiesName = "SBM.all.cmty.txt"

            parameterKeys =  list(elem['parameters'].keys())
            name = ""
            j = 0
            for e,v in elem['parameters'].items():
                name += str(e) + str(v)
                if(j<len(elem['parameters'])):
                    name+="/"
                j+=1

            # for para in parametersCombination:
            #     name = ""
            #     j = 0
            #     for e in para:
            #         name += "_" + str(paraKeys[j]) + "_" + str(e)
            #         j += 1

            inputPathGraph = inputPath + name + edgeListName
            inputPathCommunities = inputPath + name + communitiesName
            communities = []
            with open(inputPathCommunities, 'r') as f:
                data = f.read()

                for line in data.split("\n"):
                    community = []
                    for elem in line.split("\t"):
                        community.append(int(elem))
                    communities.append(community)

            self.graphs.append(nk.graphio.SNAPGraphReader().read(inputPathGraph))

            self.communities.append(communities)

    def get_graphs(self):
        return (self.graphs)
    def get_communities(self):
        return(self.communities)




