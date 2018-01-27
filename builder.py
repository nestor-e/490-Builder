import networkx as nwx


#  Base wrapper class for datasources to build graphs from.
#  A subclass must implement at least one of:
#       1) attestationTableByTablet()
#       2) attestationTableByName()
#       3) getNames()  and  tabletsOnWhichAppears(name)
#       4) getTablets()  and  namesAppearingOn(tablet)
#  GraphBuilder can construct 2 from 1 and vice-versa in O(n) where n is the
#   the total number of attestations, so don't put to much work into implementing
#   multiple options
# TODO: Make consistant for names/tablets isolated in the graph
#       Currently they will be included if returned dy dataWrapper but not if GraphBuilder needs to infer them
#       For our purposes they never matter, so perhaps they shold be filtered out at some point
class DataWrapper:
    # Returns a list of all tablets in datasource
    def getTablets(self):
        return None

    # Returns a list of all names in datasource
    def getNames(self):
        return None

    # Returns a list of all names appearing on the given tablet
    def namesAppearingOn(self, tablet):
        return None

    # Returns a list of all tablets on wich the given name appears
    def tabletsOnWhichAppears(self, name):
        return None

    # Returns a dictionary maping each tablet to a list of names appearing on it
    # { TabletId : [NameId_1, NameId_2, ..] , ... }
    def attestationTableByTablet(self):
        tabs = self.getTablets()
        if not tabs:
            return None
        table = {}
        for t in tabs:
            table[t] = self.namesAppearingOn(t)
        return table

    # Returns a dictionary maping each name to a list of tablets it appears on
    # { NameId : [TabletId_1, TabletId_2, ..] , ... }
    def attestationTableByName(self):
        names = self.getNames()
        if not names:
            return None
        table = {}
        for n in names:
            table[n] = self.tabletsOnWhichAppears(n)
        return table



# Factory class for building NetworkX graphs from a DataWrapper
# Has non-trivial memory footprint and should be deleted once desired graphs are built
class GraphBuilder:
    # Constructor requires a single argument, An instance of DataWrapper from
    # which to draw data
    weightLabel = 'weight'
    linkLabel = 'linkedBy'

    def __init__(self, dbSource):
        self._db = dbSource
        self._names = None
        self._tabs = None
        self._nEdges = None
        self._tEdges = None
        self._vertsBuilt = False
        self._tEdgesBuilt = False
        self._nEdgesBuilt = False



    # Can infer names from there occuraces on tablets and vice-versa
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

    @staticmethod
    def _updateEdge(v1, v2, link, edgeSet):
        if v1 < v2:
            key = (v1, v2)
            if key in edgeSet:
                edgeSet[key][GraphBuilder.weightLabel] += 1
                edgeSet[key][GraphBuilder.linkLabel].append(link)
            else:
                edgeSet[key] = {GraphBuilder.weightLabel : 1, GraphBuilder.linkLabel : [link]}




    def _buildVertex(self):
        if not self._vertsBuilt:
            try:
                self._names  = self._db.attestationTableByName()
                self._tabs = self._db.attestationTableByTablet()
            except AttributeError:
                print "Error: Supplied data source of wrong type"
                raise
            if (not self._names) and (not self._tabs):
                print "Error: Data source returns no data"
                return
            elif not self._names:
                self._names = self._inferOccurances(self._tabs)
            elif not self._tabs:
                self._tabs = self._inferOccurances(self._names)
            self._vertsBuilt = True




    def _buildEdges(self, verts, other):
        edges = {}
        for v1 in verts:
            for ref in verts[v1]:
                for v2 in other[ref]:
                    self._updateEdge(v1, v2, ref, edges)
        return edges

    def _buildTabEdges(self):
        if self._vertsBuilt and not self._tEdgesBuilt:
            self._tEdges = self._buildEdges(self._tabs, self._names)
            self._tEdgesBuilt = True

    def _buildNameEdges(self):
        if self._vertsBuilt and not self._nEdgesBuilt:
            self._nEdges = self._buildEdges(self._names, self._tabs)
            self._nEdgesBuilt = True





    def _buildGraph(self, verts, edges, useWeights, keepEdgeLabels):
        vSet = [vId for vId in verts]
        eSet = []
        if useWeights or keepEdgeLabels:
            for edge in edges:
                edgeData = {}
                if useWeights:
                    edgeData[self.weightLabel] = edges[edge][self.weightLabel]
                if keepEdgeLabels:
                    edgeData[self.linkLabel] = edges[edge][self.linkLabel]
                eSet.append( ( edge[0], edge[1], edgeData) )
        else:
            eSet = [ edge for edge in edges]
        g = nwx.Graph()
        g.add_nodes_from(vSet)
        g.add_edges_from(eSet)
        return g


    #  Returns a NetworkX graph ( networkx.Graph ) representing the associations between tablets
    #  takes 2 optional named boolean parameters:
    #   useWeights : to indicate wether the resulting graph should have edge weights
    #       Stored in NetworkX graph with key GraphBuilder.weightLabel
    #   keepEdgeLabels : to indicate wether edges shoould be labeled by the names that associate them
    #       Stored in NetworkX graph with key GraphBuilder.linkLabel
    def getTabletGraph(self, useWeights = True, keepEdgeLabels = False):
        self._buildVertex()
        self._buildTabEdges()
        if not (self._tEdgesBuilt and self._vertsBuilt):
            print "Error: could not build graph"
            return None
        return self._buildGraph(self._tabs, self._tEdges, useWeights, keepEdgeLabels)


    #  Returns a NetworkX graph ( networkx.Graph ) representing the associations between names
    #  takes 2 optional named boolean parameters:
    #   useWeights : to indicate wether the resulting graph should have edge weights
    #       Stored in NetworkX graph with key GraphBuilder.weightLabel
    #   keepEdgeLabels : to indicate wether edges shoould be labeled by the tablets that associate them
    #       Stored in NetworkX graph with key GraphBuilder.linkLabel
    def getNameGraph(self, useWeights = True, keepEdgeLabels = False):
        self._buildVertex()
        self._buildNameEdges()
        if not (self._nEdgesBuilt and self._vertsBuilt):
            print "Error: could not build graph"
            return None
        return self._buildGraph(self._names, self._nEdges, useWeights, keepEdgeLabels)
