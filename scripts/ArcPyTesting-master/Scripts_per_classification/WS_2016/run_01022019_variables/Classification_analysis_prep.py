"""
1: Creating work geodatabase (gdb)
2: Copying necessary files for prepping
3: Do processing within work gdb
4: Return results to result gdb
"""
# add temporal path to project folder with function files. This will make sure the functions can be imported
import sys
sys.path.append(r'E:\Python_Projects\ArcPyTesting')
from project_tools.arcpy_prep_tools import *

# import other modules
import arcpy
import os

# set paths and names
project_folder = r'G:\04_Westerschelde\02_Classificatieproces'
analysis_dir_name = '07_analysis'
work_dir = os.path.join(project_folder, analysis_dir_name)
gdb_name = 'WS_Analysis_preparation_final_variables'

if os.path.exists(work_dir):
    pass
else:
    print('Creating dir {}'.format(work_dir))
    os.mkdir(work_dir)

# shapefiles to load
classification_path = r'G:\04_Westerschelde\02_Classificatieproces\05_Mosaic_run_01022019_final_variables\Westerschelde_2016.shp'
gmk_path = r'Z:\Data rijkswaterstaat\Westerschelde\01_Data\01_Westerschelde\03_Geomorfologische_Kaarten\2016\e_GMK_Westerschelde2016.shp'
macrocells_path = r'Z:\Data rijkswaterstaat\Westerschelde\01_Data\01_Westerschelde\04_Macrocellen\macrocellen_vast.shp'

class_uu = classification_path.split('\\')[-1][:-4]
gmk = gmk_path.split('\\')[-1][:-4]
macrocells = macrocells_path.split('\\')[-1][:-4]

features = [classification_path, gmk_path, macrocells_path]

# create work gdb with shapefiles
work_gdb_path = os.path.join(work_dir, gdb_name)
create_work_gdb(work_dir, gdb_name, features)

# Set workspace to work gdb
arcpy.env.workspace = work_gdb_path+'.gdb'

####
# Adjust gmk
####

# Change class to combined class
code2class_gmk(gmk, 'class_GMK')

# dissolve with new classes
gmk_dissolved = 'gmk_dissolved'
dissolve_fields = ['class_GMK']

dissolve_features(gmk, gmk_dissolved, dissolve_fields)

# Add fields for identification
print('Adding common features to {}'.format(gmk_dissolved))
add_common_attributes(gmk_dissolved, 'gmk')

####
# Unions
####
# Union for general surface comparison
union_features = [class_uu, gmk_dissolved]
general_union_name = 'union_uu_gmk'

create_union_features(union_features, general_union_name)
add_common_attributes(general_union_name, 'union')

expression = "class_sub <> '_No_Class' And class_gmk <> ' '"
filter_union_result(general_union_name, 'filtered_union_uu_gmk',
                    expression=expression)

# Create union for object overlap analysis
# Dissolve UU
uu_dissolved = class_uu+'_dissolved'
dissolve_fields = ['class_main']

dissolve_features(class_uu, uu_dissolved, dissolve_fields)
add_common_attributes(uu_dissolved, 'UU')

# union
union_features = [uu_dissolved, gmk_dissolved]
dissolved_union = 'union_uu_gmk_dissolved'

create_union_features(union_features, dissolved_union)
add_common_attributes(dissolved_union, 'union')

expression = "class_main <> ' ' And class_gmk <> ' '"
filter_union_result(dissolved_union, 'filtered_union_uu_gmk_dissolved',
                    expression=expression)

# Create union with macrocells
# Only for Westerschelde
# Union for general surface comparison
union_features = [class_uu, gmk_dissolved, macrocells]
general_union_name = 'union_uu_gmk_macrocell'

create_union_features(union_features, general_union_name)
add_common_attributes(general_union_name, 'union')

expression = "class_sub <> '_No_Class' And class_gmk <> ' '"
filter_union_result(general_union_name, 'filtered_union_uu_gmk_macrocell',
                    expression=expression)


