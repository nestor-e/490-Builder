import networkx as nwx
import dbWrapper


class GraphBuilder:

    def __init__(self, dbSource):
        self.db = dbSource
        self.names = None
        self.tabs = None
        self.nEdges = None
        self.tEdges = None
        self.vertsBuilt = False
        self.tEdgesBuilt = False
        self.nEdgesBuilt = False

    def _buildVertex(self):
        if not self.vertsBuilt:
            self.names  = self.db.attestationTableByName()
            self.tabs = self.db.attestationTableByTablet()
            if (not self.names) and (not self.tabs):
                print "Data source not sufficent"
            elif not self.names:
                self.names = inferOccurances(self.tabs)
            elif not self.tabs:
                self.tabs = inferOccurances(self.names)
            self.vertsBuilt = True

    @staticmethod
    def _inferOccurances(other):
        occ = {}
        for key in other:
            for ref in other[key]:
                if ref in occ:
                    if key not in occ[ref]:
                        occ[ref].append(key)
                else:
                    occ[ref] = [key]
        return occ

    def _buildTabEdges(self):
        if self.vertsBuilt and not self.tEdgesBuilt:
            self.tEdges = self.buildEdges(self.tabs, self.names)
            self.tEdgesBuilt = True

    def _buildNameEdges(self):
        if self.vertsBuilt and not self.nEdgesBuilt:
            self.tEdges = self.buildEdges(self.names, self.tabs)
            self.nEdgesBuilt = True

    def _buildEdges(self, verts, other):
        edges = {}
        for v1 in verts:
            for ref in verts[v1]:
                for v2 in other[ref]:
                    self.updateEdge(v1, v2, edges)
        return edges

    @staticmethod
    def _updateEdge(v1, v2, edgeSet):
        if v1 < v2:
            key = (v1, v2)
            if key in edgeSet:
                edgeSet[key] += 1
            else:
                edgeSet[key] = 1

    def _buildGraph(self, verts, edges, useWeights):
        vSet = [vId for vId in verts]
        eSet = []
        if useWeights:
            eSet = [ (edge[0], edge[1], {'weight' : edges[edge]}) for edge in edges]
        else:
            eSet = [ edge for edge in edges]
        g = nwx.Graph()
        g.add_nodes_from(vSet)
        g.add_edges_from(eSet)
        return g

    def getTabletGraph(self, useWeights = True):
        self.buildVertex()
        self.buildTabEdges()
        if not (self.nTabBuilt and self.vertsBuilt):
            print "Error: could not build graph"
            return None
        return self.buildGraph(self.tabs, self.tEdges, useWeights)


    def getNameGraph(self, useWeights = True):
        self.buildVertex()
        self.buildNameEdges()
        if not (self.nEdgesBuilt and self.vertsBuilt):
            print "Error: could not build graph"
            return None
        return self.buildGraph(self.names, self.nEdges, useWeights)

def main():
    db = dbWrapper.dbWrapper()
    gb = GraphBuilder(db)
    gb.getTabletGraph()


if __name__ == "__main__":
    main()
