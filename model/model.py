import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._nodes = DAO.getAllNodes()
        self._idMapAO = {}
        for n in self._nodes:
            self._idMapAO[n.object_id] = n
        self._optPath = []
        self._optCost = 0

    def getOptPath(self,source,lun):
        self._optPath = []
        self._optCost = 0
        parziale = [source]

        for n in self._graph.neighbors(source):
            if n.classification == parziale[-1].classification:
                parziale.append(n)
                self._ricorsione(parziale,lun)
                parziale.pop()
        return self._optPath,self._optCost

    def _ricorsione(self, parziale, lun):
        if len(parziale) == lun:
            #condizione di terminazione, allora parziale è lunga come lun
            #per cui verifico che questa parziale sia meglio del mio best
            #(condizione di ottimalità), ed in ogni caso esco
            if self._costoPath(parziale) > self._optCost:
                self._optCost = self._costoPath(parziale)
                self._optPath = copy.deepcopy(parziale)
            return
        #se arrivo qui posso aggiungere ancora nodi
        for n in self._graph.neighbors(parziale[-1]):
            if n.classification == parziale[-1].classification:
                parziale.append(n)
                self._ricorsione(parziale, lun)
                parziale.pop()

    def _costoPath(self, path):
        costo = 0
        for i in range(0,len(path)-1):
            costo += self._graph[path[i]][path[i+1]]["weight"]
        return costo

    def buildGraph(self):
        #aggiunge nodi
        self._graph.add_nodes_from(self._nodes)
        #aggunge archi
        self.addEdgesV2()

    def addEdges(self):
        for u in self._nodes:
            for v in self._nodes:
                peso = DAO.getEdgePeso(u,v)
                if peso is not None:
                    self._graph.add_edge(u, v, weight = peso)
                    print(f"Added arco {u} e {v} con peso {peso}")

    def addEdgesV2(self):
        allEdges = DAO.getAllEdges(self._idMapAO)
        for e in allEdges:
            self._graph.add_edge(e.o1, e.o2, weight = e.peso)

    def getNumNodes(self):
        return len(self._graph.nodes)

    def getNumEdges(self):
        return len(self._graph.edges)

    def getInfoCompConnessa(self,id_oggetto):
        #cercare componente connessa che contiene id_oggetto
        if not self.hasNode(id_oggetto):
            return None
        source = self._idMapAO[id_oggetto]
        #con dfs tree
        dfsTree = nx.dfs_tree(self._graph, source)
        print("Size connessa con dfs_tree", len(dfsTree.nodes()))
        #con predecessori
        dfsPred = nx.dfs_predecessors(self._graph, source)
        print("Size connessa con dfs predecessors", len(dfsPred.values())) #di uno più piccoli perchè non prende source
        #strategia 3
        conn = nx.node_connected_component(self._graph, source)
        print("Size connessa con node_connected_component", len(conn))
        return len(conn)

    def hasNode(self,id_oggetto):
        return id_oggetto in self._idMapAO

    def getNodeFromId(self,id_oggetto):
        return self._idMapAO[id_oggetto]
