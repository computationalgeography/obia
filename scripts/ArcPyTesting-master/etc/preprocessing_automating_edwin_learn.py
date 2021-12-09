# add temporal path to project folder with function files. This will make sure the functions can be imported
import sys
sys.path.append(r'c:\edwin\scripts\ArcPyTesting-master')

# sys.path.append(r'c:\Program Files\QGIS 3.16.8\bin')

# sys.path.append(r'c:\Program Files\QGIS 3.16.8\apps\Python39\Scripts')


from project_tools.prep_auto_tools import *
import os

# =============================================================================
# ## Create mosaic ##
# =============================================================================
# set in and output paths
# gdal_bat_arg = "C:\Program Files\QGIS 3.16.8\OSGeo4W.bat"
# gdal_bat = r'"{}"'.format(gdal_bat_arg)
gdal_bat = " "

# gdal_bat = r"C:\edwin\scratch\rws_obia_2018_test\01_data\gdal_bat_folder\OSGeo4W.bat"

root = r'C:\edwin\scratch\rws_obia_2018_test'
data_folder = os.path.join(root, '01_data')
images_folder = os.path.join(data_folder, '01_tegels_luchtfoto')
## edwin's question: What are the data_folder and images_folder?

project_name = 'Westerschelde_2016_small_test'
output_folder = os.path.join(root, '02_Mozaiek')
mosaic_name = os.path.join(output_folder, '{}.tif'.format(project_name))

# create mosaic
# create_mosaic(images_folder, output_folder, mosaic_name, gdal_bat)

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

## edwin's question: Shall we change the resolution? Note that the new images have 12.5 cm resolution. 

### - the most likely setting for 12.5 cm resolution
# tile_size_x = 32000
# tile_size_y = 32000
# tile_overlap = 3200


# execute tiling
# gdal_tiling(input_filename, output_filename, output_tile_folder, tile_size_x, tile_size_y, tile_overlap)

# gdal_tiling_vrt(input_filename, output_filename, output_tile_folder, tile_size_x, tile_size_y, tile_overlap)



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

# Creating tiles from height data - WE DON'T NEED THIS
# shapefile_path = os.path.join(tile_extents_path, tile_extents_name)
# hoogte_raster = os.path.join(data_folder, '02_hoogte', 'os16_2m1.tif')
# - new dem file
# hoogte_raster = os.path.join(data_folder, '02_hoogte', 'ws18_2m_tot.tif')

# nieuw_raster_path = os.path.join(tile_folder, '02_tiles_hoogte')

# raster_subset_with_tileindex_tiles(shapefile_path, hoogte_raster, nieuw_raster_path)

# # Creating tiles for slope data
# hoogte_raster = os.path.join(data_folder,'03_slope','Slope_z0_01_filter_3.tif')
#
# nieuw_raster_path = os.path.join(tile_folder,'03_tiles_slope')
#
# create_hoogte_tiles_from_tilesindex(shapefile_path, hoogte_raster, nieuw_raster_path)
# create_hoogte_tiles_from_tilesindex(shapefile_path, hoogte_raster, nieuw_raster_path)

# =============================================================================
# ## Mosaic of classified tiles ##
# =============================================================================
# input_folder = r"E:\04_Westerschelde\99_Automation_Scripts\TestFolder_autoscripts\03_Tiles_Classificatie"
# output_folder = r"E:\04_Westerschelde\99_Automation_Scripts\TestFolder_autoscripts\04_Classification_Mosaic"
# tile_overlap = 1600

input_folder = r"E:\04_Westerschelde\02_Classificatieproces\04b_Workspace\02_Output\WS_2016_run2"
output_folder = r"E:\04_Westerschelde\02_Classificatieproces\05_Classification_mosaic_run2"
tile_overlap = 1600
# create_classification_mosaic(input_folder, output_folder, tile_overlap) - WE DON'T USE IT

input_shapefile_dir = r'C:\Oosterschelde_2016_processing\04_eCognition_Workspace\Fixing_new_segmentatie\02_Output\Classification_Shapefile001'

# - for our case
input_shapefile_dir = r'q:\edwin_2021\04_Westerschelde2016\02_Classificatieproces\results\v9'

output_dir = os.path.join(root, '05_Mosaic_run_adj_segmentatie_fix')
output_shp_name = project_name

if os.path.isdir(output_dir):
    print('directory {} already exsists'.format(output_dir))
else:
    print('creating directory {}'.format(output_dir))
    os.mkdir(output_dir)


tile_extents_name_no_overlap_path = r"s:\RWS_OBIA\External harddisk Harke\04_Westerschelde\02_Classificatieproces\03_tiles\1c_tiles_index_no_overlap\TileIndex_no_overlap.shp"
input_shapefile_dir = r'q:\edwin_2021\04_Westerschelde2016\02_Classificatieproces\results\v9\shp'
output_dir = r'q:\edwin_2021\04_Westerschelde2016\02_Classificatieproces\results\test_merge_edwin'
output_shp_name = 'Westerschelde_2016'
gdal_bat_arg = "C:\Program Files\QGIS 3.16.8\OSGeo4W.bat"
gdal_bat = r'"{}"'.format(gdal_bat_arg)

create_mosaic_from_shp_tiles(tile_extents_name_no_overlap_path,
                             input_shapefile_dir,
                             output_dir,
                             output_shp_name,
                             gdal_bat)
