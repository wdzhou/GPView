########################################################################
#
# GP Info
#
########################################################################

class RawGPInfo:
    """ A class to store a raw GP information 
    """
    def __init__(self, index, name):
        """ Init
        """
        self._index = index
        self._name = name
        self._data = None

    def __str__(self):         
        """ Write to string         
        """
        wbuf = "%d,%s\n" % (self._index, self._name)
        return wbuf


class UnitInfo:
    """ A simple structure to hold basic information
    """
    def __init__(self):
        """ Init
        """
        self.open    = 0.0
        self.close   = 0.0
        self.datestr = ""
        self.max     = 0.0
        self.min     = 0.0
    
    def __str__(self):
        """ Format output
        """
        rs = "%s: %.3f --> %.3f (%.3f, %.3f)" % (self.datestr,
                self.close, self.open, self.min, self.max)
        
        return rs

class GPInfoTrack:
    """ Class to hold a complete GP Information
    """
    def __init__(self, prefix, gindex):
        """ Init
        """
        prefix = prefix.lower()

        if prefix != 'sh' and prefix != 'sz':
            raise NotImplementedError("Prefix only support 'sh' and 'sz'")

        self._index = "%s%06d" % (prefix, int(gindex))

        self._simpleInfoList = []


    def addSinaEntry(self, sinastring):
        """ Add an entry for sina
        """
        # clean sina string
        if sinastring.count("\"") == 2:
            sinastring = sinastring.split("\"")[1]

        # split
        terms = sinastring.split(",")

        unitinfo = UnitInfo()

        unitinfo.open    = float(terms[1])
        unitinfo.close   = float(terms[2])
        unitinfo.currunt = float(terms[3])
        unitinfo.max     = float(terms[4])
        unitinfo.min     = float(terms[5])
        unitinfo.quanity = int(terms[8])
        unitinfo.amount  = float(terms[9])
        unitinfo.datestr = str(terms[30])

        self._simpleInfoList.append(unitinfo)

        return

    def getIndex(self):
        return self._index

    def getInfo(self, number):
        """ Get information to present
        """
        if number >= len(self._simpleInfoList):
            print "Out of scope"

        return self._simpleInfoList[-1-number]

