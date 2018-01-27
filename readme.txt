Python Files
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
        in the constructor, and implements 2 instance methods for creating graphs:

        builder.GraphBuilder.getTabletGraph( useWeights = True, keepEdgeLabels = False)
        builder.GraphBuilder.getNameGraph(useWeights = True, keepEdgeLabels = False)

        Both methods take 2 optional arguments, which determine if edge weights
        should be included (defaults to True) and if edges should be labeled by
        the id's of the things that caused that link to exist (defaults to False).

        Both methods return a networkx.Graph:
          https://networkx.github.io/documentation/stable/reference/classes/graph.html

        getTabletGraph creates the graph where nodes are tablets and tablets are
        joined by an edge if they both contain the same name.  Edge weights in
        this graph are the number of names the joined tablets share, and edges can
        be label by the id's of those names.

        getNameGraph creates the graph where nodes are names and are two names are
        joined by an edge if those names appear on the same tablet.  Weights in
        this graph are the number of tablets on which the pair of names occur
        together, and edges can be labeled by the id's of the tablets on which both
        names appear.

        GraphBuilder instances have non-trivial memory footprint and should be
        deleted once the desired graphs have been built.

  csvWrapper.py
    Demo of a subclass of builder.DataWrapper, can be used with DemoGraph.csv to
    build simple graph for testing.

  garshanaWrapper.py
    Contains GarshanaCsvWrapper, a subclass of builder.DataWrapper.  Used to
    interpret the data from the original csv version of the Garshana corpus we
    created last quarter (Attestations.csv, also included in this repo)

  garrshanaToGexf.py
    Uses builder module and built-in NetworkX functionality to convert Garshana
    data into gexf file format for use with Gephi.  Also serves as an example of
    usage of the module.

Data Files:
  DemoGraph.csv - simple representation of a small graph for testing with csvWrapper.py
  DemoGraphExpected.pdf - Diagram of expected results for DemoGraph.csv
  Attestations.csv - Data for Garshana corpus, in csv form, from last quarter.
  pip-dependancies.txt - output of pip freeze, a description of required python
    modules for this project.
