import itertools
import networkit as nk
import logging
import time
import random
logging.basicConfig(level=logging.DEBUG)
class GroupHarmonicCentrality:

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

    def computeGroupsCentralities(self):
        if(self.S == None):
            logging.debug("Computing all the subsets of %r nodes"%(self.k))
            logging.debug("Advice: get a coffee..")
            start_groups = time.time()
            self.groups = self.findsubsets(self.nodes,self.k)
            end_groups = time.time()
            logging.debug("Elapsed time = %r"%(end_groups-start_groups))
            logging.debug("Number of groups = %r"%(len(self.groups)))
        self.groups_centralities = []
        for group in self.groups:
            self.groups_centralities.append(self.HarmonicOfGroup(group))

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

    def sampleS(self,numberOfSets = 1):
        S = []
        for i in range(0,numberOfSets):
            S.append(random.sample(self.nodes, self.k))
        self.S = S
        self.groups = S

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


class FairGroupHarmonicCentrality(GroupHarmonicCentrality):
    def __init__(self, G,C, k):
        super().__init__(G, k)
        # Fair Group Harmonic Centrality
        self.communities = C
        # Dictionary <key,value> <---- <int,list>
        # key = key is the index of a community
        # value = each index of the list is the index of a subset of k nodes
        self.FGHC = {}

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



    # for each community computes all the Fair Group Harmonic Centrality wrt each group of k nodes
    # If such set is not given, it exhaustively computes all the possible subsets of k nodes in the network
    def computeFairGroupHarmonicCentrality(self,S = []):

        if(not (S or self.S)):
            self.compute_groups_centralities()

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

    def sampleInEachCommunity(self):
        S = []
        for community in self.communities:
            S.append(random.sample(community, 1)[0])
        self.S = S

    # HEURISTIC: For each community take the node that has highest intra-degree
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

    # HEURISTIC: For each community take the node with highest intra-harmonic centrality
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






