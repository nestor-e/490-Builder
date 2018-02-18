import json
import progressbar
import sys


def loadData(fName):
    print "Loading data"
    with open(fName, 'r') as f:
        data = json.load(f)
    return data

def readAttest(data):
    tabs = {}
    print "Reading attestations"
    b = progressbar.ProgressBar()
    for tab in b(data):
        tId = tab['idCDLI']
        for side in tab['sides']:
            for region in side['content']:
                for line in region['lines']:
                    if 'attestations' in line:
                        if tId not in tabs:
                            tabs[tId] = set()
                        for name in line['attestations']:
                            tabs[tId].add(name)
    return tabs


def compileNames(tablets):
    names = {}
    print "Compiling names"
    b = progressbar.ProgressBar()
    for tId in b(tablets):
        for nId in tablets[tId]:
            if nId not in names:
                names[nId] = set()
            if tId not in names[nId]:
                names[nId].add(tId)
    return names


def countEdges(verticies, connections, minDegree=None, maxDegree=None):
    sVert = sorted([i for i in verticies])
    count = 0
    b = progressbar.ProgressBar()
    for id1 in b(sVert):
        linked = set()
        for con in verticies[id1]:
            for id2 in connections[con]:
                if id1 != id2 and id2 not in linked:
                    linked.add(id2)
        degree = len(linked)
        if (minDegree == None or degree >= minDegree) and (maxDegree == None or degree <= maxDegree):
            for other in linked:
                if other > id1:
                    count += 1
    return count

#  type true - tablet, false - name
def countReport(tabs, names, type, minDegree=None, maxDegree=None):
    if type:
        s1 = "Tablet graph"
    else :
        s1 = "Name graph"

    if minDegree == None and maxDegree == None:
        s2 = "all degrees"
    else:
        s2 = "degree"
        if(minDegree != None):
            s2 = "{} <= {}".format(minDegree, s2)
        if(maxDegree != None):
            s2 = "{} <= {}".format(s2, maxDegree)

    print "\nCounting Edges : {}, {}".format(s1, s2)
    if type:
        n = countEdges(tabs, names, minDegree, maxDegree)
    else:
        n = countEdges(names, tabs, minDegree, maxDegree)
    print "{:,} edges found\n".format(n)

def main(fName):

    data = loadData(fName)
    tabs = readAttest(data)
    names = compileNames(tabs)

    aCount = sum([len(tabs[k]) for k in tabs])

    print "\n\n{:,} tablets total".format(len(data))
    print "{:,} total attestations".format(aCount)
    print "{:,} tablets w/ attestations".format(len(tabs))
    print "{:,} names in attestations\n\n".format(len(names))



    countReport(tabs, names, True)
    countReport(tabs, names, True, maxDegree = 1000)
    
    countReport(tabs, names, False)
    countReport(tabs, names, False, maxDegree = 1000)


if __name__ == "__main__":
    main(sys.argv[1])
