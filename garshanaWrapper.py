import csv
from builder import DataWrapper


#   Data wrapper for the csv version of the Garshana corpus from last quarter
class GarshanaCsvWrapper(DataWrapper):
    tIdKey = 'Id BDTNS'
    nIdKey = 'Id PN/GN as attested'
    nIdKeyNorm = 'Id PN/GN normalized'

    def __init__(self, filename, normalize = False):
        nameTable = {}
        tabTable = {}
        if normalize:
            nKey = self.nIdKeyNorm
        else:
            nKey  = self.nIdKey
        with open(filename, 'r') as f:
            r = csv.DictReader(f)
            for row in r:
                tab = row[self.tIdKey]
                name = row[nKey]
                if tab not in tabTable:
                    tabTable[tab] = []
                if name not in nameTable:
                    nameTable[name] = []
                if name not in tabTable[tab]:
                    tabTable[tab].append(name)
                if tab not in nameTable[name]:
                    nameTable[name].append(tab)
        self.nameTable = nameTable
        self.tabTable = tabTable


    # Returns a dictionary maping each tablet to a list of names appearing on it
    # { TabletId : [NameId_1, NameId_2, ..] , ... }
    def attestationTableByTablet(self):
        return self.tabTable

    # Returns a dictionary maping each name to a list of tablets it appears on
    # { NameId : [TabletId_1, TabletId_2, ..] , ... }
    def attestationTableByName(self):
        return self.nameTable
