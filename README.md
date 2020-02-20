# printsaver
NOTE: this is currently only tested with gcode output from Cura, some of the flags in the gcode that the script looks for may be different 

A command line script to attempt to save failed 3D prints. Reads the gcode inputFile, removes all layers of the print below the given height of the failed print (partHeight), and corrects the extruder value so that the new gcode file can hopefully save the failed part if it hasn't been removed from the print bed.

Takes the required arguments inputfile and partheight (mm), the output file can be specified using the --o optional argument or defaults to rescue.gcode. 

An example for usage would be: 
python printsaver.py benchy.gcode 6.2 --o benchy_printsaver.gcode

