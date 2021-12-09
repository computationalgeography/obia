"""
Functions for processing the input classification data (attributes of polygons) to a format that can be plotted

Each section corresponds to a figure and is indicated by a comment

"""

import pandas as pd
from numpy import diag

# 1 Bar figure for overal area per class


def fig_staaf_opp_processing(input_dataframe, klasse_uu, klasse_gmk, opp_kolom, klasse_subset_list):
    """
    Process input dataframe to produce new dataframe for figure input
    :param input_dataframe:
    :param klasse_uu:
    :param klasse_gmk:
    :param opp_kolom:
    :param klasse_subset_list:
    :return:
    """
    data_staaf = input_dataframe

    data_staaf_uu = data_staaf[data_staaf[klasse_uu].isin(klasse_subset_list)]
    data_staaf_gmk = data_staaf[data_staaf[klasse_gmk].isin(klasse_subset_list)]

    data_staaf_uu = data_staaf_uu[[klasse_uu, opp_kolom]]
    data_staaf_uu_summed = data_staaf_uu.groupby(by=[klasse_uu]).sum()
    data_staaf_uu_summed['Classificatie'] = 'UU'
    data_staaf_uu_summed.columns = [opp_kolom, 'Classificatie']

    data_staaf_gmk = data_staaf_gmk[[klasse_gmk, opp_kolom]]
    data_staaf_gmk_summed = data_staaf_gmk.groupby(by=[klasse_gmk]).sum()
    data_staaf_gmk_summed['Classificatie'] = 'GMK'
    data_staaf_gmk_summed.columns = [opp_kolom, 'Classificatie']

    data_staaf_combined = pd.concat([data_staaf_uu_summed, data_staaf_gmk_summed]).reset_index()
    data_staaf_combined['Opp_ha'] = data_staaf_combined[opp_kolom]/10000

    return data_staaf_combined


# 2 Error matrix for class overgang


def oppervlakte_tabel(input_data, groupby_column_uu, groupby_column_gmk, opp_column, class_list):
    """
    Returns a tuple with two crosstable dataframes where the first one is percentage overlap, and second one
    is hectare overlap
    :param input_data: input pandas dataframe
    :param groupby_column_uu: uu class to groupby
    :param groupby_column_gmk: gmk class to groupby
    :param class_list: class list for subset and sequence
    :return: tuple of dataframes
    """
    # Berekenen van percentage
    # groupby klasse_uu en Klasse RWS, sum by oppervlakte

    # subset data set for relevant classes
    class_grouped_uu = groupby_column_uu
    class_grouped_gmk = groupby_column_gmk
    input_data_subset_temp = input_data[input_data[class_grouped_uu].isin(class_list)]
    input_data_subset = input_data_subset_temp[input_data_subset_temp[class_grouped_gmk].isin(class_list)]

    # grouperen data
    grouped_klasse = input_data_subset[[class_grouped_uu, class_grouped_gmk, opp_column]].groupby(
        by=[class_grouped_uu, class_grouped_gmk]).agg({opp_column: 'sum'})
    oppervlakte_pcts_uu = grouped_klasse.groupby(class_grouped_uu).apply(lambda x:
                                                                         100 * x / float(x.sum())).reset_index()

    oppervlakte_pcts_uu.columns = [class_grouped_uu, class_grouped_gmk, 'perc_uu']
    opp_pct = pd.concat([oppervlakte_pcts_uu, grouped_klasse.reset_index()[opp_column]], axis=1, sort=True)

    # maken van pivot van de lijst om een crosstabel te maken
    pivot_perc = opp_pct.pivot(index=class_grouped_uu,
                               columns=class_grouped_gmk,
                               values='perc_uu')
    pivot_opp = opp_pct.pivot(index=class_grouped_uu,
                              columns=class_grouped_gmk,
                              values=opp_column)
    # Aanpassen index van tabel
    pivot_perc = pivot_perc.reindex(class_list,
                                    columns=class_list,
                                    fill_value=0)
    pivot_opp = pivot_opp.reindex(class_list,
                                  columns=class_list,
                                  fill_value=0)
    # m2 naar ha
    pivot_opp = pivot_opp / 10000

    return pivot_perc, pivot_opp


