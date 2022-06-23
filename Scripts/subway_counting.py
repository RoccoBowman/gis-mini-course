import os
import pandas as pd
import qgis.core

# Setting Working Directories for data folders and Day 5 output folder 
datapath = '...GIS Mini-course Summer 2021/Day 5/data/'
outpath = '.../GIS Mini-course Summer 2021/Day 5/output/'

# Load NYC shapefile
vlayer = QgsVectorLayer(datapath + 'nybb.shp', "nyc", "ogr")
QgsProject.instance().addMapLayer(vlayer)

# Load rent points from table

input = datapath + 'rent_observations.csv'
x = 'long'
y = 'lat'
crs = 'EPSG:4326'
output = outpath + 'rent_points.shp'

processing.runAndLoadResults("qgis:createpointslayerfromtable",
{'INPUT':input,
'XFIELD':x,
'YFIELD':y,
'ZFIELD':None,
'MFIELD':None,
'TARGET_CRS':QgsCoordinateReferenceSystem(crs),
'OUTPUT':output})

# Reproject into 2263

processing.runAndLoadResults("native:reprojectlayer",
{'INPUT':'...GIS Mini-course Summer 2021/Day 5/output/rent_points.shp',
'TARGET_CRS':QgsCoordinateReferenceSystem('EPSG:2263'),
'OUTPUT':'...GIS Mini-course Summer 2021/Day 5/output/rent_points_2263.shp'})

# Extract Manhattan Island from nyc shapefile

processing.runAndLoadResults("native:extractbyattribute",
{'INPUT':'...GIS Mini-course Summer 2021/Day 5/data/nybb.shp',
'FIELD':'BoroName',
'OPERATOR':0,
'VALUE':'Manhattan',
'OUTPUT':'...GIS Mini-course Summer 2021/Day 5/output/manhattan.shp'})

# Buffer Rent ob points

processing.runAndLoadResults("native:buffer",
{'INPUT':'...GIS Mini-course Summer 2021/Day 5/output/rent_points_2263.shp',
'DISTANCE':1000,
'SEGMENTS':5,
'END_CAP_STYLE':0,
'JOIN_STYLE':0,
'MITER_LIMIT':2,
'DISSOLVE':False,
'OUTPUT':'...GIS Mini-course Summer 2021/Day 5/output/rent_buffers.shp'})

# Load subway stops

vlayer = QgsVectorLayer(datapath + 'stops_nyc_subway.shp', "subway", "ogr")
QgsProject.instance().addMapLayer(vlayer)

# Count stations within each buffer

processing.runAndLoadResults("qgis:joinbylocationsummary",
{'INPUT':'...GIS Mini-course Summer 2021/Day 5/output/rent_buffers.shp',
'JOIN':'...GIS Mini-course Summer 2021/Day 5/data/stops_nyc_subway.shp',
'PREDICATE':[0],
'JOIN_FIELDS':['trains'],
'SUMMARIES':[0],
'DISCARD_NONMATCHING':False,
'OUTPUT':'...GIS Mini-course Summer 2021/Day 5/output/count_subways.shp'})

# Create voronoi polygon tesselation

processing.runAndLoadResults("qgis:voronoipolygons", {'INPUT':'...GIS Mini-course Summer 2021/Day 5/output/rent_points_2263.shp',
'BUFFER':100,
'OUTPUT':outpath + 'rent_voronoi.shp'})

# Clip to manhattan island

processing.runAndLoadResults("gdal:clipvectorbypolygon",
{'INPUT':outpath + 'rent_voronoi.shp',
'MASK':'...GIS Mini-course Summer 2021/Day 5/output/manhattan.shp',
'OPTIONS':'',
'OUTPUT':outpath + 'voronoi_clip.shp'})

# Count stations within each voronoi poly

processing.runAndLoadResults("qgis:joinbylocationsummary",
{'INPUT':outpath + 'voronoi_clip.shp',
'JOIN':'...GIS Mini-course Summer 2021/Day 5/data/stops_nyc_subway.shp',
'PREDICATE':[0],
'JOIN_FIELDS':['trains'],
'SUMMARIES':[0],
'DISCARD_NONMATCHING':False,
'OUTPUT':'...GIS Mini-course Summer 2021/Day 5/output/voronoi_subways.shp'})

