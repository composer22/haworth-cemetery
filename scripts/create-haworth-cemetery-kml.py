#!/usr/bin/env python

# Create St Michael and All Angels's Church Graveyard Section
#
# This application reads a .csv file of grave markers and creates a KML file for
# import into Google Maps. Graves are ordered in a grid's row and col as marked in the .cvs
# Parameters
# -f --filepath  = name of .csv file to process.
# -n --section-name = graveyard section being processed.
# -o --long-start = longitude point where to start adding graves on the map.
# -a --lat-start = latitude point where to start adding graves on the map.
#
# example: create-haworth-cemetery-kml.py -f foo.csv -o -1.9563400 -a 53.8309600

# Outputs Keyhole Markup Language document for import to google Earth and Maps.
# see
#   https://developers.google.com/kml/ for file layout.
#   https://github.com/cleder/fastkml for library and requirements.

import csv
import sys, getopt
from fastkml import kml, styles
from shapely.geometry import Point, LineString, Polygon

# Constants
NS = '{http://www.opengis.net/kml/2.2}'
NAME = 'Haworth Cemetery'
DESCRIPTION = 'This is a map of graves in St Michael and All Angels\'s Church, Haworth UK.'
LONG_3FEET = 0.0000141
LONG_2FEET = 0.0000094
LAT_3FEET = 0.0000083
LAT_2FEET = 0.0000050

# Classes

def main(argv):
    # Get commandline options
    try:
        opts, args = getopt.getopt(argv,"hf:n:o:a:",["filepath=", "section-name=",
        "long-start=", "lat-start="])
    except getopt.GetoptError:
        print 'create-haworth-cemetery-kml.py -f <filepath> -n <section name> -o <long start> -a <lat start>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'create-haworth-cemetery-kml.py -f <filepath> -n <section name> -o <long start> -a <lat start>'
            sys.exit()
        elif opt in ("-f", "--filepath"):
            filepath = arg
        elif opt in ("-n", "--section-name"):
            section_name = arg
        elif opt in ("-o", "--long-start"):
            long_start = float(arg)
        elif opt in ("-a", "--lat-start"):
            lat_start = float(arg)

    # Create the root KML object
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

    # Create the KML Document, and add it to the KML root object
    d = kml.Document(NS, None, NAME, DESCRIPTION, doc_styles)
    k.append(d)

    # Create a KML Folder for the section and add it to the Document
    f = kml.Folder(NS, None, section_name)
    k.append(f)

    # Create a Placemark with a simple polygon geometry for each grave, and add it to the folder
    x = long_start
    y = lat_start
    counter = 1
    with open(filepath) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            grave_name = '{}-{}'.format(row['section'], row['grave_id'])
            grave_inscription = row['inscription']
            grave_inscription = grave_inscription.replace('\n','<br>')
            p = kml.Placemark(NS, None, grave_name, grave_inscription, None, '#poly-BDBDBD-1-77')
            p.geometry =  Polygon([
              (x,y,0),
              (x + LONG_3FEET,y,0),
              (x + LONG_3FEET,y + LAT_3FEET,0),
              (x,y + LAT_3FEET,0),
              (x,y,0)])
            y += (LAT_2FEET * 2)
            f.append(p)

            # Adjust rows
            if (counter % 10) == 0:
                x += (LONG_2FEET * 2)
                y = lat_start
            counter += 1

    # Print out the KML Object as a string
    print k.to_string(prettyprint=True)

if __name__ == "__main__":
   main(sys.argv[1:])
