# add temporal path to project folder with function files. This will make sure the functions can be imported
import sys
import arcpy
sys.path.append(r'E:\Python_Projects\ArcPyTesting')

# from project_tools.prep_auto_tools_Wadden import *
from project_tools.prep_auto_tools import *
from project_tools.arcpy_prep_tools import create_work_gdb
import os

# =============================================================================
# ## Create mosaic ##
# =============================================================================
# set in and output paths
gdal_bat = r"C:\Program Files\QGIS 3.4\OSGeo4W.bat"
root = r'G:\07_FrieseZeegat_Classificatie'
data_folder = os.path.join(root, '01_data')
images_folder = os.path.join(data_folder, '01_luchtfoto_tiles')

project_name = 'FrieseZeegat_2018'
output_folder = os.path.join(root, '02_Mozaiek')
mosaic_name = os.path.join(output_folder, f'{project_name}')

# create pyramid overviews for rasters
for raster in os.listdir(images_folder):
    raster_path = os.path.join(images_folder, raster)
    # create_overviews_gdal(raster_path, gdal_bat)

# create mosaic
# create_vrt_mosaic(images_folder, output_folder, mosaic_name)

# create mosaic hoogte
dem_dir = os.path.join(data_folder, '02_hoogte')
dem_mosaic_name = 'dem_mosaic'
dem_mosaic_path = os.path.join(output_folder, f'{dem_mosaic_name}.vrt')
# create_vrt_mosaic(dem_dir, output_folder, dem_mosaic_name)

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
output_filename = f'{project_name}_tile'

# set tile size and overlap in pixels
tile_size_x = 16000
tile_size_y = 16000
tile_overlap = 1600

# execute tiling
# gdal_tiling_vrt(input_filename, output_filename, output_tile_folder,
#                 tile_size_x, tile_size_y, tile_overlap)

# change vrt to tiff
tif_tile_dir = os.path.join(output_tile_folder, 'tif_tiles')
vrt_tile_dir = os.path.join(output_tile_folder, 'temp_vrt_rasters')
# vrt2tif(vrt_tile_dir)

# Creating tile extents shapefile
tile_extents_dir = os.path.join(tile_folder, '01b_tiles_index')
tile_extents_name = 'TileIndex.shp'
tile_extents_path = os.path.join(tile_extents_dir, tile_extents_name)

# create_tile_extents(tif_tile_dir, tile_extents_dir, tile_extents_name)

# Creating tile extents shapefile no overlap
input_path = tif_tile_dir
output_path = os.path.join(tile_folder, '01c_tiles_index_no_overlap')
# cut_overlap_from_tiles(input_path, output_path, tile_overlap)

temp_tile_rasters = os.path.join(output_path, 'temp_tile_rasters')
tile_extents_name_no_overlap = 'TileIndex_no_overlap.shp'
tile_extents_name_no_overlap_path = os.path.join(output_path, tile_extents_name_no_overlap)
# create_tile_extents(temp_tile_rasters, output_path, tile_extents_name_no_overlap)

# Creating tiles from height data
mosaic_tiles_dir = os.path.join(tile_folder, '02_hoogte')
create_dir(mosaic_tiles_dir)
# raster_subset_with_tileindex_tiles(tile_extents_path, dem_mosaic_path, mosaic_tiles_dir)

