#!/usr/bin/env python

# Test the rotation mechanism of kml output and Google resolution
# Parameters:
# -o --long-start = longitude point where to start adding graves on the map.
# -a --lat-start = latitude point where to start adding graves on the map.
#
# example:
# test-rotation-kml.py -o -1.9565970 -a 53.8306800 > test-rotation.kml
#
# Outputs Keyhole Markup Language document for import to google Earth and Maps.
# see:
#   https://developers.google.com/kml/ for file layout.
#   https://github.com/cleder/fastkml for library and requirements.

import csv
import sys, getopt
from fastkml import kml, styles
from shapely.geometry import Point, LineString, Polygon
import shapely.affinity

# Constants
NS = '{http://www.opengis.net/kml/2.2}'
NAME = 'Test Rotation'
DESCRIPTION = "This is a test of the rotation feature of the shapely library."
SECTION = 'Rotation-Test'

# Approx. lengths
LONG_3FEET = 0.0000141
LONG_2FEET = 0.0000094
LONG_1FEET = 0.0000047
LONG_SIX_INCHES = 0.0000023
LAT_3FEET = 0.0000083
LAT_2FEET = 0.0000050
LAT_1FEET = 0.0000020
LAT_SIX_INCHES = 0.0000010

ADJUSTMENT_ANGLE_INCR = 4.00     # degrees counter-clockwise to rotate
OBJECT_START_ROW = 5
OBJECT_START_COL = 1

def main(argv):
    # Get command line options
    try:
        opts, args = getopt.getopt(argv,"ho:a:",[ "long-start=", "lat-start="])
    except getopt.GetoptError:
        print 'test-rotation-kml.py -o <long start> -a <lat start>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'test-rotation-kml.py -o <long start> -a <lat start>'
            sys.exit()
        elif opt in ("-o", "--long-start"):
            long_start = float(arg)
        elif opt in ("-a", "--lat-start"):
            lat_start = float(arg)

    map_origin = Point(long_start, lat_start)

    k = kml.KML()

    # Create the KML Document styles to use.
    doc_styles = []
    a = []
    a.append(styles.LineStyle(NS, None, 'ffbdbdbd'))
    a.append(styles.PolyStyle(NS, None, '4dbdbdbd'))
    doc_styles.append(kml.Style(NS, 'poly-BDBDBD-1-77-normal', a))
    a[0] = styles.LineStyle(NS, None, 'ffbdbdbd', None, 2)
    doc_styles.append(kml.Style(NS, 'poly-BDBDBD-1-77-highlight', a))
    doc_styles.append(kml.StyleMap(NS, "poly-BDBDBD-1-77",
        kml.StyleUrl(NS, None, '#poly-BDBDBD-1-77-normal'),
        kml.StyleUrl(NS, None, '#poly-BDBDBD-1-77-highlight')))

    # Create the KML Document, and add it to the KML root object.
    d = kml.Document(NS, None, NAME, DESCRIPTION.format(SECTION), doc_styles)
    k.append(d)

    # Create a KML Folder for the section and add it to the Document.
    f = kml.Folder(NS, None, "Section {}".format(SECTION))
    k.append(f)

    # Process a spiral of markers in a counter-clockwise direction
    lon = long_start + (OBJECT_START_ROW * (LONG_2FEET * 3))
    lat = lat_start  + (OBJECT_START_COL * (LAT_2FEET * 2))
    adjustment_angle = 0.00
    while adjustment_angle < 360:
        name = 'Degrees: {}'.format(adjustment_angle)
        p = kml.Placemark(NS, None, name, "Test Rotation", None, '#poly-BDBDBD-1-77')
        p.geometry =  Polygon([
          (lon, lat, 0),
          (lon + LONG_3FEET + LONG_2FEET, lat, 0),
          (lon + LONG_3FEET + LONG_2FEET, lat + LAT_3FEET, 0),
          (lon, lat + LAT_3FEET, 0),
          (lon, lat, 0)])
        p.geometry = shapely.affinity.rotate(p.geometry, adjustment_angle, map_origin)
        f.append(p)
        adjustment_angle += ADJUSTMENT_ANGLE_INCR

    # Print out the KML Object as a string.
    print k.to_string(prettyprint=True)

if __name__ == "__main__":
   main(sys.argv[1:])
