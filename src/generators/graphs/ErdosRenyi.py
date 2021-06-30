import networkit as nk
import random as rnd
from src.generators.graphs.structure.community import community
class ErdosRenyi(community):


    def __init__(self,n,p,communities_number,communities_structure, communities_size = None):

        if(communities_size != None):
            super().__init__(nk.generators.ErdosRenyiGenerator(n,p).generate(),communities_structure,communities_size)
        else:
            # Assuming that n/communities_number give us an int
            cs = [n/communities_number for k in range(0,communities_number)]
            super().__init__(nk.generators.ErdosRenyiGenerator(n,p).generate(),communities_structure,cs)
        self.n = n
        self.p = p

    def get_n(self):
        return self.n
    def get_p(self):
        return self.p




