from builder import DataWrapper
import json
import csv
import sys


class CdliWrapper(DataWrapper):

    def __init__(self, jsonFile, nameLabelsFile=None):
        self.data = {}
        with open(jsonFile, 'r') as jf:
            tablets = json.load(jf)
            for tab in tablets:
                tabId = tab['idCDLI']
                if tabId not in self.data:
                    self.data[tabId] = []
                else:
                    print "Dulicate tablet Id : " , tabId
                for side in tab['sides']:
                    for region in side['content']:
                        for line in region['lines']:
                            if 'attestations' in line:
                                for nId in line['attestations']:
                                    if nId not in self.data[tabId]:
                                        self.data[tabId].append(nId)

        if nameLabelsFile != None:
            nameMap = {}
            with open(nameLabelsFile, 'r') as nf:
                nameReader = csv.reader(nf)
                for row in nameReader:
                    nameId = row[0]
                    nameText = row[1]
                    nameMap[nameId] = nameText
            for tId in self.data:
                self.data[tId] = [ nameMap[nId] for nId in self.data[tId] ]


    def attestationTableByTablet(self):
        return self.data
