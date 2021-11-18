# import arcpy
# import os
#
# input_las_dir = r"G:\07_FrieseZeegat_Fotogrammetrie\01_Data\hansaluftbild_LAS\SURE_DSM_Cloud_Interpolated"
# output_dir = r"G:\07_FrieseZeegat_Fotogrammetrie\01_Data\hansaluftbild_LAS\merged"
# arcpy.CreateLasDataset_management(input_las_dir, output_dir)

import os
from project_tools.prep_auto_tools import *


root = r'G:\06_Wadden\03_tiles\Deelgebieden_3'
old_tif_dir = r'G:\06_Wadden\03_tiles\Deelgebieden\1\tif_tiles'

for deelgebied in os.listdir(root):
    deelgebied_path = os.path.join(root, deelgebied)
    vrt_dir = os.path.join(deelgebied_path, 'vrt_tiles')
    tif_dir = os.path.join(deelgebied_path, 'tif_tiles')
    create_dir(tif_dir)
    print(vrt_dir)
    if deelgebied in ['AM_ZEEGAT', 'EEMS_DOLLARD','HUIBERTGAT',
                      'FRIESE_ZEEGAT',]:
        continue

    for file in os.listdir(vrt_dir):
        print(f'vrt_dir file = {file}')
        file_basename = file[:-4]
        file_tif = f'{file_basename}.tif'
        file_ovr = f'{file_basename}.tif.ovr'

        file_tif_path = os.path.join(old_tif_dir, file_tif)
        file_ovr_path = os.path.join(old_tif_dir, file_ovr)

        copy(file_tif_path, tif_dir)
        copy(file_ovr_path, tif_dir)


