"""
Load data from gdb as either text export or from gdb itself
"""
# import os
# import pandas as pd
# add temporal path to project folder with function files. This will make sure the functions can be imported

import sys

#sys.path.append(r'Q:\edwin_2021\04_Westerschelde2016\ArcPyTesting-master')
sys.path.append(r'c:\edwin\scripts\ArcPyTesting-master')


from project_tools.arcpy_prep_tools import feature_attributes_to_pandas
from project_tools.analyse_processing import *
from project_tools.Figure_functions import *

import arcpy

#%%
# gdb path import with arcpy works, but maybe export from analysis
# to csv first and load csv to remove arcpy dependency from analysis?
# gdb = r'V:\ws\westernscheldt\test_Harkecode\07_analysis\run_V5_TOTALv1.gdb'
# gdb = r'V:\ws\westernscheldt\test_Harkecode\07_analysis_with_Harke\V5_run_1_main.gdb'
# gdb = r'V:\ws\westernscheldt\test_Harkecode\07_analysis_with_Harke\V5_run_3.gdb'
# gdb = r'V:\ws\westernscheldt\test_Harkecode\07_analysis_with_Harke\V5_run_test.gdb'
# gdb = r'V:\ws\westernscheldt\test_Harkecode\07_analysis_with_Harke\V6.gdb'
# gdb = r'Q:\edwin_2021\04_Westerschelde2016\07_analysis\V9.gdb'

gdb = r'c:\edwin\scratch\analysis_2016_v10\final\merged_p1a_split.gdb'

arcpy.env.workspace = gdb

# Figure Folder
figure_dir = r'c:\edwin\scratch\analysis_2016_v10\final'

# load data
fields_list = ['class_main',
               'class_GMK', 'ID_gmk', 'ID_union',
               'Area_gmk', 'Length_gmk', 'Area_union', 'Length_union']

data = feature_attributes_to_pandas('filtered_union_uu_gmk', fields_list)

data.columns = ['class_lars',
                'class_gmk', 'ID_gmk', 'ID',
                'Oppervlakte_gmk', 'Omtrek_gmk', 'Oppervlakte', 'Omtrek']

####
# Main variables
####

# class names from ecognition export
class_eCognition = ['S1a',
                    'S1c, open plek',#'S1c, Open Plek',
                    'S2, Pionier',
                    'S3a',
                    'Plaat Laag energetisch',
                    'P1a_tree',
                    'P1a_tree2',
                    'P1a1_tree',
                    'P1a1',
                    'P1a2',
                    'P1a1_tree2',
                    'P1a2_tree',
                    'P1a2_tree2',

                    'Plaat Megaribbel',
                    '_Candidate megaribbel',
                    'P2b_tree',
                    'P2b_tree2',
                    'Plaat Hoog Vlak',
                    'P2c_tree',
                    'P2c_tree2',
                    # 'H1_tree',
]

# main class names and sequence for figures
klasse_subset_list = ['Schor',
                      'Schor Open Plek',
                      'Schor Pionier',
                      'Schor Meanderende Kreek',
                        'Plaat Laag Energetisch',#p1a
                      'Plaat Laag Energetisch',#p1a
                      'Plaat Laag Energetisch',#p1a
                      'Plaat Laag Energetisch Zand',
                      'Plaat Laag Energetisch Zand',
                      'Plaat Laag Energetisch Zand',
                      'Plaat Laag Energetisch Silt',
                      'Plaat Laag Energetisch Silt',
                      'Plaat Laag Energetisch Silt',
                      
                      'Plaat Megaribbel',
                      'Plaat Megaribbel',
                      'Plaat Megaribbel',
                      'Plaat Megaribbel',#P2b
                      'Plaat Hoog Vlak',
                      'Plaat Hoog Vlak',
                      'Plaat Hoog Vlak',
                      # 'Hard Substraat H1'
                      ]



# change main classes to correct names for figures
ecog2klasse = dict(zip(class_eCognition, klasse_subset_list)) #nu niet nodig aangezien al de goede namen
klasse_subset_list = klasse_subset_list = ['Schor',
                      'Schor Open Plek',
                      'Schor Pionier',
                      'Schor Meanderende Kreek',
                      'Plaat Laag Energetisch',
                      'Plaat Laag Energetisch Zand',
                      'Plaat Laag Energetisch Silt',
                      'Plaat Megaribbel',
                      'Plaat Hoog Vlak',
#                       'Final Classification'
                      # 'Hard Substraat H1'
                      ]
