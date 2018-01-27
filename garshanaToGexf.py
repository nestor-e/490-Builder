#!/usr/bin/python

from builder import GraphBuilder
from garshanaWrapper import GarshanaCsvWrapper
import networkx as nwx

dataSource = GarshanaCsvWrapper('Attestations.csv')
gFact = GraphBuilder(dataSource)
tabGraph = gFact.getTabletGraph()
nwx.write_gexf(tabGraph, 'GarshanaTabletGraph.gexf')
del tabGraph
nameGraph = gFact.getNameGraph()
nwx.write_gexf(nameGraph, 'GarshanaNameGraph.gexf')
