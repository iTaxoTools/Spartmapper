# Spartmapper-Project
The Spartmapper project adds a GUI (graphical user interface) which is a utility to transform a series of geographical coordinates into a kml file.
The user can just input in a box a series of geographical coordinates in decimal format, tab-delimited, such as:



* 52.2807     10.5488



* But in the box, the user can input several such coordinates, in different rows, such as:

 * 52.2807    10.5488
 * 52.3465    11.3456
 * 52.1234    -9.3322
 * 52.3789    8.1234

 and so on.

* Then the program transform this into a .kml file that specifies the coordinates each as a point, and if imported in Google Earth, one sees all the points.

* Here is the information on the kml syntax which is a kind of xml:
* https://en.wikipedia.org/wiki/Keyhole_Markup_Language


# Features

* support for input tab file
* Viewing of kml in GUI interface
* Spart species information mapped to kml file


# How to use it


* To use it as GUI tool; Please type python mapper_spart.py on your terminal and follow the instructions.
