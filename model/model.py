import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._nodes = DAO.getAllNodes()
        self._idMapAO = {}
        for n in self._nodes:
            self._idMapAO[n.object_id] = n

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
