from datetime import datetime

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._fermate = DAO.getAllFermate() #questo metodo resituisce un elenco di tutte le fermate
        self._grafo=nx.DiGraph() #il grafo lo costruisco solo una volta, quindi va bene definirlo nel costruttore
        self._idMapFermate={} #dizionario in cui metto come chiave l'id della fermata e valore l'oggetto fermata
        for f in self._fermate:
            self._idMapFermate[f.id_fermata] = f


    def buildGraph(self):
        #aggiungiamo i nodi
        self._grafo.add_nodes_from(self._fermate)
        #self.addEdges1() #questo metodo ci mette troppo tempo perchè ciclo 2 volte
        # tic=datetime.now()
        # self.addEdges1()
        # toc=datetime.now()
        # print("Tempo modo 1:", toc-tic)

        # self._grafo.clear_edges()
        # tic = datetime.now()
        # self.addEdges2()
        # toc = datetime.now()
        # print("Tempo modo 2:", toc - tic)

        self._grafo.clear_edges()
        tic = datetime.now()
        self.addEdges3()
        toc = datetime.now()
        print("Tempo modo 3:", toc - tic)

    def addEdges1(self):
        """Aggiungo gli archi ciclando con doppio ciclo sui nodi e testando se per ogni coppia esiste una connessione"""
        for u in self._fermate:
            for v in self._fermate:
                if DAO.hasConnessione(u,v):
                    self._grafo.add_edge(u,v)


    def addEdges2(self):
        """ Ciclo solo una volta e faccio una query per trovare tutti i vicini"""
        for u in self._fermate:
            for connessione in DAO.getVicini(u):
                v=self._idMapFermate[connessione.id_stazA] #accedo alla fermata di arrivo tramite la mappa in cui ho id e oggetti. Prendo come id quello della stazione di arrivo della connessione
                self._grafo.add_edge(u,v)


    def addEdges3(self):
        """Faccio una query unica che prende tutti gli archi (connessioni) e poi ciclo qui"""
        allEdges=DAO.getAllEdges()
        for edge in allEdges:
            u= self._idMapFermate[edge.id_stazP]
            v= self._idMapFermate[edge.id_stazA]
            self._grafo.add_edge(u,v)



    @property
    def fermate(self):
        return self._fermate

    def getNumNodi(self):
        return len(self._grafo.nodes)

    def getNumArchi(self):
        return len(self._grafo.edges)
