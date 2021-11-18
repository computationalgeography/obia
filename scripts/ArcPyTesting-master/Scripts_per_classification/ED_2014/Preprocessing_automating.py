# add temporal path to project folder with function files. This will make sure the functions can be imported
import sys
import arcpy

sys.path.append(r'E:\Python_Projects\ArcPyTesting')
from project_tools.arcpy_prep_tools import create_work_gdb
from project_tools.prep_auto_tools import *
import os

# =============================================================================
# ## Create mosaic ##
# =============================================================================
# set in and output paths
gdal_bat = r"C:\Program Files\QGIS 3.4\OSGeo4W.bat"
root = r'G:\05_EemsDollard\Classificatie'
data_folder = os.path.join(root, '01_data')
images_folder = os.path.join(data_folder, '01_tegels_luchtfoto')

project_name = 'EemsDollard_2014'
output_folder = os.path.join(root, '02_Mozaiek', '01_luchtfoto')
mosaic_name = os.path.join(output_folder, '{}.img'.format(project_name))

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
output_filename = '{}_tile'.format(project_name)

# set tile size and overlap in pixels
tile_size_x = 16000
tile_size_y = 16000
tile_overlap = 1600

# execute tiling
# gdal_tiling(input_filename, output_filename, output_tile_folder,
#             tile_size_x, tile_size_y, tile_overlap)

# UNCOMMENT BELOW
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

# # Creating tiles from height data
# shapefile_path = os.path.join(tile_extents_path, tile_extents_name)
# hoogte_raster = os.path.join(data_folder, '02_hoogte_loding', 'EemsDollard_2014_loding.img')
#
# nieuw_raster_path = os.path.join(tile_folder, '02_tiles_hoogte_loding')
#
# create_hoogte_tiles_from_tilesindex(shapefile_path, hoogte_raster, nieuw_raster_path)
#
# # Creating tiles for slope data
# hoogte_raster = os.path.join(data_folder,'03_hoogte_lidar', 'EemsDollard_2014_lidar.tif')
#
# nieuw_raster_path = os.path.join(tile_folder, '03_tiles_hoogte_lidar')
#
# create_hoogte_tiles_from_tilesindex(shapefile_path, hoogte_raster, nieuw_raster_path)
#
# # =============================================================================
# # ## Create and analyze eCognition workspace ##
# # =============================================================================
# # Paths to command line clients
# workspace_cmd_client = r"C:\Program Files\Trimble\eCognition Cmd Client 9.3\bin\DIAMkWksp.exe"
# eCognition_cmd_client = r"C:\Program Files\Trimble\eCognition Cmd Client 9.3\bin\DIACmdClient.exe"
#
# # # Create workspace
# # Change path according to your workspace
# workspace_name = 'Cmd_Workspace'
# workspace_path = r"E:\04_Westerschelde\99_Automation_Scripts\WorkspaceTesting"
# workspace_file = os.path.join(workspace_path, workspace_name + '.dpj')
#
# # Folder with image data to be processed, all the image data will be processed
# image_folder = r"E:\04_Westerschelde\99_Automation_Scripts\WorkspaceTesting\Images"
#
# # Custom import template name and folder
# import_template = 'Westerschelde_Import'
# import_template_path = r"E:\04_Westerschelde\99_Automation_Scripts\WorkspaceTesting\CustomImports"
#
# # create_eCogWSP(workspace_cmd_client, workspace_file, image_folder,
# #               import_template, import_template_path)
#
# # # Analyze images in the workspace
# # path to the rule-set
# ruleSetPath = r"E:\04_Westerschelde\99_Automation_Scripts\WorkspaceTesting\Testrulesets\ChessTest.dcp"
#
# # analyze_eCogWSP(eCognition_cmd_client, workspace_file, ruleSetPath)
#
# # =============================================================================
# # ## Mosaic of classified tiles ##
# # =============================================================================
# # input_folder = r"E:\04_Westerschelde\99_Automation_Scripts\TestFolder_autoscripts\03_Tiles_Classificatie"
# # output_folder = r"E:\04_Westerschelde\99_Automation_Scripts\TestFolder_autoscripts\04_Classification_Mosaic"
# # tile_overlap = 1600
#
# input_folder = r"E:\04_Westerschelde\02_Classificatieproces\04b_Workspace\02_Output\WS_2016_run2"
# output_folder = r"E:\04_Westerschelde\02_Classificatieproces\05_Classification_mosaic_run2"
# tile_overlap = 1600
# # create_classification_mosaic(input_folder, output_folder, tile_overlap)

input_shapefile_dir = r'G:\05_EemsDollard\Classificatie\04_Workspace\01_EemsDollard\02_Output\_Final_classificatie_adj_HondPaap'
mosaic_dir = os.path.join(root, '05_Mosaic')
run_dir = os.path.join(mosaic_dir, 'run_first_adj_HondPaap')
output_shp_name = project_name

if os.path.isdir(mosaic_dir):
    print('directory {} already exsists'.format(mosaic_dir))
else:
    print('creating directory {}'.format(mosaic_dir))
    os.mkdir(mosaic_dir)

if os.path.isdir(run_dir):
    print('directory {} already exsists'.format(run_dir))
else:
    print('creating directory {}'.format(run_dir))
    os.mkdir(run_dir)

create_mosaic_from_shp_tiles(tile_extents_name_no_overlap_path,
                             input_shapefile_dir,
                             run_dir,
                             output_shp_name,
                             gdal_bat,
                             mosaic=False)

# Create gdb for classification
create_work_gdb(run_dir, project_name)
gdb_path = os.path.join(run_dir, f'{project_name}.gdb')
arcpy.env.workspace = gdb_path

# merge files into gdb feature layer
input_shapefile_dir_clipped = os.path.join(run_dir, '01_Clipped_Tiles')
shapefile_list = []
for file in os.listdir(input_shapefile_dir_clipped):
    if file.endswith('.shp'):
        shapefile = os.path.join(input_shapefile_dir_clipped, file)
        shapefile_list.append(shapefile)
arcpy.Merge_management(shapefile_list, 'Eems_Dollard_2014')