data.loc[:, 'class_lars'] = data['class_lars'].replace(ecog2klasse)

# rest of variables for further use
klasse_uu = 'class_lars'
klasse_gmk = 'class_gmk'
opp_kolom = 'Oppervlakte'


####
# 1 Bar graph with Area values per class for uu and gmk
####

# data_staaf_combined = fig_staaf_opp_processing(data, klasse_uu, klasse_gmk, opp_kolom,
#                                                klasse_subset_list)
# figuur_opp_per_klasse_staaf(data_staaf_combined, klasse_subset_list,
#                             save_plot=False, safe_fig_folder=figure_dir,
#                             figure_name='Barplot_Opp')

####
# 2 Error matrix, conversion matrix areaal
####

# first error matrices for percentage and area
pivot_perc, pivot_opp = oppervlakte_tabel(input_data=data,
                                          groupby_column_uu=klasse_uu,
                                          groupby_column_gmk=klasse_gmk,
                                          opp_column=opp_kolom,
                                          class_list=klasse_subset_list)
# adding rows and columns to area matrix
error_matrix = add_outer_columns_rows(pivot_opp)

# Plot the graphs
# Normal without added columns/rows
plot_error_matrix(pivot_perc, col_scale=(0, 100), added_columns=False,
                  save_plot=True, safe_fig_folder=figure_dir,
                  figure_name='ErrorMatrix_Oppervlakte'+gdb.split('\\')[-1][:-4])#P1a1,p1a2

# With added columns
plot_error_matrix(error_matrix, col_scale=(1000, 1000), added_columns=True,
                  save_plot=True, safe_fig_folder=figure_dir,
                  figure_name='ErrorMatrix_Oppervlakte'+gdb.split('\\')[-1][:-4])
#%%
ecog2klasse = dict(zip(class_eCognition, klasse_subset_list)) #nu niet nodig aangezien al de goede namen
klasse_subset_list = klasse_subset_list = ['Schor',
                      'Schor Open Plek',
                      'Schor Pionier',
                      'Schor Meanderende Kreek',
                      'Plaat Laag Energetisch',
                      'Plaat Laag Energetisch Zand',
                      'Plaat Laag Energetisch Silt',
                      'Plaat Megaribbel',
                      'Plaat Hoog Vlak',
                       'Final Classification'
                      # 'Hard Substraat H1'
                      ]
data.loc[:, 'class_lars'] = data['class_lars'].replace(ecog2klasse)

# rest of variables for further use
klasse_uu = 'class_lars'
klasse_gmk = 'class_gmk'
opp_kolom = 'Oppervlakte'


####
# 1 Bar graph with Area values per class for uu and gmk
####

# data_staaf_combined = fig_staaf_opp_processing(data, klasse_uu, klasse_gmk, opp_kolom,
#                                                klasse_subset_list)
# figuur_opp_per_klasse_staaf(data_staaf_combined, klasse_subset_list,
#                             save_plot=False, safe_fig_folder=figure_dir,
#                             figure_name='Barplot_Opp')

####
# 2 Error matrix, conversion matrix areaal
####

# first error matrices for percentage and area
pivot_perc, pivot_opp = oppervlakte_tabel(input_data=data,
                                          groupby_column_uu=klasse_uu,
                                          groupby_column_gmk=klasse_gmk,
                                          opp_column=opp_kolom,
                                          class_list=klasse_subset_list)
# adding rows and columns to area matrix
error_matrix = add_outer_columns_rows(pivot_opp)

# Plot the graphs
# Normal without added columns/rows
plot_error_matrix(pivot_perc, col_scale=(0, 100), added_columns=False,
                  save_plot=True, safe_fig_folder=figure_dir,
#                  figure_name='ErrorMatrix_Oppervlakte'+gdb.split('\\')[-1][:-4]+'_P1a__Candidate megaribbel')#merged P1a
                  figure_name='ErrorMatrix_Oppervlakte'+gdb.split('\\')[-1][:-4]+'_all')#P1a1,p1a2

# With added columns
plot_error_matrix(error_matrix, col_scale=(1000, 1000), added_columns=True,
                  save_plot=True, safe_fig_folder=figure_dir,
#                  figure_name='ErrorMatrix_Oppervlakte'+gdb.split('\\')[-1][:-4]+'_P1a_Candidate megaribbel')
                  figure_name='ErrorMatrix_Oppervlakte'+gdb.split('\\')[-1][:-4]+'_all')