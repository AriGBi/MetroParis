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


        tic = datetime.now()
        self.addEdges3()
        toc = datetime.now()
        print("Tempo modo 3:", toc - tic)

    def buildGraphPesato(self):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._fermate)
        self.addEdgesPesati()

    def addEdgesPesati(self):
        allEdges = DAO.getAllEdges()
        for edge in allEdges:
            u = self._idMapFermate[edge.id_stazP]
            v = self._idMapFermate[edge.id_stazA]
            if self._grafo.has_edge(u, v): #se il grafo ha già un arco tra u e v, modifico il suo peso
                self._grafo[u][v]["weight"] += 1
            else: #se l'arco non c'era già, devo crearlo
                self._grafo.add_edge(u, v, weight=1)

    def addEdgesPesatiV2(self):
        allEdgesPesati= DAO.getAllEdgesPesati()
        for e in allEdgesPesati:
            self._grafo.add_edge(self._idMapFermate[e[0]],self._idMapFermate[e[1]],weight=e[2])

    def getArchiPesoMaggiore(self):
        edges= self._grafo.edges(data=True) #data=True per prendere anche i pesi
        res=[]
        for e in edges:
            if self._grafo.get_edge_data(e[0],e[1])["weight"]>1:
                res.append(e)
        return res

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
            self._grafo.add_edge(u,v) #add_edge non aggiunge un arco se è già presente!! Noi in realtà abbiamo delle fermate collegate da piu linee

    def getBFSNodesFromTree(self, source):
        """Cerco l'albero di visita che viene fuori con BFS. L'utente mi dice da dove partire, selezionando la stazione"""
        tree=nx.bfs_tree(self._grafo, source) #questo metodo calcola l'albero del grafo a partire dal nodo source
        #tree è comunque un GRAFO che avrà archi e nodi
        archi = list(tree.edges())
        nodi= list(tree.nodes())
        return nodi[1:] #tolgo il nodo da cui parto

    def getDFSNodesFromTree(self, source):
        tree=nx.dfs_tree(self._grafo, source)
        nodi= list(tree.nodes())
        return nodi[1:]

    def getBFSNodesFromEdges(self, source):
        archi= nx.bfs_edges(self._grafo, source) #archi di VISITA --> tuple coppie di nodi
        res=[]
        for u,v in archi: #(u,v)
            res.append(v) #prendo solo i nodi di arrivo dei vari archi
        return res

    def getDFSNodesFromEdges(self, source):
        tree=nx.dfs_edges(self._grafo, source)
        res=[]
        for u,v in tree:
            res.append(v)
        return res



    @property
    def fermate(self):
        return self._fermate

    def getNumNodi(self):
        return len(self._grafo.nodes)

    def getNumArchi(self):
        return len(self._grafo.edges)
