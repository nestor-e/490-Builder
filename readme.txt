Python Files

Note:: Now requires package progressbar2

  builder.py
    Contains a python module for creating NetworkX graph of co-occurrences of names
    and tablets in a way which is flexible for different data sources.

    Consists of 2 Classes:

    1: builder.DataWrapper
        Base class which will need to be extended for each data source we want to use.
        Defines a set of basic data queries from which the graph can be built.
        See comments in builder.py for details on implementing subclass or csvWrapper.py
        or garshanaWrapper.py for example subclasses.

    2: builder.GraphBuiilder
        Factory object for constructing graphs.  Takes an instance of builder.DataWrapper
        in the constructor, and implements 3 instance methods for creating graphs:

        buildNameGraph( useWeights=True, minConDegree=None, maxConDegree=None,
                        minVertDegree=None, maxVertDegree=None)

        buildTabletGraph( useWeights=True, minConDegree=None, maxConDegree=None,
                          minVertDegree=None, maxVertDegree=None)

        buildMultiLevelGraph( minDegree=None, maxDegree=None)

        buildNameGraph and buildTabletGraph methods take the following optional
        arguments:

            - useWeight :  Determines if the output graph should be weighted or
                            unweighted.  Defualts to weighted.

            - minConDegree/maxConDegree : minimum/maximum allowed degree for the
                objects responsible for creating connections between the nodes.
                For example, in buildTabletGraph, only names with degree between
                minConDegree and maxConDegree would be considered when creating
                edges between tablets.  Defualt is None, which causes no filtering
                to occur.

            - minVertDegree/maxVertDegree : minimum/maximum allowed degree for
                nodes in the final graph.  All nodes with degree outside these
                bounds will be removed, as will edges incident to them.  Defualt
                is None, which causes no filtering to occur.

        buildMultiLevelGraph returns an unweighted graph containing both names and
        tablets as nodes.  Each node in the graph is labeled as either a name or
        a tablet.  buildMultiLevelGraph takes the following optional arguments:

            - minDegree/maxDegree : minimum/maximum allowed degree for
                nodes in the final graph.  All nodes with degree outside these
                bounds will be removed, as will edges incident to them.  Defualt
                is None, which causes no filtering to occur.

        All methods return a networkx.Graph:
          https://networkx.github.io/documentation/stable/reference/classes/graph.html

        buildTabletGraph creates the graph where nodes are tablets and tablets are
        joined by an edge if they both contain the same name.  Edge weights in
        this graph are the number of names the joined tablets share.

        buildNameGraph creates the graph where nodes are names and are two names are
        joined by an edge if those names appear on the same tablet.  Weights in
        this graph are the number of tablets on which the pair of names occur
        together.

        buildMultiLevelGraph creates a graph with both names and tablets as nodes.
        Edges are unweighted, and join a tablet to a name if the name appears on
        that tablet.

  csvWrapper.py
    Demo of a subclass of builder.DataWrapper, can be used with DemoGraph.csv to
    build simple graph for testing.

  garshanaWrapper.py
    Contains GarshanaCsvWrapper, a subclass of builder.DataWrapper.  Used to
    interpret the data from the original csv version of the Garshana corpus we
    created last quarter.

  CdliWrapper.py
    Containd CdliWrapper, a subclass of builder.DataWrapper.  Used to feed json
    results from sner into GraphBuilder.

  garrshanaToGexf.py
    Uses builder module and built-in NetworkX functionality to convert Garshana
    data into gexf file format for use with Gephi.  Also serves as an example of
    usage of the module.

  CDLItoGEXF.py
    Uses builder module to create some graphs from CDLI data.  Uses some arbitrary
    degree limits for tablet graph since building entire structure is very memory
    intensive.

Data Files:
  DemoGraph.csv - simple representation of a small graph for testing with csvWrapper.py
  DemoGraphExpected.pdf - Diagram of expected results for DemoGraph.csv
  pip-dependancies.txt - output of pip freeze, a description of required python
    modules for this project.
