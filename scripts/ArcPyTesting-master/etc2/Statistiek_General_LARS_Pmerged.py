"""
Load data from gdb as either text export or from gdb itself
"""
# import os
# import pandas as pd
# add temporal path to project folder with function files. This will make sure the functions can be imported
import sys
sys.path.append(r'V:\ws\westernscheldt\test_Harkecode\ArcPyTesting-master')

from project_tools.arcpy_prep_tools import feature_attributes_to_pandas
from project_tools.analyse_processing import *
from project_tools.Figure_functions import *
import arcpy

# gdb path import with arcpy works, but maybe export from analysis
# to csv first and load csv to remove arcpy dependency from analysis?
#gdb = r'V:\ws\westernscheldt\test_Harkecode\07_analysis\OS_Analysis_preparation__adj_segmentation_fix.gdb'
#gdb = r'V:\ws\westernscheldt\test_Harkecode\07_analysis\PandH_areas.gdb'
#gdb = r'V:\ws\westernscheldt\test_Harkecode\07_analysis\PandH_areas_Pmerged.gdb'
gdb = r'V:\ws\westernscheldt\test_Harkecode\07_analysis\run_V5_TOTALv3.gdb'
arcpy.env.workspace = gdb

# Figure Folder
figure_dir = r'V:\ws\westernscheldt\test_Harkecode\figures'

# load data
fields_list = ['class_lars',
               'class_GMK', 'ID_gmk', 'ID_union',
               'Area_gmk', 'Length_gmk', 'Area_union', 'Length_union']

data = feature_attributes_to_pandas('filtered_union_uu_gmk', fields_list)

data.columns = ['class_lars',
                'class_gmk', 'ID_gmk', 'ID',
                'Oppervlakte_gmk', 'Omtrek_gmk', 'Oppervlakte', 'Omtrek']

####
# Main variables
####
# =============================================================================
# code in this block is used for the Totalv2 dataset where the p1a1 and p1a2 in class_lars and class_gmk are merged to P1a

# class names from ecognition export
class_eCognition = ['P1a1','P1a2']
# main class names and sequence for figures
klasse_subset_list = ['P1a','P1a']
# change main classes to correct names for figures
ecog2klasse = dict(zip(class_eCognition, klasse_subset_list))
data.loc[:, 'class_lars'] = data['class_lars'].replace(ecog2klasse)
data.loc[:, 'class_gmk'] = data['class_gmk'].replace(ecog2klasse)
# =============================================================================

# rest of variables for further use
klasse_uu = 'class_lars'
klasse_gmk = 'class_gmk'
opp_kolom = 'Oppervlakte'
klasse_matrix = ['P1a','P2b','P2c','H1']

####
# 2 Error matrix, conversion matrix areaal
####

# first error matrices for percentage and area
pivot_perc, pivot_opp = oppervlakte_tabel(input_data=data,
                                          groupby_column_uu=klasse_uu,
                                          groupby_column_gmk=klasse_gmk,
                                          opp_column=opp_kolom,
                                          class_list=klasse_matrix)
# adding rows and columns to area matrix
error_matrix = add_outer_columns_rows(pivot_opp)

# Plot the graphs
# Normal without added columns/rows
plot_error_matrix(pivot_perc, col_scale=(0, 100), added_columns=False,
                  save_plot=True, safe_fig_folder=figure_dir,
                  figure_name='ErrorMatrix_Oppervlakte'+gdb.split('\\')[-1][:-4]+'P_merged')

# With added columns
plot_error_matrix(error_matrix, col_scale=(1000, 1000), added_columns=True,
                  save_plot=True, safe_fig_folder=figure_dir,
                  figure_name='ErrorMatrix_Oppervlakte'+gdb.split('\\')[-1][:-4]+'P_merged')