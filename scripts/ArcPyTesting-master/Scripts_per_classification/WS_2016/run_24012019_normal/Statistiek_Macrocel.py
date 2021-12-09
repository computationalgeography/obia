"""
Load data from gdb as either text export or from gdb itself
currently retrieving data from gdb

This script runs functions from analyse_processing.py to process data from the input data
to the data structure that is needed to plot.

With functions from Figure_functions.py the processed data is plotted.
"""
# import os
# import pandas as pd

# add temporal path to project folder with function files. This will make sure the functions can be imported
import sys
sys.path.append(r'E:\Python_Projects\ArcPyTesting')

from project_tools.arcpy_prep_tools import feature_attributes_to_pandas
from project_tools.analyse_processing import *
from project_tools.Figure_functions import *
import arcpy

# gdb path import with arcpy works, but maybe export from analysis
# to csv first and load csv to remove arcpy dependency from analysis?
gdb = r'C:\Oosterschelde_2016_processing\07_analysis\OS_Analysis_preparation__adj_segmentation_fix.gdb'
arcpy.env.workspace = gdb

# Figure Folder
figure_dir = r"C:\Users\3786064\Desktop\TestImages_statistiek_Oosterschelde\test"

# load data
fields_list = ['class_main', 'ID_UU', 'Area_UU', 'Length_UU',
               'Class_GMK', 'ID_gmk', 'Area_gmk', 'Length_gmk',
               'ID_union', 'Area_union', 'Length_union']

data = feature_attributes_to_pandas('filtered_union_uu_gmk_dissolved', fields_list)

data.columns = ['class_uu', 'ID_uu', 'Area_uu', 'Length_uu',
                'class_gmk', 'ID_gmk', 'Area_gmk', 'Length_gmk',
                'ID_union', 'Area_union', 'Length_union']

####
# Main variables
####

# class names from ecognition export
class_eCognition = ['S1a, Schor',
                    'S1c, Open Plek',
                    'S2, Pionier',
                    'S3a, Meanderende Kreek',
                    'Plaat Laag energetisch',
                    'Plaat Megaribbel',
                    'Plaat Hoog Vlak']

# main class names and sequence for figures
klasse_subset_list = ['Schor',
                      'Schor Open Plek',
                      'Schor Pionier',
                      'Schor Meanderende Kreek',
                      'Plaat Laag Energetisch',
                      'Plaat Megaribbel',
                      'Plaat Hoog Vlak']

# change main classes to correct names for figures
ecog2klasse = dict(zip(class_eCognition, klasse_subset_list))
data.loc[:, 'class_uu'] = data['class_uu'].replace(ecog2klasse)

# rest of variables for further use
klasse_uu = 'class_uu'
klasse_gmk = 'class_gmk'
opp_kolom = 'Area_union'
