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

####
# 1 Bar graph with Area values per class for uu and gmk
####

data_staaf_combined = fig_staaf_opp_processing(data, klasse_uu, klasse_gmk, opp_kolom,
                                               klasse_subset_list)
figuur_opp_per_klasse_staaf(data_staaf_combined, klasse_subset_list,
                            save_plot=True, safe_fig_folder=figure_dir,
                            figure_name='Barplot_Opp_dissolved')

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
                  figure_name='ErrorMatrix_Oppervlakte_dissolved')

# With added columns
plot_error_matrix(error_matrix, col_scale=(1000, 1000), added_columns=True,
                  save_plot=True, safe_fig_folder=figure_dir,
                  figure_name='ErrorMatrix_Oppervlakte_dissolved')

####
# 3 Histogram of objects per classification (uu, gmk)
####
# prep data for figure
histogram_df = prep_original_object_histogram(data, klasse_subset_list,
                                              'ID_uu', klasse_uu,
                                              'ID_gmk', klasse_gmk, opp_kolom)

# plot data
plot_histogram_og_objects(histogram_df, klasse_subset_list,
                          bin_min_max_n=(0.00001, 1500, 60),
                          save_plot=True, safe_fig_folder=figure_dir,
                          figure_name='Histogram_per_klasse_origineel')

# plot cumulative curve
plot_histogram_og_objects_cumulative(histogram_df, klasse_subset_list,
                                     bin_min_max_n=(0.00001, 1500, 60),
                                     save_plot=True, safe_fig_folder=figure_dir,
                                     figure_name='Histogram_per_klasse_origineel_cumulative_2')

####
# 4 Histogram of objects per class transition
####
klasses = (klasse_uu, klasse_gmk)
overgang_hist_df = prep_hist_per_transition(data, klasse_subset_list,
                                            klasses, opp_kolom)
plot_histogram_transi_objects(overgang_hist_df, klasse_subset_list,
                              klasses,
                              bin_min_max_n=(0.00001, 1500, 60),
                              save_plot=True, safe_fig_folder=figure_dir,
                              figure_name='Histogram_per_overgang_alle_objecten_opp')

plot_histogram_transi_objects_cumulative(overgang_hist_df, klasse_subset_list,
                                         klasses,
                                         bin_min_max_n=(0.00001, 1500, 60),
                                         save_plot=True, safe_fig_folder=figure_dir,
                                         figure_name='Histogram_per_overgang_alle_objecten_cumulatief_opp')
