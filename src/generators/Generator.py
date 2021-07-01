from src.generators.graphs.SBM import SBM
from src.generators.graphs.ErdosRenyi import ErdosRenyi
from src.generators.graphs.BarabasiAlbert import BarabasiAlbert


class Generator:

    def __init__(self,instance,outPath = "./"):
        self.instance = instance
        self.outPath = outPath

    def run(self):

        for elem in self.instance:


