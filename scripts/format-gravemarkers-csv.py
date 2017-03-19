#!/usr/bin/python

# Reads a file which contains lines that represent grave markers in the Haworth Cemetery.
#
# format-gravemarkers-csv.py -f <inputfile>
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
# ID: a line of 1-4 characters that represent the grave ID ex: 142A, 12, etc.
# Inscription: one or more lines of text from the grave marker.
#
# example;
# 12
# line 1
# line 2
# 13
# line 1
# line 2
# line 3
#
# To differenciate between ID and Inscription, the following rule is used to pull the grave id:
# * First character must be numeric.
# * Length must be <= 5
#
# Hence if the source line meets these rules but should be included as an ID, you should
# add a leading space.
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
    first_pass_complete = False
    grave = ""
    for line in iter(fh):
      if line[0].isdigit() and len(line) <= 5:
          if first_pass_complete:
              print grave.fmt()
              del grave
          grave = Grave("C", line.replace("\n", ""), "")
      else:
          grave.inscription += line.lstrip(" ")
      first_pass_complete = True
    print grave.fmt()
    fh.close()

if __name__ == "__main__":
   main(sys.argv[1:])
