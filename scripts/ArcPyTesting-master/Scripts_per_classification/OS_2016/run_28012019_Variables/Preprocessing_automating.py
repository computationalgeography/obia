# add temporal path to project folder with function files. This will make sure the functions can be imported
import sys
sys.path.append(r'E:\Python_Projects\ArcPyTesting')

from project_tools.prep_auto_tools import *
import os

# =============================================================================
# ## Create mosaic ##
# =============================================================================
# set in and output paths
gdal_bat = r"C:\Program Files\QGIS 3.4\OSGeo4W.bat"
root = r'C:\Oosterschelde_2016_processing'
data_folder = os.path.join(root, '01_data')
images_folder = os.path.join(data_folder, '01_tegels_luchtfoto')

project_name = 'Oosterschelde_2016'
output_folder = os.path.join(root, '02_Mozaiek')
mosaic_name = os.path.join(output_folder, '{}.tif'.format(project_name))

# create mosaic
# create_mosaic(images_folder, output_folder, mosaic_name, gdal_bat)

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
# gdal_tiling(input_filename, output_filename, output_tile_folder,
#            tile_size_x, tile_size_y, tile_overlap)

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

# Creating tiles from height data
shapefile_path = os.path.join(tile_extents_path, tile_extents_name)
hoogte_raster = os.path.join(data_folder, '02_hoogte', 'os16_2m1.tif')

nieuw_raster_path = os.path.join(tile_folder, '02_tiles_hoogte')

# create_hoogte_tiles_from_tilesindex(shapefile_path, hoogte_raster, nieuw_raster_path)

# # Creating tiles for slope data
# hoogte_raster = os.path.join(data_folder,'03_slope','Slope_z0_01_filter_3.tif')
#
# nieuw_raster_path = os.path.join(tile_folder,'03_tiles_slope')
#
# create_hoogte_tiles_from_tilesindex(shapefile_path, hoogte_raster, nieuw_raster_path)

# =============================================================================
# ## Create and analyze eCognition workspace ##
# =============================================================================
# Paths to command line clients
workspace_cmd_client = r"C:\Program Files\Trimble\eCognition Cmd Client 9.3\bin\DIAMkWksp.exe"
eCognition_cmd_client = r"C:\Program Files\Trimble\eCognition Cmd Client 9.3\bin\DIACmdClient.exe"

# # Create workspace
# Change path according to your workspace
workspace_name = 'Cmd_Workspace'
workspace_path = r"E:\04_Westerschelde\99_Automation_Scripts\WorkspaceTesting"
workspace_file = os.path.join(workspace_path, workspace_name + '.dpj')

# Folder with image data to be processed, all the image data will be processed
image_folder = r"E:\04_Westerschelde\99_Automation_Scripts\WorkspaceTesting\Images"

# Custom import template name and folder
import_template = 'Westerschelde_Import'
import_template_path = r"E:\04_Westerschelde\99_Automation_Scripts\WorkspaceTesting\CustomImports"

# create_eCogWSP(workspace_cmd_client, workspace_file, image_folder,
#               import_template, import_template_path)

# # Analyze images in the workspace
# path to the rule-set
ruleSetPath = r"E:\04_Westerschelde\99_Automation_Scripts\WorkspaceTesting\Testrulesets\ChessTest.dcp"

# analyze_eCogWSP(eCognition_cmd_client, workspace_file, ruleSetPath)

# =============================================================================
# ## Mosaic of classified tiles ##
# =============================================================================
# input_folder = r"E:\04_Westerschelde\99_Automation_Scripts\TestFolder_autoscripts\03_Tiles_Classificatie"
# output_folder = r"E:\04_Westerschelde\99_Automation_Scripts\TestFolder_autoscripts\04_Classification_Mosaic"
# tile_overlap = 1600

input_folder = r"E:\04_Westerschelde\02_Classificatieproces\04b_Workspace\02_Output\WS_2016_run2"
output_folder = r"E:\04_Westerschelde\02_Classificatieproces\05_Classification_mosaic_run2"
tile_overlap = 1600
# create_classification_mosaic(input_folder, output_folder, tile_overlap)

input_shapefile_dir = r'C:\Oosterschelde_2016_processing\04_eCognition_Workspace\run_open_plek\02_Output\Classification_Shapefile_variables'
output_dir = os.path.join(root, '05_Mosaic_run_open_plek_variables')
output_shp_name = project_name

if os.path.isdir(output_dir):
    print('directory {} already exsists'.format(output_dir))
else:
    print('creating directory {}'.format(output_dir))
    os.mkdir(output_dir)

create_mosaic_from_shp_tiles(tile_extents_name_no_overlap_path,
                             input_shapefile_dir,
                             output_dir,
                             output_shp_name,
                             gdal_bat)
