from project_tools.prep_auto_tools import create_vrt_mosaic
import os

tegel_dirs = r'G:\06_Wadden\01_data\02_hoogte\01_Tegels'
output_root = r'G:\06_Wadden\01_data\02_hoogte\02_Compleet extent'

for tegel_dir in os.listdir(tegel_dirs):
    tegel_dir_path = os.path.join(tegel_dirs, tegel_dir)
    mosaic_name =  tegel_dir.split('\\')[-1]
    output_dir = os.path.join(output_root, mosaic_name)
    create_vrt_mosaic(tegel_dir_path, output_dir, mosaic_name)

