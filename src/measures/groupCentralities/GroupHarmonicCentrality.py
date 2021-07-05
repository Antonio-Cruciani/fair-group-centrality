import itertools
import networkit as nk
import logging
import time
import random
logging.basicConfig(level=logging.DEBUG)

# DEPRECATED !!!!
class GroupHarmonicCentrality:
    '''
       Parameters:
           G: Networkit Graph
           k: Size of the fair set S
    '''

    def __init__(self,G,k):
        self.G = G
        self.k = k

        self.nodes = [u for u in self.G.iterNodes()]

        self.groups = None
        self.groups_centralities = None

        self.degree_heuristic_group = None
        self.GHC_degree_heuristic_group = None

        self.max_group = None
        self.GHC_max_group = None

        self.S = None


    def findsubsets(self,s, k):
        return list(itertools.combinations(s, k))

    '''
    Method that computes the Harmonic Centrality of a set of nodes in the graph
    Parameters: 
            group: list of nodes
    '''

    def HarmonicOfGroup(self,group):
        distances = []
        nk.traversal.Traversal.BFSfrom(self.G, group, lambda u, dist: distances.append(dist))
        normalized = []
        for dist in distances:
            if(dist != 0):
                normalized.append(1./dist)
            else:
                normalized.append(0.0)

        return sum(normalized)

    '''
    TO COMPLETE
    '''
    def computeGroupsCentralities(self):
        # if(self.S == None):
        #     logging.debug("Computing all the subsets of %r nodes"%(self.k))
        #     logging.debug("Advice: get a coffee..")
        #     start_groups = time.time()
        #     self.groups = self.findsubsets(self.nodes,self.k)
        #     end_groups = time.time()
        #     logging.debug("Elapsed time = %r"%(end_groups-start_groups))
        #     logging.debug("Number of groups = %r"%(len(self.groups)))
        # self.groups_centralities = []
        # for group in self.groups:
        #     self.groups_centralities.append(self.HarmonicOfGroup(group))
        ciao = nk.centrality.GroupHarmonicCloseness(self.G,10)
        ciao.run()
        print(ciao)
        #print(ciao.groupMaxHarmonicCloseness()())
        # getting the group of k nodes that maximizes the Group Harmonic Centrality
        index = 0
        j = 0
        maximum = 0

        for elem in self.groups_centralities:
            if(elem>maximum):
                maximum = elem
                index = j
            j+=1

        self.max_group = self.groups[index]
        self.GHC_max_group = self.groups_centralities[index]


    def get_GHC_max_group(self):
        return self.GHC_max_group
    def get_max_group(self):
        return self.max_group
    '''
    Parameters: 
                numberOfSets: number of random sets to sample (without replacement) from the graph G
    Method that samples without replacement k nodes from the graph.
    '''
    def sampleS(self,numberOfSets = 1):
        S = []
        for i in range(0,numberOfSets):
            S.append(random.sample(self.nodes, self.k))
        self.S = S
        self.groups = S

    '''
    Parameters: 
                numberOfSets: number of random sets to sample (without replacement) from the graph G
    Method that samples without replacement k nodes from the graph using the PageRank Algorithm, it gets the k-best nodes.
    '''
    def samplePageRankS(self,numberOfSets = 1):
        S = []
        for j in range(0,numberOfSets):
            PR = nk.centrality.PageRank(self.G).run().ranking()
            ranking = []
            for i in range(0,self.k):
                ranking.append(PR[i][0])
            S.append(ranking)
        self.S = S
        self.groups = S

    '''
    Method that gets the k-best nodes with higher degree
    '''
    def maxDegS(self):
        S = []
        degs = []
        for u in self.nodes:
            degs.append([u,self.G.degree(u)])

        degs = sorted(degs, key=lambda tup: tup[1],reverse=True)
        for i in range(0,self.k):
            S.append(degs[i][0])
        self.S = S
        self.groups = S

    def set_S(self,S):
        self.S = S
    def get_S(self):
        return self.S

    def get_groups(self):
        return(self.groups)
    def get_groups_centralities(self):
        return(self.groups_centralities)








