from builder import DataWrapper


# Sample DataWrapper class
#  Loads data from a .csv file where each row represents a tablet,
#   the first item in that row is the Id for that tablet, and each
#   subsiquent item in the row is a nameId appearing on that tablet
class CsvWrapper(DataWrapper):

    def __init__(self, filename):
        self.input = {}
        f = open(filename, 'r')
        delim = ','
        for line in f:
            cells = line.split(delim)
            for i in range(len(cells)):
                cells[i] = cells[i].strip()
            self.input[cells[0]] = cells[1:]
        f.close()

    def getTablets(self):
        return [r for r in self.input]

    def namesAppearingOn(self, tablet):
        if tablet in self.input:
            return self.input[tablet]
        else:
            return []

    def attestationTableByTablet(self):
        return self.input
