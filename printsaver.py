#!/usr/bin/env python
import argparse
import re

parser = argparse.ArgumentParser(description='creates a gcode file restarting a 3D print from the next layer to hopefully save failed prints')
parser.add_argument("inputfile", type=str, help="This is the input file")
parser.add_argument("partheight", type=float, help="the height of the failed part, the z value the new gcode should start from. In mm")
parser.add_argument("--o", default="rescue.gcode", type=str, help="This is the output file")

args = parser.parse_args()
inputFile = args.inputfile
partHeight = args.partheight
outputFile = args.o

def printSaver(inputFile,partHeight,outputFile):
    """
    Reads the gcode inputFile, removes all layers of the print below the height of the 
    failed print (partHeight), and corrects the extruder value so that the new gcode file 
    can hopefully save the failed part.
    """
    gPattern = re.compile('G[01]')
    zPattern = re.compile('[ ]Z.?\d+.\d+')
    ePattern = re.compile('[ ]E.?\d+.\d+')
    startPattern = re.compile(';LAYER:0')
    
    bookmarks = {}
    flag = 0
    
    with open(inputFile) as gcode:
        for i,line in enumerate(gcode):
            line = line.strip()
            if gPattern.match(line):
                zCoord = re.findall(zPattern, line)
                extruder = re.findall(ePattern,line)
                if ('split' in bookmarks and extruder):
                    bookmarks['extruder'] =  float(re.findall(r'\d+.\d+',extruder[0])[0])
                    break
                elif zCoord:
                    if (float(re.findall(r'\d+.\d+',zCoord[0])[0]) > partHeight):
                        bookmarks['split'] = i
            elif startPattern.match(line):
                bookmarks['eoh'] = i - 1
    
    newGcode = []
    with open(inputFile) as gcode:
        for i,line in enumerate(gcode):
            if ((i >= bookmarks['split']) or (i < bookmarks['eoh'])):
                newGcode.append(line)
            elif (i == bookmarks['eoh']):
                newGcode.append(line)
                newGcode.append(";PRINTSAVER EDITS BEGIN HERE") 
                newGcode.append("G92 E{}\n".format(bookmarks['extruder']))
                newGcode.append(";PRINTSAVER EDITS END HERE")
                                
    with open(outputFile, 'w+') as rescue_gcode:
        rescue_gcode.writelines(newGcode)

    linesRemoved = bookmarks['split'] - bookmarks['eoh']
    print("Printsaver finished, {0} lines removed, saved to {1}".format(linesRemoved,outputFile))


printSaver(inputFile,partHeight,outputFile)
