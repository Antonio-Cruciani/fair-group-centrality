import itertools
from src.generators.graphs.SBM import SBM
from src.generators.graphs.ErdosRenyi import ErdosRenyi
from src.generators.graphs.BarabasiAlbert import BarabasiAlbert
class Harmonic:

    #instance= {
        # type = "Syntetic or Real"
        # graphs = [{ "name": , "parameters":{" "}   }]


    # }
    def __init__(self,instance):

        self.instance = instance


    def run(self):

        if(self.instance['type'] in ['syntetic','Syntetic']):
            self.runSynteticExperiments()

    # Method that load the datasets and run the experiments

    def runSynteticExperiments(self):

        for elem in self.instance['graphs']:


            listOfParameters = []

            for parameter in self.instance['graphs'][elem]:

                listOfParameters.append(parameter)

            parametersCombination =list(itertools.product(*listOfParameters))
            paraKeys = list(self.instance['graphs'][elem].keys())
            # Loading the graphs
            if(elem in ['Erdos-Renyi','ER','er','Erdos Renyi','ErdosRenyi']):
                j = 0
                for para in
            elif(elem in ['Barabasi-Albert','BA','ba','BarabasiAlbert','Barabasi Albert']):

            elif(elem in ['SBM','sbm']):



