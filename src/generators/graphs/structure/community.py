import random as rnd
import networkit as nk

# Object community that given a networkit graph builds\retrieve communities
class community():
    '''
    Parameters:
        G: Networkit Graph
        structure: String that defines the technique for building the communities
                   it can have: BFS,RND
                   If not declared you need to call the community detection method to define the communities.
        size: List that defines the number of the communities that you want to define.
              NOTE: in this version 0.1a of the code all the communities are built automatically without the need of the sizes
              HOW TO USE IT: set size = []
        threshold: Integer that defines the max number of nodes in each community using the BFS method.
    '''
    def __init__(self, G, structure, size,threshold = None):

        self.G = G
        self.structure = structure
        self.size = size
        self.number = len(size)
        self.nodes = [v for v in self.G.iterNodes()]
        self.edges = [e for e in self.G.iterEdges()]
        self.communities = []
        self.detectedCommunities = []
        self.threshold = threshold

    '''
    Method that calls the community builder method 
    NOTE: After defining the object call .run() for building the communities.  
    '''
    def run(self):
        if (self.structure in ['random', 'Random', 'RANDOM','rnd','rd']):
            self.assignRandomCommunities()
        elif (self.structure in ['BFS', 'bfs']):
            self.samplingBFSCommunities()
        else:
            print("CIAO")
            #self.communities = []
    '''
    Parameters:
        algorithm: string value that defines the community detection algorithm to use 
                    standard: default algorithm used by networkit
                    plm: uses the plm algorithm
                    plp: uses the plp algorithm
    '''
    def communityDetection(self, algorithm="standard"):
        if (algorithm in ['standard', 'Standard', 'STANDARD']):
            communities = nk.community.detectCommunities(self.G)
        elif (algorithm in ['PLM', 'plm']):
            communities = nk.community.detectCommunities(self.G, algo=nk.community.PLM(self.G, True))
        elif (algorithm in ['PLP', 'plp']):
            communities = nk.community.detectCommunities(self.G, algo=nk.community.PLP(self.G))
        for setIndex in communities.getSubsetIds():
            self.detectedCommunities.append(list(communities.getMembers(setIndex)))

    '''
      Method to be checked do not use it
    '''
    def computeBFSCommunities(self):

        nodes = self.nodes
        seeds = rnd.sample(nodes, self.number)
        graph = self.G
        j = 0
        for seed in seeds:
            bfs = nk.distance.BFS(graph, seed, storePaths=True, storeNodesSortedByDistance=True).run()
            sorted_by_distance = bfs.getNodesSortedByDistance()
            self.communities.append(sorted_by_distance[0:self.size[j]])
            new_nodes = set(nodes) - set(sorted_by_distance[0:self.size[j]])
            nodes = list(new_nodes)
            graph = nk.graphtools.subgraphFromNodes(self.G, nodes)
            j += 1
        # If the method did not assign all the nodes to a community, assign the remaining at random to the communities that have
        # size less than the desidered target size.
        if (len(nodes) != 0):
            j = 0
            for elem in self.communities:
                if (len(elem) != self.size[j]):
                    target_size = self.size[j] - len(elem)
                    new_nodes = rnd.sample(nodes, target_size)
                    self.communities[j].extend(new_nodes)
                    updates = set(nodes) - set(new_nodes)
                    nodes = list(updates)
                j += 1
    '''
    Method that iteratively computes the communities via BFS method
    '''
    def samplingBFSCommunities(self):
        nodes = self.nodes
        graph = self.G
        while(len(nodes)>0):
            seed =  rnd.sample(nodes, 1)[0]
            bfs = nk.distance.BFS(graph, seed, storePaths=True, storeNodesSortedByDistance=True).run()
            sorted_by_distance = bfs.getNodesSortedByDistance()
            i = 0
            community = []
            while(i<self.threshold and i<len(sorted_by_distance)):
                community.append(sorted_by_distance[i])
                i+=1
            new_nodes = set(nodes) - set(community)
            nodes = list(new_nodes)
            graph = nk.graphtools.subgraphFromNodes(self.G, nodes)
            self.communities.append(community)

        self.number = len(self.communities)


    '''
    Method to be checked do not use it
    '''
    def computeRandomCommunities(self):
        nodes = self.nodes
        j = 0
        for k in range(0, self.number):
            self.communities.append(rnd.sample(nodes, self.size[j]))
            new_nodes = set(nodes) - set(self.communities[j])
            nodes = list(new_nodes)
            j += 1
    '''
    Method that computes random communities.
    Each node picks a community between 1 and k u.a.r.
    '''
    def assignRandomCommunities(self):
        for c in range(0,self.number):
            self.communities.append([])
        for u in self.nodes:
            communityIndex = rnd.randint(0, self.number-1)
            self.communities[communityIndex].append(u)

    def get_communities(self):
        return self.communities

    def get_G(self):
        return self.G

    def get_size(self):
        return self.size

    def get_structure(self):
        return self.structure

    def get_detectedCommunities(self):
        return self.detectedCommunities

    def set_communities(self, communities):
        self.communities = communities

    '''
    Parameters: dictionary that contains the graph infos.
                Values:
                    outPath: output path
                    graph: graph type
                    parameters: dictionary of all the parameters of the graph (depends on the type of random graph)
    '''
    def write_instance(self, instance):
        # EdgeListFile

        type = "# Undirected graph: "+instance['outPath'] + str(instance['graph']) + ".ungraph.txt"+"\n"
        name = "# " + str(instance['graph'])+"\n"
        nodes = "# Nodes: " + str(self.G.numberOfNodes()) + " Edges: " + str(self.G.numberOfEdges())+"\n"
        parameters = '# '
        for key in instance['parameters']:

            parameters += key + ": " + str(instance['parameters'][key]) + " "
        parameters+="\n"
        keyVal = "# FromNodeId"+"\t"+"ToNodeId"+"\n"
        f = open(instance['outPath'] +str(instance['graph']) + ".ungraph.txt", "w+")
        f.write(type)
        f.write(name)
        f.write(nodes)
        f.write(parameters)
        f.write(keyVal)
        j = 0
        for edge in self.edges:
            f.write(str(edge[0])+"\t"+str(edge[1]))
            if(j < len(self.edges)):
                f.write("\n")
            j+=1
        f.close()

        # CommunitiesFile
        g = open(instance['outPath'] +str(instance['graph']) + ".all.cmty.txt", "w+")
        j = 0

        for community in self.communities:
            i = 0
            for u in community:
                g.write(str(u))
                if(i <len(community)-1):
                    g.write("\t")
                i+=1
            j+=1
            if(j<len(self.communities)):
                g.write("\n")
        g.close()

