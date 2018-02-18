import networkx as nwx
from progressbar import ProgressBar as Pb
import CdliWrapper


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

    @staticmethod
    def settify(dictOfItterables):
        r = {}
        for key in dictOfItterables:
            r[key] = set(dictOfItterables[key])
        return r

    @staticmethod
    def buildInverse(dictOfSets):
        r = {}
        for key in dictOfSets:
            for value in dictOfSets[key]:
                if value not in r:
                    r[value] = set()
                r[value].add(key)
        return r

    @staticmethod
    def degreeCheck(actual, minD, maxD):
        return (minD == None or actual >= minD) and (maxD == None or actual <= maxD)

    @staticmethod
    def filterConnections(connections, minConDegree, maxConDegree):
        r = {}
        b = Pb()
        for con in b(connections):
            deg = len(connections[con])
            if GraphBuilder.degreeCheck(deg, minConDegree, maxConDegree):
                r[con] = set(connections[con])

        return r

    @staticmethod
    def filterVert(verticies, connections, minVertDegree, maxVertDegree):
        r = {}
        b = Pb()
        for v in b(verticies):
            adj = set()
            attest = set()
            for con in verticies[v]:
                if con in connections:
                    attest.add(con)
                    for otherV in connections[con]:
                        if otherV != v:
                            adj.add(otherV)
            if GraphBuilder.degreeCheck(len(adj), minVertDegree, maxVertDegree):
                r[v] = attest
        return r


    def __init__(self, dbSource):
        self._db = dbSource
        self._names = None
        self._tabs = None
        self._populate()

    def _populate(self):
        try:
            print "Loading data from wrapper..."
            names = self._db.attestationTableByName()
            tablets = self._db.attestationTableByTablet()
            print "Done."
        except AttributeError:
            print "Supplied data source not of correct type"
            raise

        if names == None and tablets == None:
            print "Supplied data source returns no data"
            raise RuntimeError()

        if names != None:
            print "Reading names..."
            names = GraphBuilder.settify(names)
            print "Done."
        if tablets != None:
            print "Reading tablets..."
            tablets = GraphBuilder.settify(tablets)
            print "Done."

        if tablets == None:
            print "Generating tablets from names..."
            tablets = GraphBuilder.buildInverse(names)
            print "Done."
        if names == None:
            print "Generating names from tablets..."
            names = GraphBuilder.buildInverse(tablets)
            print "Done."

        self._tabs = tablets
        self._names = names

    @staticmethod
    def buildGraph(verticies, connections, useWeights=True, minConDegree=None,
                    maxConDegree=None, minVertDegree=None, maxVertDegree=None):
        print "Filtering connections..."
        connections = GraphBuilder.filterConnections(connections, minConDegree, maxConDegree)
        print "Filtering verticies..."
        verticies = GraphBuilder.filterVert(verticies, connections, minVertDegree, maxVertDegree)
        vList = sorted([vId for vId in verticies])

        G = nwx.Graph()
        print "Building graph..."
        b = Pb()
        for v in b(vList):
            G.add_node(v)
            edges = {}
            for con in verticies[v]:
                for otherV in connections[con]:
                    if otherV < v and otherV in verticies:
                        if otherV not in edges:
                            edges[otherV] = 0
                        edges[otherV] += 1
            for otherV in edges:
                if useWeights:
                    G.add_edge(v, otherV, weight=edges[otherV])
                else:
                    G.add_edge(v, otherV)

        return G

    def buildNameGraph(self, useWeights=True, minConDegree=None, maxConDegree=None,
                        minVertDegree=None, maxVertDegree=None):
        return self.buildGraph(self._names, self._tabs, useWeights, minConDegree, maxConDegree,
                        minVertDegree, maxVertDegree)


    def buildTabletGraph(self, useWeights=True, minConDegree=None, maxConDegree=None,
                        minVertDegree=None, maxVertDegree=None):
        return self.buildGraph(self._tabs, self._names, useWeights, minConDegree, maxConDegree,
                        minVertDegree, maxVertDegree)


def main():
    path = '../snerData/atf_parsed.json'
    w = CdliWrapper.CdliWrapper(path)
    gb = GraphBuilder(w)
    G = gb.buildNameGraph(minVertDegree=3, maxVertDegree=600, minConDegree=2, maxConDegree=20)

if __name__ == '__main__':
    main()
