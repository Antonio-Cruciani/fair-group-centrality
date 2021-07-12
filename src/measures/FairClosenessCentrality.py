import networkit as nk
#from groupCentralities.GroupHarmonicCentrality import GroupHarmonicCentrality

import itertools
import networkit as nk
import logging
import time
import random
logging.basicConfig(level=logging.DEBUG)


class GroupClosenessCentrality:
    '''
       Parameters:
           G: Networkit Graph
           k: Size of the group
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
       Method that computes the Closeness Centrality of a set of nodes in the graph
       Parameters: 
               group: list of nodes
    '''
    def ClosenessOfGroup(self,group):
        distances = []
        nk.traversal.Traversal.BFSfrom(self.G, group, lambda u, dist: distances.append(dist))
        return self.G.numberOfNodes() / sum(distances)
    '''
    Method that computes the Maximum Group Closeness Closeness of a set of size k using
    the networkit algorithm if S is not set.
    Otherwise, given the list of groups computed by some heuristic, it computes the Group Closeness Centrality of each group and stores the best one
    '''
    def computeGroupsCentralities(self):
        if(self.S == None):
            logging.info("Computing the Group Harmonic Closeness using networkit")
            start_groups = time.time()
            self.groups_centralities = nk.centrality.GroupCloseness(self.G, self.k).run()

            end_groups = time.time()
            logging.debug("Elapsed time = %r"%(end_groups-start_groups))
            self.max_group = self.groups_centralities.groupMaxCloseness()()
            self.GHC_max_group = self.groups_centralities.scoreOfGroup(self.G, self.max_group)
            #print("GHC = ",self.GHC_max_group)


        else:
            self.groups_centralities = []
            for group in self.groups:
                self.groups_centralities.append(self.ClosenessOfGroup(group))
            # getting the group of k nodes that maximizes the Group Harmonic Centrality
            index = 0
            j = 0
            maximum = 0
            for elem in self.groups_centralities:
                if (elem > maximum):
                    maximum = elem
                    index = j
                j += 1
            self.max_group = self.groups[index]
            self.GHC_max_group = self.groups_centralities[index]

        self.S = self.max_group
        #print(self.S)
        #print(len(self.S))
        #print('------------')

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
        self.groups = [S]

    def set_S(self,S):
        self.S = S
    def get_S(self):
        return self.S

    def get_groups(self):
        return(self.groups)
    def get_groups_centralities(self):
        return(self.groups_centralities)

    def set_k(self,k):
        self.k = k









'''
   Parameters:
       GroupHarmonicCentrality extend this class
'''
class FairGroupClosenessCentrality(GroupClosenessCentrality):
    '''
       Parameters:
           G: networkit graph
           C: list of lists of integers. Each inner list is a community
           k: size of the fair set S
    '''
    def __init__(self, G,C, k):
        super().__init__(G, k)
        # Fair Group Closeness Centrality
        self.communities = C
        # Dictionary <key,value> <---- <int,list>
        # key = key is the index of a community
        # value = each index of the list is the index of a subset of k nodes
        self.FGHC = {}
        self.GH = None
    '''
    Parameters:
            C: list of nodes that represent a community
            group: list of nodes that are "central" nodes for which we compute the measure
    '''
    # Compute the Group Closeness Centrality between the community and the group
    def ClosenessOfGroupOnSubsets(self,C, group):
        nodes = set(C)-set(group)
        distances = []
        for u in nodes:

            bfs = nk.distance.BFS(self.G,u).run()

            min_distance = 100000000
            for v in group:
                dist = bfs.distance(v)
                if(dist< min_distance):
                    min_distance = dist
            if(min_distance >0):

                distances.append(min_distance)
            else:
                distances.append(0.0)


        return(len(nodes)/sum(distances))


    '''
    Parameters:
                S: list of nodes
    The method for each community computes all the Fair Group Harmonic Centrality wrt each group of k nodes in S 
    If such set is not given, it computes all the possible subsets of k nodes in the network using the networkit algorithm
    '''
    def computeFairGroupClosenssCentrality(self,S = []):

        if(not (S or self.S)):
            self.computeGroupsCentralities()

        else:
            if(S):
                self.groups = [S]
            elif(self.S):
                self.groups = [self.S]

        i = 0
        for community in self.communities:

            self.FGHC[i] = []
            for group in self.groups:
                GHC = self.ClosenessOfGroupOnSubsets(community,group)
                #print("len community = ",len(community)," len group = ",len(group)," GHC = ", GHC, " len sett diff = " ,(len((set(community) - set(group)))))

                if(GHC >0):
                    self.FGHC[i].append(GHC)
                else:
                    self.FGHC[i].append(GHC)
            i+=1
        self.GH = self.ClosenessOfGroup(group)
        #self.GH = self.HarmonicOfGroupOnSubsets(group, [])
    def get_GH(self):
        return self.GH
    def get_FGHC(self):
        return self.FGHC

    '''
    Method that randomly build S sampling an element from each community
    '''



    def sampleInEachCommunity(self):
        S = []
        for community in self.communities:
            S.append(random.sample(community, 1)[0])
        self.S = S
        self.groups = [S]


    '''
        Method that build S by taking for each community the node that has highest intra-degree
    '''
    def maxDegreeInEachCommunity(self):
        S = []
        for community in self.communities:
            subgraph = nk.graphtools.subgraphFromNodes(self.G, community)
            degs = []
            for u in community:
                degs.append([u, subgraph.degree(u)])
            degs = sorted(degs, key=lambda tup: tup[1], reverse=True)
            S.append(degs[0][0])
        self.S = S
        self.groups = [S]

    '''
     Method that build S by taking for each community the node with highest intra-harmonic centrality
    '''
    def maxHCInEachCommunity(self,normalized = True,approximated = False):
        S = []
        for community in self.communities:
            subgraph = nk.graphtools.subgraphFromNodes(self.G, community)
            if(approximated):
                centralities = nk.centrality.TopHarmonicCloseness(subgraph,1,useNBbound= False).run().topkNodesList()
                S.append(centralities[0])
            else:
                centralities = nk.centrality.HarmonicCloseness(subgraph, normalized=normalized).run().ranking()
                S.append(centralities[0][0])
        self.S = S
        self.groups = [S]

    '''
       Method that build S by taking the top k nodes that hits all the communities
    '''
    def maxHitting(self):
        # preprocessing
        j = 0
        partition = {}
        for community in self.communities:
            for u in community:
                partition[u] = j
            j=1

        results = []
        for community in self.communities:
            max_hitting = -1
            max_hitting_index = 0
            for v in community:
                hits = {partition[v] : 0}
                for neig in self.G.iterNeighbors(v):
                    if not (partition[neig] in hits):
                        hits[partition[neig]] = 0
                if(len(hits) > max_hitting):
                    max_hitting = len(hits)
                    max_hitting_index = v
            results.append((max_hitting_index,max_hitting))
        results = sorted(results, key=lambda tup: tup[1], reverse=True)
        selected = []
        for node in  results[0:self.k]:
            selected.append(node[0])
        self.S =selected

    def get_price_of_fairness(self):
        fairness = self.FGHC.values()
        if(min(fairness)[0] == 0.0):
            return(-1)
        else:
            return (max(fairness)[0]/min(fairness)[0])