# =============================================================================
# ## Create and analyze eCognition workspace ##
# =============================================================================
# # Paths to command line clients
# workspace_cmd_client = r"C:\Program Files\Trimble\eCognition Cmd Client 9.4\bin\DIAMkWksp.exe"
# eCognition_cmd_client = r"C:\Program Files\Trimble\eCognition Cmd Client 9.4\bin\DIACmdClient.exe"
#
#
# # Create workspace
# workspace_base_dir = os.path.join(root, '04_Workspace')
#
# for deelgebied in os.listdir(deelgebieden):
#     if deelgebied == 'EEMS_DOLLARD':
#         continue
#     run = 'run_x'
#     # Change path according to your workspace
#     workspace_dir = os.path.join(workspace_base_dir, deelgebied)
#     create_dir(workspace_dir)
#     run_dir = os.path.join(workspace_dir, run)
#     create_dir(run_dir)
#     workspace_file = os.path.join(run_dir, f"{deelgebied}_{run}.dpj")
#
#     # Root folder for search string of the custom import algorithm. Create within eCognition.
#     root_folder_deelgebied = os.path.join(deelgebieden, deelgebied)
#
#     # Custom import template name and folder
#     import_template = 'Import_Wadden_Deelgebied_1'
#     import_template_path = r"G:\06_Wadden\04_Workspace\99_custom_import"
#
#     # create_ecog_workspace(workspace_cmd_client, workspace_file, root_folder_deelgebied,
#     #                       import_template, import_template_path)
#
# # # Analyze images in the workspace
# # path to the rule-set
# ruleSetPath = r"E:\04_Westerschelde\99_Automation_Scripts\WorkspaceTesting\Testrulesets\ChessTest.dcp"
#
# # analyze_eCogWSP(eCognition_cmd_client, workspace_file, ruleSetPath)
# # =============================================================================
# # ## mosaic shapefile Tiles ##
# # =============================================================================
mosaic_dir = os.path.join(root, '05_Mosaic')
create_dir(mosaic_dir)

input_shapefile_dir = r"G:\07_FrieseZeegat_Classificatie\04_Workspace\FrieseZeegat_run_2\02_Output\Classification_Shapefile001"

section_dir = os.path.join(mosaic_dir, project_name)
run_dir = os.path.join(section_dir, 'run_Lidar_2')
output_shp_name = project_name

create_dir(section_dir)
create_dir(run_dir)
#
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

input_shapefile_dir_clipped = os.path.join(run_dir, '01_Clipped_Tiles')
shapefile_list = []
for file in os.listdir(input_shapefile_dir_clipped):
    if file.endswith('.shp'):
        shapefile = os.path.join(input_shapefile_dir_clipped, file)
        shapefile_list.append(shapefile)
print(f'Merging clipped shapefiles in {input_shapefile_dir_clipped} to gdb')
arcpy.Merge_management(shapefile_list, f'{project_name}')
print('Merging shapefile complete!')

#
#
#
#
# # input_shapefile_dir = r'G:\06_Wadden\04_Workspace\EI_ZEEGAT\run_x\02_Output\Classification_Shapefile001'
# # section_dir = os.path.join(mosaic_dir, 'EI_ZEEGAT')
# # run_dir = os.path.join(section_dir, 'run_x')
# # output_shp_name = project_name
# #
# # create_dir(mosaic_dir)
# # create_dir(section_dir)
# # create_dir(run_dir)
# #
# # # if os.path.isdir(mosaic_dir):
# # #     print('directory {} already exsists'.format(mosaic_dir))
# # # else:
# # #     print('creating directory {}'.format(mosaic_dir))
# # #     os.mkdir(mosaic_dir)
# # #
# # # if os.path.isdir(run_dir):
# # #     print('directory {} already exsists'.format(run_dir))
# # # else:
# # #     print('creating directory {}'.format(run_dir))
# # #     os.mkdir(run_dir)
# #
# # create_mosaic_from_shp_tiles(tile_extents_name_no_overlap_path,
# #                              input_shapefile_dir,
# #                              run_dir,
# #                              output_shp_name,
# #                              gdal_bat,
# #                              mosaic=False)
# #
# # # Create gdb for classification
# # create_work_gdb(run_dir, project_name)
# # gdb_path = os.path.join(run_dir, f'{project_name}.gdb')
# # arcpy.env.workspace = gdb_path
# #
# # # merge files into gdb feature layer
# # input_shapefile_dir_clipped = os.path.join(run_dir, '01_Clipped_Tiles')
# # shapefile_list = []
# # for file in os.listdir(input_shapefile_dir_clipped):
# #     if file.endswith('.shp'):
# #         shapefile = os.path.join(input_shapefile_dir_clipped, file)
# #         shapefile_list.append(shapefile)
# # arcpy.Merge_management(shapefile_list, f'{project_name}_section_1')
