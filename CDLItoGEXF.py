#!/usr/bin/python
from builder import GraphBuilder
from CdliWrapper import CdliWrapper
import networkx as nwx
import sys
#
# dataSource = GarshanaCsvWrapper('Attestations.csv')
# gFact = GraphBuilder(dataSource)
# tabGraph = gFact.getTabletGraph()
# nwx.write_gexf(tabGraph, 'GarshanaTabletGraph.gexf')
# del tabGraph
# nameGraph = gFact.getNameGraph()
# nwx.write_gexf(nameGraph, 'GarshanaNameGraph.gexf')
def main(data, names):
    wrapper = CdliWrapper(data, names)
    build = GraphBuilder(wrapper)
    tabGraph = build.getTabletGraph()
    nwx.write_gexf(tabGraph, 'CdliTabletGraph.gexf')
    del tabGraph
    nameGraph = build.getNameGraph()
    nwx.write_gexf(nameGraph, 'CdliNameGraph.gexf')


if __name__ == '__main__':
    fData = sys.argv[1]
    if len(sys.argv) > 2:
        fName = sys.argv[2]
    else:
        fName = None
    main(fData, fName)
