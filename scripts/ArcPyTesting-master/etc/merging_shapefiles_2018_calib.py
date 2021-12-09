# add temporal path to project folder with function files. This will make sure the functions can be imported
import sys
sys.path.append(r'c:\edwin\scripts\ArcPyTesting-master')

from project_tools.prep_auto_tools import *
import os


tile_extents_name_no_overlap_path = r"q:\edwin_2021\04_Westerschelde2018\02_Classificatieproces\03_tiles\1c_tiles_index_no_overlap\TileIndex_no_overlap.shp"
input_shapefile_dir = r'c:\edwin\scratch\analyze_2018\results\v9_calibration_1_edwin\shp'
output_dir = r'c:\edwin\scratch\analyze_2018\results\v9_calibration_1_edwin\shp_without_overlaps'
output_shp_name = 'westerschelde_2018_v9_calibration_1_edwin'

# the following is not needed
# gdal_bat_arg = "C:\Program Files\QGIS 3.16.8\OSGeo4W.bat"
# gdal_bat = r'"{}"'.format(gdal_bat_arg)
gdal_bat = None

create_mosaic_from_shp_tiles(tile_extents_name_no_overlap_path,
                             input_shapefile_dir,
                             output_dir,
                             output_shp_name,
                             gdal_bat)
