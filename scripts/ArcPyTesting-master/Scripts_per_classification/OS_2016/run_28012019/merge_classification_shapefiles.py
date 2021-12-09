import sys
sys.path.append(r'E:\Python_Projects\ArcPyTesting')

from project_tools.prep_auto_tools import *
import os

input_shapefile_dir = r'C:\Oosterschelde_2016_processing\04_eCognition_Workspace\Fix_kleine_objecten\02_Output\Classification_Shapefile001'
output_dir = os.path.join(root, '05_Mosaic_run_small_obj_fix')
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