To use the script modify the variables found in configuration file:
* The graphhopper api key (retrievable for frree here: https://www.graphhopper.com/)
* Your address to plan the route from here to the starting point of the trail
* The list of operators to parse (on OSM the operator tag of a relation must of course be filled to be found)

## Needed libraries
pip3 install OSMPythonTools osmnx folium

Also you will need to install libspatialindex_c, for linux just install package python3-rtree, for mac os brew install spatialindex

## Known issues
* Cannot handle CAI trails without operator (if a trail is shared between operators we leave the tag blank)
