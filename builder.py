import networkx as nwx
import dbWrapper
import dbWrapperCSV as dbc


class GraphBuilder:

    def __init__(self, dbSource):
        self._db = dbSource
        self._names = None
        self._tabs = None
        self._nEdges = None
        self._tEdges = None
        self._vertsBuilt = False
        self._tEdgesBuilt = False
        self._nEdgesBuilt = False

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

    def _buildVertex(self):
        if not self._vertsBuilt:
            self._names  = self._db.attestationTableByName()
            self._tabs = self._db.attestationTableByTablet()
            if (not self._names) and (not self._tabs):
                print "Data source not sufficent"
                return
            elif not self._names:
                self._names = self._inferOccurances(self._tabs)
            elif not self._tabs:
                self._tabs = self._inferOccurances(self._names)
            self._vertsBuilt = True



    def _buildTabEdges(self):
        if self._vertsBuilt and not self._tEdgesBuilt:
            self._tEdges = self._buildEdges(self._tabs, self._names)
            self._tEdgesBuilt = True

    def _buildNameEdges(self):
        if self._vertsBuilt and not self._nEdgesBuilt:
            self._nEdges = self._buildEdges(self._names, self._tabs)
            self._nEdgesBuilt = True

    def _buildEdges(self, verts, other):
        edges = {}
        for v1 in verts:
            for ref in verts[v1]:
                for v2 in other[ref]:
                    self._updateEdge(v1, v2, ref, edges)
        return edges

    @staticmethod
    def _updateEdge(v1, v2, link, edgeSet):
        if v1 < v2:
            key = (v1, v2)
            if key in edgeSet:
                edgeSet[key]['weight'] += 1
                edgeSet[key]['linkedBy'].append(link)
            else:
                edgeSet[key] = {'weight' : 1, 'linkedBy' : [link]}

    def _buildGraph(self, verts, edges, useWeights, keepEdgeLabels):
        vSet = [vId for vId in verts]
        eSet = []
        if useWeights or keepEdgeLabels:
            for edge in edges:
                edgeData = {}
                if useWeights:
                    edgeData['weight'] = edges[edge]['weight']
                if keepEdgeLabels:
                    edgeData['linkedBy'] = edges[edge]['linkedBy']
                eSet.append( ( edge[0], edge[1], edgeData))
        else:
            eSet = [ edge for edge in edges]
        g = nwx.Graph()
        g.add_nodes_from(vSet)
        g.add_edges_from(eSet)
        return g

    def getTabletGraph(self, useWeights = True, keepEdgeLabels = False):
        self._buildVertex()
        self._buildTabEdges()
        if not (self._tEdgesBuilt and self._vertsBuilt):
            print "Error: could not build graph"
            return None
        return self._buildGraph(self._tabs, self._tEdges, useWeights, keepEdgeLabels)


    def getNameGraph(self, useWeights = True, keepEdgeLabels = False):
        self._buildVertex()
        self._buildNameEdges()
        if not (self._nEdgesBuilt and self._vertsBuilt):
            print "Error: could not build graph"
            return None
        return self._buildGraph(self._names, self._nEdges, useWeights, keepEdgeLabels)

def main():
    db = dbc.CsvWrapper('testGraph.csv')
    gb = GraphBuilder(db)
    G = gb.getTabletGraph()


if __name__ == "__main__":
    main()
