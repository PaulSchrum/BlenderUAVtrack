
import math

# class MyLittleProjection(object):
#     pass


_CENTER_LAT = 35.72777
_CENTER_LONG = -78.697949
_CENTER_EASTING = 2089649.0
_CENTER_NORTHING = 719945.0
_EW_DIST_MULTIPLIER = 296547.231270123
_NS_DIST_MULTIPLIER = 364360.587001507

class ptsPoint(object):

    def __init__(self, orderNumber, LatLongZ=None, XYZ=None):
        if not LatLongZ == None:
            self.orderNumber = float(orderNumber)
            parsed = LatLongZ.strip().split(',')
            self.long = float(parsed[0])
            self.lat = float(parsed[1])
            self.elev = float(parsed[2])

            deltaLat = self.lat - _CENTER_LAT
            deltaLong = self.long - _CENTER_LONG
            deltaEasting = deltaLong * _EW_DIST_MULTIPLIER
            deltaNorthing = deltaLat * _NS_DIST_MULTIPLIER
            self.easting = _CENTER_EASTING + deltaEasting
            self.northing = _CENTER_NORTHING + deltaNorthing
        elif XYZ != None:
            raise NotImplementedError("ptsPoint class does not currently "
                                      "work for known XYZ coordinates.")

    def __str__(self):
        return "#: {4:0.2f} Lat: {2:0.5f}  Long: {3:0.5f}    N: {0:0.4f}  " \
               "E: {1:0.4f}".format(self.northing, self.easting, self.lat,
                                self.long, self.orderNumber)

if __name__ == '__main__':
    testPtExpectedEasting = 2091925.0
    testPtExpectedNorthing = 720814.0
    testPt = ptsPoint(0.0, LatLongZ='-78.690272,35.730155,100.0')
    try:
        assert math.isclose(testPtExpectedEasting, testPt.easting,
                            abs_tol=1.25)
    except Exception as e:
        print("Assertion Failed in Easting")

    try:
        assert math.isclose(testPtExpectedNorthing, testPt.northing,
                            abs_tol=1.25)
    except Exception as e:
        print("Assertion Failed in Northing")
    else:
        print("Point test succeeded.")


class DinkyKML(object):
    def __init__(self, infileName, outfileName=None):
        self.infileName = infileName
        self.outfileName = outfileName
        self.pointSequence = []

        # Parse the input file
        with open(self.infileName) as inKML:
            allLines = inKML.readlines()
            self.headerLines = []
            self.pointSequence = []
            self.footerLines = []
            stateList = ['headers', 'line_coords', 'footers']
            state = stateList[0]
            seqNumber = 0
            for aLine in allLines:
                if state == 'headers':
                    self.headerLines.append(aLine)
                    if '<coordinates>' in aLine:
                        state = 'line_coords'
                elif state == 'line_coords':
                    if '</coordinates>' in aLine:
                        state = 'footers'
                        self.footerLines.append(aLine)
                    else:
                        self.pointSequence.append(ptsPoint(seqNumber, aLine))
                        seqNumber += 1
                elif state == 'footers':
                    self.footerLines.append(aLine)
        return



if __name__ == '__main__':
    fname = r"D:\SourceModules\Python\BlenderUAVtrack\testData\Afarm_Flight1.kml"

    kml = DinkyKML(fname)
    dbg = True
