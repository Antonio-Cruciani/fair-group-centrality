import itertools
import logging
import json
import networkit as nk
import pandas as pd
from src.generators.graphs.SBM import SBM
from src.generators.graphs.ErdosRenyi import ErdosRenyi
from src.generators.graphs.BarabasiAlbert import BarabasiAlbert
from src.measures.FairClosenessCentrality import FairGroupClosenessCentrality

class Closeness:
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
        self.names = []
        self.results = []
        self.node_community_mapping = []
        self.parameters = []

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
                result = {'graph' : self.names[communityIndex],
                          'parameters': self.parameters[communityIndex],
                          'experiment_mod': self.instance['experiments']['mod'],
                          'experiments': []}
                for size in fairSetSizes:
                    FGC = FairGroupClosenessCentrality(graph, self.communities[communityIndex], None)

                    FGC.set_k(size)
                    FGC.sampleS(trials)
                    FGC.computeGroupsCentralities()

                    FGC.computeFairGroupClosenessCentrality(FGC.get_S())

                    #print("Group that maximizes GHC ",FGC.get_S())
                    #print("GH ",FGC.get_GHC_max_group())
                    PoF = FGC.get_price_of_fairness()
                    res = {}
                    res['type_of_exp'] = self.instance['experiments']['mod']
                    res['sampling_trials'] = trials
                    res['fair_set_size'] = len(FGC.get_S())
                    res['fair_set'] = FGC.get_S()
                    res['group_closeness'] = FGC.get_GHC_max_group()
                    res['PoF'] = FGC.get_price_of_fairness()
                    res['fair_closeness_centrality'] = FGC.get_FGCC()
                    res['communities_dimension'] = FGC.get_communities_size()
                    res['node_community_mapping'] = self.node_community_mapping[communityIndex]
                    res['execution_time'] = FGC.get_overall_time()
                    res['fair_group_centrality_time'] = FGC.get_exec_time()
                    res['fair_group_centrality_community_time'] = FGC.get_time_per_comm()

                    #result['experiments'].append(FGC)
                    ''' 
                    logging.debug("Max Group closeness Centrality: %r"%FGC.get_GHC_max_group())
                    if(PoF == -1):
                        logging.debug("PoF: Undefined")
                    else:
                        logging.debug("PoF: %r"%PoF)'''

                    result['experiments'].append(res)
                communityIndex += 1

                results.append(result)
        elif(self.instance['experiments']['mod'] in ['pr','PageRank','pagerank']):
            fairSetSizes = self.instance['experiments']['sSize']
            trials = self.instance['experiments']['nRun']
            results = []
            communityIndex = 0
            for graph in self.graphs:
                result = {'graph': self.names[communityIndex],
                          'parameters': self.parameters[communityIndex],

                          'experiment_mod': self.instance['experiments']['mod'],

                          'experiments': []}


                for size in fairSetSizes:
                    FGC = FairGroupClosenessCentrality(graph, self.communities[communityIndex], None)

                    FGC.set_k(size)
                    FGC.samplePageRankS(trials)
                    FGC.computeGroupsCentralities()
                    FGC.computeFairGroupClosenessCentrality(FGC.get_S())
                    PoF = FGC.get_price_of_fairness()
                    res = {}

                    res['type_of_exp'] = self.instance['experiments']['mod']
                    res['sampling_trials'] = trials
                    res['fair_set_size'] = len(FGC.get_S())
                    res['fair_set'] = FGC.get_S()
                    res['group_closeness'] = FGC.get_GHC_max_group()

                    res['PoF'] = FGC.get_price_of_fairness()
                    res['fair_closeness_centrality'] = FGC.get_FGCC()
                    res['communities_dimension'] = FGC.get_communities_size()
                    res['node_community_mapping'] = self.node_community_mapping[communityIndex]
                    res['execution_time'] = FGC.get_overall_time()
                    res['fair_group_centrality_time'] = FGC.get_exec_time()
                    res['fair_group_centrality_community_time'] = FGC.get_time_per_comm()

                    '''logging.debug("Max Group closeness Centrality: %r"%FGC.get_GHC_max_group())
                    if(PoF == -1):
                        logging.debug("PoF: Undefined")
                    else:
                        logging.debug("PoF: %r"%PoF)'''
                    result['experiments'].append(res)
                communityIndex += 1

                results.append(result)

        elif (self.instance['experiments']['mod'] in ['sampleInEachCommunity', 'siec']):
            fairSetSizes = self.instance['experiments']['sSize']
            trials = self.instance['experiments']['nRun']
            results = []
            communityIndex = 0
            for graph in self.graphs:
                result = {'graph': self.names[communityIndex],
                          'parameters': self.parameters[communityIndex],

                          'experiment_mod': self.instance['experiments']['mod'],

                          'experiments': []}

                FGC = FairGroupClosenessCentrality(graph, self.communities[communityIndex], None)

                FGC.sampleInEachCommunity()
                FGC.computeGroupsCentralities()
                FGC.computeFairGroupClosenessCentrality(FGC.get_S())
                # print("Group that maximizes GHC ",FGC.get_S())
                # print("GH ",FGC.get_GHC_max_group())
                PoF = FGC.get_price_of_fairness()
                res = {}
                res['type_of_exp'] = self.instance['experiments']['mod']
                res['sampling_trials'] = -1
                res['fair_set_size'] = len(FGC.get_S())
                res['fair_set'] = FGC.get_S()
                res['group_closeness'] = FGC.get_GHC_max_group()

                res['PoF'] = FGC.get_price_of_fairness()
                res['fair_closeness_centrality'] = FGC.get_FGCC()
                res['communities_dimension'] = FGC.get_communities_size()
                res['node_community_mapping'] = self.node_community_mapping[communityIndex ]
                res['execution_time'] = FGC.get_overall_time()
                res['fair_group_centrality_time'] = FGC.get_exec_time()
                res['fair_group_centrality_community_time'] = FGC.get_time_per_comm()
                '''logging.debug("Group closeness Centrality: %r" % FGC.get_GH())
                if (PoF == -1):
                    logging.debug("PoF: Undefined")
                else:
                    logging.debug("PoF: %r" % PoF)'''
                result['experiments'].append(res)
                communityIndex+=1

                results.append(result)

        elif (self.instance['experiments']['mod'] in ['maxHitting', 'MH','mh']):
            fairSetSizes = self.instance['experiments']['sSize']
            trials = self.instance['experiments']['nRun']
            results = []
            communityIndex = 0
            for graph in self.graphs:
                result = {'graph': self.names[communityIndex],
                          'parameters': self.parameters[communityIndex],

                          'experiment_mod': self.instance['experiments']['mod'],

                          'experiments': []}


                for size in fairSetSizes:
                    FGC = FairGroupClosenessCentrality(graph, self.communities[communityIndex], None)

                    FGC.set_k(size)
                    FGC.maxHitting()
                    FGC.computeGroupsCentralities()

                    FGC.computeFairGroupClosenessCentrality(FGC.get_S())
                    # print("Group that maximizes GHC ",FGC.get_S())
                    # print("GH ",FGC.get_GHC_max_group())
                    PoF = FGC.get_price_of_fairness()
                    res = {}
                    res['type_of_exp'] = self.instance['experiments']['mod']
                    res['sampling_trials'] = -1
                    res['fair_set_size'] = len(FGC.get_S())
                    res['fair_set'] = FGC.get_S()
                    res['group_closeness'] = FGC.get_GHC_max_group()

                    res['PoF'] = FGC.get_price_of_fairness()
                    res['fair_closeness_centrality'] = FGC.get_FGCC()
                    res['communities_dimension'] = FGC.get_communities_size()
                    res['node_community_mapping'] = self.node_community_mapping[communityIndex]
                    res['execution_time'] = FGC.get_overall_time()
                    res['fair_group_centrality_time'] = FGC.get_exec_time()
                    res['fair_group_centrality_community_time'] = FGC.get_time_per_comm()
                    '''logging.debug("Group closeness Centrality: %r" % FGC.get_GH())
                    if (PoF == -1):
                        logging.debug("PoF: Undefined")
                    else:
                        logging.debug("PoF: %r" % PoF)'''
                    result['experiments'].append(res)
                communityIndex+=1

                results.append(result)

        elif (self.instance['experiments']['mod'] in ['Classic','classic', 'CL', 'cl']):
            fairSetSizes = self.instance['experiments']['sSize']
            trials = self.instance['experiments']['nRun']
            results = []
            communityIndex = 0
            for graph in self.graphs:
                result = {'graph': self.names[communityIndex],
                          'parameters': self.parameters[communityIndex],

                          'experiment_mod': self.instance['experiments']['mod'],

                          'experiments': []}


                for size in fairSetSizes:
                    FGC = FairGroupClosenessCentrality(graph, self.communities[communityIndex], None)

                    FGC.set_S(None)
                    FGC.set_k(size)
                    FGC.computeGroupsCentralities()
                    FGC.computeFairGroupClosenessCentrality(FGC.get_S())

                    # print("Group that maximizes GHC ",FGC.get_S())
                    # print("GH ",FGC.get_GHC_max_group())
                    PoF = FGC.get_price_of_fairness()
                    res = {}
                    res['type_of_exp'] = self.instance['experiments']['mod']
                    res['sampling_trials'] = -1
                    res['fair_set_size'] = len(FGC.get_S())
                    res['fair_set'] = FGC.get_S()
                    res['group_closeness'] = FGC.get_GHC_max_group()

                    res['PoF'] = FGC.get_price_of_fairness()
                    res['fair_closeness_centrality'] = FGC.get_FGCC()
                    res['communities_dimension'] = FGC.get_communities_size()
                    res['node_community_mapping'] = self.node_community_mapping[communityIndex]
                    res['execution_time'] = FGC.get_overall_time()
                    res['fair_group_centrality_time'] = FGC.get_exec_time()
                    res['fair_group_centrality_community_time'] = FGC.get_time_per_comm()

                    '''logging.debug("Group closeness Centrality: %r" % FGC.get_GH())

                    if (PoF == -1):
                        logging.debug("PoF: Undefined")
                    else:
                        logging.debug("PoF: %r" % PoF)'''
                    result['experiments'].append(res)
                communityIndex+=1

                results.append(result)

        elif (self.instance['experiments']['mod'] in ['maxDeg', 'md', 'MD']):
            fairSetSizes = self.instance['experiments']['sSize']
            trials = self.instance['experiments']['nRun']
            results = []
            communityIndex = 0
            for graph in self.graphs:
                result = {'graph': self.names[communityIndex],
                          'parameters': self.parameters[communityIndex],

                          'experiment_mod': self.instance['experiments']['mod'],

                          'experiments': []}


                for size in fairSetSizes:
                    FGC = FairGroupClosenessCentrality(graph, self.communities[communityIndex], None)

                    FGC.set_k(size)
                    FGC.maxDegS()
                    FGC.computeGroupsCentralities()
                    FGC.computeFairGroupClosenessCentrality(FGC.get_S())

                    # print("Group that maximizes GHC ",FGC.get_S())
                    # print("GH ",FGC.get_GHC_max_group())
                    PoF = FGC.get_price_of_fairness()
                    res = {}
                    res['type_of_exp'] = self.instance['experiments']['mod']
                    res['sampling_trials'] = -1
                    res['fair_set_size'] = len(FGC.get_S())
                    res['fair_set'] = FGC.get_S()
                    res['group_closeness'] = FGC.get_GHC_max_group()

                    res['PoF'] = FGC.get_price_of_fairness()
                    res['fair_closeness_centrality'] = FGC.get_FGCC()
                    res['communities_dimension'] = FGC.get_communities_size()
                    res['node_community_mapping'] = self.node_community_mapping[communityIndex]
                    res['execution_time'] = FGC.get_overall_time()
                    res['fair_group_centrality_time'] = FGC.get_exec_time()
                    res['fair_group_centrality_community_time'] = FGC.get_time_per_comm()
                    '''logging.debug("Group closeness Centrality: %r" % FGC.get_GH())
                    if (PoF == -1):
                        logging.debug("PoF: Undefined")
                    else:
                        logging.debug("PoF: %r" % PoF)'''
                    result['experiments'].append(res)
                communityIndex+=1

                results.append(result)


        elif (self.instance['experiments']['mod'] in ['maxDegInEachCommunity', 'mdiec', 'MDIEC']):
            fairSetSizes = self.instance['experiments']['sSize']
            trials = self.instance['experiments']['nRun']
            results = []
            communityIndex = 0
            for graph in self.graphs:
                result = {'graph': self.names[communityIndex],
                          'parameters': self.parameters[communityIndex],

                          'experiment_mod': self.instance['experiments']['mod'],

                          'experiments': []}

                FGC = FairGroupClosenessCentrality(graph, self.communities[communityIndex], None)

                #FGC.set_k(size)
                FGC.maxDegreeInEachCommunity()
                FGC.computeGroupsCentralities()
                FGC.computeFairGroupClosenessCentrality(FGC.get_S())

                # print("Group that maximizes GHC ",FGC.get_S())
                # print("GH ",FGC.get_GHC_max_group())
                PoF = FGC.get_price_of_fairness()
                res = {}
                res['type_of_exp'] = self.instance['experiments']['mod']
                res['sampling_trials'] = -1
                res['fair_set_size'] = len(FGC.get_S())
                res['fair_set'] = FGC.get_S()
                res['group_closeness'] = FGC.get_GHC_max_group()

                res['PoF'] = FGC.get_price_of_fairness()
                res['fair_closeness_centrality'] = FGC.get_FGCC()
                res['communities_dimension'] = FGC.get_communities_size()
                res['node_community_mapping'] = self.node_community_mapping[communityIndex]
                res['execution_time'] = FGC.get_overall_time()
                res['fair_group_centrality_time'] = FGC.get_exec_time()
                res['fair_group_centrality_community_time'] = FGC.get_time_per_comm()
                '''logging.debug("Group closeness Centrality: %r" % FGC.get_GH())
                if (PoF == -1):
                    logging.debug("PoF: Undefined")
                else:
                    logging.debug("PoF: %r" % PoF)'''

                result['experiments'].append(res)
                communityIndex+=1

                results.append(result)


        elif (self.instance['experiments']['mod'] in ['maxHCInEachCommunity', 'mhciec', 'MHCIEC']):
            fairSetSizes = self.instance['experiments']['sSize']
            trials = self.instance['experiments']['nRun']
            results = []
            communityIndex = 0
            for graph in self.graphs:
                result = {'graph': self.names[communityIndex],
                          'parameters': self.parameters[communityIndex],

                          'experiment_mod': self.instance['experiments']['mod'],

                          'experiments': []}

                FGC = FairGroupClosenessCentrality(graph, self.communities[communityIndex], None)


                # FGC.set_k(size)
                FGC.maxHCInEachCommunity()
                FGC.computeGroupsCentralities()
                FGC.computeFairGroupClosenessCentrality(FGC.get_S())

                # print("Group that maximizes GHC ",FGC.get_S())
                # print("GH ",FGC.get_GHC_max_group())
                PoF = FGC.get_price_of_fairness()
                res = {}
                res['type_of_exp'] = self.instance['experiments']['mod']
                res['sampling_trials'] = -1
                res['fair_set_size'] = len(FGC.get_S())
                res['fair_set'] = FGC.get_S()
                res['group_closeness'] = FGC.get_GHC_max_group()

                res['PoF'] = FGC.get_price_of_fairness()
                res['fair_closeness_centrality'] = FGC.get_FGCC()
                res['communities_dimension'] = FGC.get_communities_size()
                res['node_community_mapping'] = self.node_community_mapping[communityIndex ]
                res['execution_time'] = FGC.get_overall_time()
                res['fair_group_centrality_time'] = FGC.get_exec_time()
                res['fair_group_centrality_community_time'] = FGC.get_time_per_comm()
                logging.debug("Group closeness Centrality: %r" % FGC.get_GH())
                if (PoF == -1):
                    logging.debug("PoF: Undefined")
                else:
                    logging.debug("PoF: %r" % PoF)
                result['experiments'].append(res)
                communityIndex += 1

                results.append(result)
        self.results.extend(results)

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
        self.graphs.append(nk.graphio.EdgeListReader('\t', 0, '#').read(self.instance['inputPathGraph']))

        #self.graphs.append(nk.graphio.SNAPGraphReader().read(self.instance['inputPathGraph']))
        logging.info("Loading Graph: Completed")
        edgeListName = self.instance['inputPathGraph'].split('/')[-1]
        self.names.append(edgeListName)
        self.communities.append(communities)
        self.parameters.append(" ")

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
            elif(elem['name'] in ['SBM','sbm','Stochastic-Block-Model']):
                inputPath = "datasets/synthetic/sbm/"
                edgeListName = "Stochastic-Block-Model.ungraph.txt"
                communitiesName = "Stochastic-Block-Model.all.cmty.txt"

            parameterKeys =  list(elem['parameters'].keys())
            name = ""
            j = 0
            for e,v in elem['parameters'].items():
                name += str(e) + str(v)
                if(j<len(elem['parameters'])):
                    name+="/"
                j+=1
            self.parameters.append(elem['parameters'])
            #print(elem['parameters'])
            # for para in parametersCombination:
            #     name = ""
            #     j = 0
            #     for e in para:
            #         name += "_" + str(paraKeys[j]) + "_" + str(e)
            #         j += 1

            inputPathGraph = inputPath + name + edgeListName
            inputPathCommunities = inputPath + name + communitiesName
            communities = []
            index = 0
            node_community_mapping = {}
            with open(inputPathCommunities, 'r') as f:
                data = f.read()

                for line in data.split("\n"):
                    community = []
                    for elem in line.split("\t"):
                        community.append(int(elem))
                        node_community_mapping[int(elem)] = index
                    communities.append(community)
                    index +=1
            self.graphs.append(nk.graphio.EdgeListReader('\t', 0, '#').read(inputPathGraph))
            #self.graphs.append(nk.graphio.SNAPGraphReader().read(inputPathGraph))
            self.names.append(edgeListName)
            self.communities.append(communities)
            self.node_community_mapping.append(node_community_mapping)


    def get_graphs(self):
        return (self.graphs)
    def get_communities(self):
        return(self.communities)
    def get_node_community_mapping(self):
        return (self.node_community_mapping)

    def save_results_to_json(self,path = "./"):
        with open(path, 'a+', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=4)

    def save_results_to_csv(self,path = "./"):
        lista_to_csv = []
        for elem in self.results:
            for exp in elem['experiments']:
                lista_to_csv.append({**elem['parameters'],**exp})

        for dic in self.results:
            df = pd.DataFrame(lista_to_csv)
            name = dic['graph'][0:-4]
            towriteName = ''
            for x in name:
                towriteName+=x
            df.to_csv(path+towriteName+'.csv')

        print("TO DO")





