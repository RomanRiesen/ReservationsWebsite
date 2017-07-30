#This script takes a svg file as a command line parameter and creates a json file and a svg file.
#The json file contains the seats, represented by name, column, state and optionally row number.
#The svg file that gets produced contains all non-seat objects.

#elements whose name contains "seat", are treated as a seat.

#FIXME should calculate the normFacX by the size specifications of the actual svg file, but is hard because can be stuff like 90% or 12 hv

#FIXME files specified in the .svg by relative paths (e.g. images) should be copied and the paths adapted in the final svg file.

import json
import sys
import os.path as path
import xml.etree.ElementTree as elmTree

args = sys.argv[1:]
root = elmTree.parse(args[0]).getroot()
attributes = [elem.attrib for elem in root.iter()]

#these will contain the size  in which there are seats.
maxCy, maxCx, minCy, minCx = 0,0,float('inf'),float('inf')

seats, otherObj = [], []

for obj in attributes:
    name = str(obj.get('id'))
    if "seat" not in name :
        otherObj.append(obj)
        continue
    seats.append(obj)
    # Borders of the seat area in the svg file
    maxCy = max(float(obj['cy']), maxCy)
    maxCx = max(float(obj['cx']), maxCx)
   
    minCy = min(float(obj['cy']), minCy)
    minCx = min(float(obj['cx']), minCx)

#!!! assuming, that the seats are centered on the center of the svg file
normFacY = 1/(maxCy+minCy)
normFacX = 1/(maxCx+minCx)

jsonSeats = []
for seat in seats:
    x = float(seat["cx"])*normFacX
    y = float(seat["cy"])*normFacY
    jsonSeats.append({"i":seat["id"],"x":x,"y":y,"f":1})

jsonString = json.dumps(jsonSeats)

with open("seats_ORIGINAL.json", "w+") as f:
    f.write(jsonString)
