import networkit as nk
from src.generators.graphs.structure.community import community

class SBM(community):

    def __init__(self, n, p, q, number_of_communities):

        self.n = n
        self.p = p
        self.q = q
        self.k = number_of_communities
        self.clustered =  nk.generators.ClusteredRandomGraphGenerator(self.n,self.k,self.p,self.q)
        self.G =self.clustered.generate()

        #self.communities = self.computeCommuniteis()

        super().__init__(self.G, None, [])
        self.set_communities(self.computeCommuniteis())

    def computeCommuniteis(self):
        C = self.clustered.getCommunities()
        idCommunities = C.getSubsetIds()
        Communities = []
        for id in idCommunities:
            Communities.append(list(C.getMembers(id)))
        self.set_communities(Communities)
        return Communities
    #def get_communities(self):
    #    return(self.communities)
    def get_n(self):
        return self.n

    def get_p(self):
        return self.p

    def save_graph(self,outPath="./"):
        if (outPath[-1] != "/"):
            outPath += "/"
        instance = {
            'outPath': outPath,
            'graph':'Stochastic-Block-Model',
            'parameters': {
                'In_p':self.p,
                'Out_p':self.q,
                'Communities':self.k

            }

        }
        self.write_instance(instance)