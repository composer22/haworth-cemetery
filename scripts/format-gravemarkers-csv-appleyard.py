#!/usr/bin/env python

# Reads a file which contains lines that represent grave markers in the Haworth Cemetery.
# Data was sourced from Peter Appleyard version
#
# format-gravemarkers-csv-appleyard.py -f <inputfile>
#
# Ex: format-gravemarkers-csv.py -f foo.txt > out.csv
#
# Then outputs a .csv formatted file:
#
# * Cemetery section
# * Grave ID
# * Grave Inscription
#
# The format of the lines of the input file is:

# Blank line = delimeter
# ID: a first three characters of the first line
# Inscripion: the remaining characters of the first line and all lines following
# till the next blank line
#
# example:
#
# A01 line 1
# line 2
#
# A02 line 1
# line 2
# line 3
#
# Leading spaces are removed from the output.
# A trailing newline is removed from the inscription on output.

import sys, getopt

# Represents a grave marker for formatted output.
class Grave(object):
    def __init__(self, section, id, inscription):
        self.section = section
        self.id = id
        self.inscription = inscription

    def fmt(self):
        return "\"{}\",{},\"{}\"".format(self.section, self.id, self.inscription[:-1])

def main(argv):
    # Get command line options
    try:
        opts, args = getopt.getopt(argv,"hf:",["inputfile="])
    except getopt.GetoptError:
        print 'format-gravemarkers-csv.py -f <inputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'format-gravemarkers-csv.py -f <inputfile>'
            sys.exit()
        elif opt in ("-f", "--inputfile"):
            input_file = arg

    # Read and process file.
    fh = open(input_file,"r")
    print "section,grave_id,inscription"
    grave = Grave("A", "" , "")
    first_line = True
    for line in iter(fh):
        l = line.replace("\n", "")
        if len(l) == 0:
            print grave.fmt()
            del grave
            grave = Grave("A", "" , "")
            first_line = True
        else:
            if first_line:
                grave.id = line[1:3]
                l = line[3:]
                grave.inscription = l.lstrip()
                first_line = False
            else:
                grave.inscription += line.lstrip()
    fh.close()
    print grave.fmt()
    del grave

if __name__ == "__main__":
   main(sys.argv[1:])
