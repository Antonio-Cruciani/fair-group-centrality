import networkit as nk
#from groupCentralities.GroupHarmonicCentrality import GroupHarmonicCentrality

import itertools
import networkit as nk
import logging
import time
import random
logging.basicConfig(level=logging.DEBUG)


class GroupHarmonicCentrality:
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
    Method that computes the Maximum Group Harmonic Closeness of a set of size k using
    the networkit algorithm
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
        self.groups_centralities = nk.centrality.GroupHarmonicCloseness(self.G,self.k).run()

        self.max_group = self.groups_centralities.groupMaxHarmonicCloseness()

        self.GHC_max_group = self.groups_centralities.scoreOfGroup(self.G,self.max_group)
        self.S = self.max_group

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











'''
   Parameters:
       GroupHarmonicCentrality extend this class
'''
class FairGroupHarmonicCentrality(GroupHarmonicCentrality):
    '''
       Parameters:
           G: networkit graph
           C: list of lists of integers. Each inner list is a community
           k: size of the fair set S
    '''
    def __init__(self, G,C, k):
        super().__init__(G, k)
        # Fair Group Harmonic Centrality
        self.communities = C
        # Dictionary <key,value> <---- <int,list>
        # key = key is the index of a community
        # value = each index of the list is the index of a subset of k nodes
        self.FGHC = {}
    '''
    Parameters:
            C: list of nodes that represent a community
            group: list of nodes that are "central" nodes for which we compute the measure
    '''
    # Compute the Group Harmonic Centrality between the community and the group
    def HarmonicOfGroupOnSubsets(self,C, group):

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

                distances.append(1./min_distance)
            else:
                distances.append(0.0)
        return(sum(distances))


    '''
    Parameters:
                S: list of nodes
    The method for each community computes all the Fair Group Harmonic Centrality wrt each group of k nodes in S 
    If such set is not given, it computes all the possible subsets of k nodes in the network using the networkit algorithm
    '''
    def computeFairGroupHarmonicCentrality(self,S = []):

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
                GHC = self.HarmonicOfGroupOnSubsets(community,group)
                if(GHC >0):
                    self.FGHC[i].append(GHC * (1./(len((set(community) - set(group))))))
                else:
                    self.FGHC[i].append(GHC)
            i+=1


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
