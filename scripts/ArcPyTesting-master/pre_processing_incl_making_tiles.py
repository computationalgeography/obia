
# Note that you will need a gdal environment. 

# add temporal path to project folder with function files. This will make sure the functions can be imported
import sys
sys.path.append(r'c:\edwin\scripts\ArcPyTesting-master')

from project_tools.prep_auto_tools import *
import os


# gdal_bat_arg = "C:\Program Files\QGIS 3.16.8\OSGeo4W.bat"
# gdal_bat = r'"{}"'.format(gdal_bat_arg)
#
# We don't need the following (gdal_bat) as Edwin has modified the scripts such that they will just use gdal functions (e.g. that can loaded in a gdal conda environment).
gdal_bat = None


# set in and output paths

root = r'C:\edwin\scratch\rws_obia_2018_test'
data_folder = os.path.join(root, '01_data')
images_folder = os.path.join(data_folder, '01_tegels_luchtfoto')

project_name = 'Westerschelde_2018'
output_folder = os.path.join(root, '02_Mozaiek')
mosaic_name = os.path.join(output_folder, '{}.tif'.format(project_name))



# =============================================================================
# ## Create mosaic ##
# =============================================================================

# create mosaic in vrt
output_mosaic_name = os.path.join(output_folder, '{}'.format(project_name))
create_vrt_mosaic(images_folder, output_folder, output_mosaic_name)
mosaic_name = output_mosaic_name + ".vrt"


# =============================================================================
# ## Create Tiles ##
# =============================================================================
# set in and output paths
input_filename = mosaic_name
tile_folder = os.path.join(root, '03_tiles')
if os.path.isdir(tile_folder):
    print('directory {} already exsists'.format(tile_folder))
else:
    print('creating directory {}'.format(tile_folder))
    os.mkdir(tile_folder)

output_tile_folder = os.path.join(tile_folder, '01_tiles_luchtfoto')
output_filename = os.path.join(output_tile_folder, '{}_tile'.format(project_name))

# set tile size and overlap in pixels
tile_size_x = 16000
tile_size_y = 16000
tile_overlap = 1600


# execute tiling
gdal_tiling(input_filename, output_filename, output_tile_folder, tile_size_x, tile_size_y, tile_overlap)


# Creating tile extents shapefile
tile_extents_path = os.path.join(tile_folder, '01b_tiles_index')
tile_extents_name = 'TileIndex.shp'
create_tile_extents(output_tile_folder, tile_extents_path, tile_extents_name)


# Creating tile extents shapefile no overlap
input_path = output_tile_folder
output_path = os.path.join(tile_folder, '1c_tiles_index_no_overlap')

cut_overlap_from_tiles(input_path, output_path, tile_overlap)

temp_tile_rasters = os.path.join(output_path, 'temp_tile_rasters')
tile_extents_name_no_overlap = 'TileIndex_no_overlap.shp'

tile_extents_name_no_overlap_path = os.path.join(output_path, tile_extents_name_no_overlap)

create_tile_extents(temp_tile_rasters, output_path, tile_extents_name_no_overlap)


# Creating tiles for height data
shapefile_path = os.path.join(tile_extents_path, tile_extents_name)
hoogte_raster  = os.path.join(data_folder, '02_hoogte', 'ws18_2m_tot.tif')

nieuw_raster_path = os.path.join(tile_folder, '02_tiles_hoogte')

raster_subset_with_tileindex_tiles(shapefile_path, hoogte_raster, nieuw_raster_path)