def add_outer_columns_rows(input_dataframe):
    """
    Adding the outer columns to the crosstable with area values

    :param input_dataframe: dataframe with area values
    :return df_adjusted: adjusted dataframe with extra column and row values
    """
    df_adjusted = input_dataframe.copy()
    diagonal = diag(input_dataframe)
    total_diagonal = diag(input_dataframe).sum()
    total_percentage = total_diagonal / (input_dataframe.sum().sum())
    total_column = input_dataframe.sum()
    total_row = input_dataframe.sum(axis=1)

    df_adjusted.loc[:, 'Total row (ha)'] = total_row
    df_adjusted.loc['Total column (ha)'] = total_column

    df_adjusted.loc['Total diagonal (ha)', 'Total diagonal (ha)'] = total_diagonal

    df_adjusted.loc['User Accuracy (%)'] = diagonal / total_column * 100
    
    # df_adjusted.loc[:, 'Classification Accuracy (%)'] = diagonal / total_row * 100
    df_adjusted.loc[:, 'Producer Accuracy (%)'] = diagonal / total_row * 100

    df_adjusted.loc['Total Accuracy (%)', 'Total Accuracy (%)'] = total_percentage * 100
    return df_adjusted


# 3 Histogram for original objects of uu and gmk


def prep_original_object_histogram(input_dataframe, klasse_subset_list,
                                   id_uu, klasse_uu,
                                   id_gmk, klasse_gmk, opp_kolom):
    """

    :param input_dataframe:
    :param klasse_subset_list:
    :param id_uu:
    :param klasse_uu:
    :param id_gmk:
    :param klasse_gmk:
    :param opp_kolom:
    :return:
    """
    klasse_data_subset_uu = input_dataframe[input_dataframe[klasse_uu].isin(klasse_subset_list)]
    klasse_data_rws = input_dataframe[input_dataframe[klasse_gmk].isin(klasse_subset_list)]

    # groupby to get area per class/object
    klasse_data_uu = klasse_data_subset_uu[[id_uu, klasse_uu, opp_kolom]].groupby(by=[id_uu, klasse_uu],
                                                                                  as_index=False).sum()
    klasse_data_rws = klasse_data_rws[[id_gmk, klasse_gmk, opp_kolom]].groupby(by=[id_gmk, klasse_gmk],
                                                                               as_index=False).sum()

    # combine uu and rws for plotting
    klasse_data_uu_temp = klasse_data_uu[[opp_kolom, klasse_uu]]
    klasse_data_uu_temp.columns = [opp_kolom, 'Klasse']
    klasse_data_uu_temp['Classificatie'] = 'UU'

    klasse_data_rws_temp = klasse_data_rws[[opp_kolom, klasse_gmk]]
    klasse_data_rws_temp.columns = [opp_kolom, 'Klasse']
    klasse_data_rws_temp['Classificatie'] = 'RWS'

    klasse_data_combined = pd.concat([klasse_data_uu_temp, klasse_data_rws_temp])
    klasse_data_combined.loc[:, 'Opp_ha'] = klasse_data_combined[opp_kolom] / 10000

    return klasse_data_combined


# 4 Histogram of objects per class transition

def prep_hist_per_transition(input_dataframe, klasse_subset_list, classes, opp_column):
    """

    :param input_dataframe:
    :param klasse_subset_list:
    :param classes:
    :param opp_column:
    :return:
    """
    # Create filter for different class objects
    class_uu, class_gmk = classes
    dif_class_filter = ~(input_dataframe[class_uu] == input_dataframe[class_gmk])

    # subset objects with different classes on the overlap
    dif_classes = input_dataframe[dif_class_filter].copy()

    dif_classes_subset = dif_classes[(dif_classes[class_uu].isin(klasse_subset_list)) &
                                     (dif_classes[class_gmk].isin(klasse_subset_list))]

    dif_classes_subset.loc[:, 'Opp_ha'] = dif_classes_subset.loc[:, opp_column] / 10000
    return dif_classes_subset
