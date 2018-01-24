

# base class for python classes interacting with db

class dbWrapper:
    def getTablets(self):
        return None

    def getNames(self):
        return None

    def namesAppearingOn(self, tablet):
        return None

    def tabletsOnWhichAppears(self, name):
        return None

    def attestationTableByTablet(self):
        tabs = self.getTablets()
        if not tabs:
            return None
        table = {}
        for t in tabs:
            table[t] = namesAppearingOn(t)
        return table

    def attestationTableByName(self):
        names = self.getNames()
        if not names:
            return None
        table = {}
        for n in names:
            table[n] = tabletsOnWhichAppears(n)
        return table
