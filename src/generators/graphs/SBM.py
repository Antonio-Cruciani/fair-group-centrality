import networkit as nk

class SBM():

    def __init__(self, n, p, q, number_of_communities):


        self.n = n
        self.p = p
        self.q = q
        self.k = number_of_communities
        self.clustered =  nk.generators.ClusteredRandomGraphGenerator(self.n,self.k,self.p,self.q)
        self.G =self.clustered.generate()
        self.communities = self.computeCommuniteis()

    def computeCommuniteis(self):
        C = self.clustered.getCommunities()
        idCommunities = C.getSubsetIds()
        Communities = []
        for id in idCommunities:
            Communities.append(list(C.getMembers(id)))
        return Communities
    def get_communities(self):
        return(self.communities)
    def get_n(self):
        return self.n

    def get_p(self):
        return self.p
