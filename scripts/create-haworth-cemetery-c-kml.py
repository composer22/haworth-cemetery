#!/usr/bin/env python

# Create St Michael and All Angels's Church Graveyard Section C
#
# This application reads a .csv file of grave markers and creates a KML file for
# import into Google Maps. Graves are ordered in a grid's row and col as marked in the .cvs
#
# Parameters:
# -f --filepath  = name of .csv file to process.
# -o --long-start = longitude point where to start adding graves on the map.
# -a --lat-start = latitude point where to start adding graves on the map.
#
# example:
# (latest to oldest)
# create-haworth-cemetery-c-kml.py -f "/home/foo/bar.csv" -o -1.9566000 -a 53.8306300 > graves-section-c.kml
# create-haworth-cemetery-c-kml.py -f "/home/foo/bar.csv" -o -1.9566250 -a 53.8306900
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
NAME = 'Haworth Cemetery'
DESCRIPTION = \
  "This is a map of graves for section {} of St Michael and All Angels\'s Church, Haworth UK."
SECTION = 'C'
GRAVEYARD_MAX_SIZE = 1000 # for graveyard grid

# Approx. lengths
LONG_3FEET = 0.0000141
LONG_2FEET = 0.0000094
LONG_1FEET = 0.0000047
LAT_3FEET = 0.0000083
LAT_2FEET = 0.0000050
LAT_1FEET = 0.0000020

ADJUSTMENT_ANGLE = 2 # degrees counter-clockwise to rotate

# Classes
# Represents a grave marker from the csv file
class Grave(object):
    def __init__(self, section, grave_id, row, column, inscription):
        self.section = section
        self.grave_id = grave_id
        self.row = row
        self.column = column
        self.inscription = inscription.replace('\n','<br>')

def main(argv):
    # Get command line options
    try:
        opts, args = getopt.getopt(argv,"hf:o:a:",["filepath=", "long-start=", "lat-start="])
    except getopt.GetoptError:
        print 'create-haworth-cemetery-c-kml.py -f <filepath> -o <long start> -a <lat start>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'create-haworth-cemetery-c-kml.py -f <filepath> -o <long start> -a <lat start>'
            sys.exit()
        elif opt in ("-f", "--filepath"):
            filepath = arg
        elif opt in ("-o", "--long-start"):
            long_start = float(arg)
        elif opt in ("-a", "--lat-start"):
            lat_start = float(arg)

    map_origin = Point(long_start, lat_start)

    # Read in all the graves as objects and stick them in a grid.
    graveyard =  [ [ None for i in range(GRAVEYARD_MAX_SIZE) ] for j in range(GRAVEYARD_MAX_SIZE) ]
    with open(filepath) as csvfile:
        reader = csv.DictReader(csvfile)
        for r in reader:
            if r['column']:
                row = int(r['row'])
                column = int(r['column'])
                graveyard[row][column] = Grave(r['section'], r['grave_id'], row, column, r['inscription'])

    # Create the root KML object.
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

    # Process the graveyard grid, creating a Placemark with a polygon for each grave.
    for i in range(GRAVEYARD_MAX_SIZE):
        for j in range(GRAVEYARD_MAX_SIZE):
            if graveyard[i][j]:
                g = graveyard[i][j]
                name = '{}-{}'.format(g.section, g.grave_id)
                p = kml.Placemark(NS, None, name.lower(), g.inscription, None, '#poly-BDBDBD-1-77')
                lon = long_start + (i * (LONG_2FEET * 3))
                lat = lat_start  + (j * (LAT_2FEET * 2))
                p.geometry =  Polygon([
                  (lon, lat, 0),
                  (lon + LONG_3FEET + LONG_2FEET, lat, 0),
                  (lon + LONG_3FEET + LONG_2FEET, lat + LAT_3FEET, 0),
                  (lon, lat + LAT_3FEET, 0),
                  (lon, lat, 0)])
                p.geometry = shapely.affinity.rotate(p.geometry, ADJUSTMENT_ANGLE, map_origin)
                f.append(p)

    # Print out the KML Object as a string.
    print k.to_string(prettyprint=True)

if __name__ == "__main__":
   main(sys.argv[1:])
