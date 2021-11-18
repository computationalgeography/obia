"""
Functions for the GIS processing of the classification data.
The functions work mainly with arcpy.

"""
import arcpy
import os
from pandas import DataFrame as df


def field_exists(features, field):
    """
    Check if a field exists for the input features
    :param features: Input features
    :param field: Field to check
    :return: True or False
    """
    field_list = list(arcpy.ListFields(features, field))
    if len(field_list) == 1:
        return True
    else:
        return False


def create_work_gdb(gdb_dir, gdb_name, features_list=[]):
    """
    Creating a work directory for prepping classification analysis
    :param gdb_dir:
    :param gdb_name:
    :param features_list:
    :return:
    """
    # create database
    gdb_path = os.path.join(gdb_dir, gdb_name+'.gdb')
    if os.path.exists(gdb_path):
        print('database already exists')
    else:
        print('Creating geodatabase {gdb}'.format(gdb=gdb_name))
        arcpy.CreateFileGDB_management(gdb_dir, gdb_name)

        # add file to geo database
        if len(features_list) < 1:
            print('No features to add to gdb')
        else:
            print('Adding features to gdb')
            for features in features_list:
                arcpy.FeatureClassToGeodatabase_conversion(features, gdb_path)
            print('Adding features complete\n')


def code2class_gmk(gmk_features, field_name):
    """
    Add a field to the GMK with new classes
    :param gmk_features:
    :param field_name:
    :return:
    test1
    """
    if field_exists(gmk_features, field_name):
        print('Target field already exists')
    else:
        arcpy.AddField_management(gmk_features, field_name, 'TEXT', field_length=30)

        # calculate new field:
        expression = 'get_class_name(!GEOCODE2!)'
        codeblock = '''def get_class_name(class_value):
            RWS_code_list = [['P1', 'K1'],
                             ['P2b', 'P2a', 'K2a', 'K2b'],
                             ['P2c', 'K2c', 'P2d'],
                             ['H2'],
                             ['O'],
                             ['S1a'],
                             ['S1c'],
                             ['S2'],
                             ['S3a'],
                             ['H1']]
            class_list_rws = ['Plaat Laag Energetisch',
                              'Plaat Megaribbel',
                              'Plaat Hoog Vlak',
                              'Hard Substraat',
                              'Overig',
                              'Schor',
                              'Schor Open Plek',
                              'Schor Pionier',
                              'Schor Meanderende Kreek',
                              'Overig']
            code2class = zip(RWS_code_list, class_list_rws)
            for codes, klasse in code2class:
                for code in codes:
                    if code == class_value.strip():
                        return klasse
                    if code in class_value.strip():
                        return klasse
            return 'Overig'
        '''
        arcpy.CalculateField_management(gmk_features, field_name, expression, "PYTHON3",
                                        codeblock)
def code2class_gmkP(gmk_features, field_name):
    """
    Add a field to the GMK with new classes
    :param gmk_features:
    :param field_name:
    :return:
    test1
    """
    if field_exists(gmk_features, field_name):
        print('Target field already exists')
    else:
        arcpy.AddField_management(gmk_features, field_name, 'TEXT', field_length=30)

        # calculate new field:
        expression = 'get_class_name(!GEOCODE2!)'
        codeblock = '''def get_class_name(class_value):
            RWS_code_list = [['P1a1','K1a1'],
                            ['P1a2','K1a2'],
                            ['P1'],
                            ['P2b', 'P2a', 'K2a', 'K2b'],
                            ['P2c', 'K2c', 'P2d'],
                            ['H2'],
                            ['O'],
                            ['S1a'],
                            ['S1c'],
                            ['S2'],
                            ['S3a'],
                            ['H1']]
            class_list_rws = ['Plaat Laag Energetisch Zand',
                              'Plaat Laag Energetisch Silt',
                              'Plaat Laag Energetisch Zand',
                              'Plaat Megaribbel',
                              'Plaat Hoog Vlak',
                              'Hard Substraat',
                              'Overig',
                              'Schor',
                              'Schor Open Plek',
                              'Schor Pionier',
                              'Schor Meanderende Kreek',
                              'Hard Substraat H1']
            code2class = zip(RWS_code_list, class_list_rws)
            for codes, klasse in code2class:
                for code in codes:
                    if code == class_value.strip():
                        return klasse
                    if code in class_value.strip():
                        return klasse
            return 'Overig'
        '''
        arcpy.CalculateField_management(gmk_features, field_name, expression, "PYTHON3",
                                        codeblock)
        
def code2class_lars(features, field_name):
    """
    Add a field to the GMK with new classes
    :param features:
    :param field_name:
    :return:
    test1
    """
    if field_exists(features, field_name):
        print('Target field already exists')
    else:
        arcpy.AddField_management(features, field_name, 'TEXT', field_length=30)

        # calculate new field:
        expression = 'get_class_name(!GEOCODE2!)'
        codeblock = '''def get_class_name(class_value):
            RWS_code_list = [           
                     ['P1a1_tree'],
                     ["P1a2_tree"],
                     ['P1', 'K1'],
                     ['P2b', 'P2a', 'K2a', 'K2b'],
                     ['P2c', 'K2c', 'P2d'],
                     ['H2'],
                     ['O'],
                     ['S1a'],
                     ['S1c'],
                     ['S2'],
                     ['S3a'],
                     ['H1']]
            class_list_rws = ['Plaat zand',
                      'Plaat silt',
                      'Plaat Laag Energetisch',
                      'Plaat Megaribbel',
                      'Plaat Hoog Vlak',
                      'Hard Substraat',
                      'Overig',
                      'Schor',
                      'Schor Open Plek',
                      'Schor Pionier',
                      'Schor Meanderende Kreek',
                      'Hard substraat H1']
            code2class = zip(RWS_code_list, class_list_rws)
            for codes, klasse in code2class:
                for code in codes:
                    if code == class_value.strip():
                        return klasse
                    if code in class_value.strip():
                        return klasse
            return 'Overig'
        '''
        arcpy.CalculateField_management(features, field_name, expression, "PYTHON3",
                                        codeblock)        
        
def code2class_lars_old(gmk_features, field_name):
    """
    Add a field to the GMK with new classes
    :param class_features:
    :param field_name:
    :return:
    test1
    """
    if field_exists(gmk_features, field_name):
        print('Target field already exists')
    else:
        arcpy.AddField_management(gmk_features, field_name, 'TEXT', field_length=30)

        # calculate new field:
        expression = 'get_class_name(!Assigned_c!)'
        codeblock = '''def get_class_name(class_value):
            RWS_code_list = [['P1a1'],
                             ['P1a2'],
                             ['p1a2'],
                             ['P2b_tr'],
                             ['P2c'],
                             ['H1']]
            class_list_rws = ['P1a1',
                              'P1a2',
                              'P1a2',
                              'P2b',
                              'P2c',
                              'H1']
            code2class = zip(RWS_code_list, class_list_rws)
            for codes, klasse in code2class:
                for code in codes:
                    if code == class_value.strip():
                        return klasse
                    if code in class_value.strip():
                        return klasse
            return 'Overig'
        '''
        arcpy.CalculateField_management(gmk_features, field_name, expression, "PYTHON3",
                                        codeblock)
        
#def code2class_gmkPmerge(gmk_features, field_name):
#    """
#    Add a field to the GMK with new classes
#    :param gmk_features:
#    :param field_name:
#    :return:
#    test1
#    """
#    if field_exists(gmk_features, field_name):
#        print('Target field already exists')
#    else:
#        arcpy.AddField_management(gmk_features, field_name, 'TEXT', field_length=30)
#
#        # calculate new field:
#        expression = 'get_class_name(!GEOCODE2!)'
#        codeblock = '''def get_class_name(class_value):
#            RWS_code_list = [['P1a1'],
#                             ['P1a2'],
#                             ['P2b'],
#                             ['P2c'],
#                             ['H1']]
#            class_list_rws = ['P1a',
#                              'P1a',
#                              'P2b',
#                              'P2c',
#                              'H1']
#            code2class = zip(RWS_code_list, class_list_rws)
#            for codes, klasse in code2class:
#                for code in codes:
#                    if code == class_value.strip():
#                        return klasse
#                    if code in class_value.strip():
#                        return klasse
#            return 'Overig'
#        '''
#        arcpy.CalculateField_management(gmk_features, field_name, expression, "PYTHON3",
#                                        codeblock)        
def code2class_larsPmerge(gmk_features, field_name):
    """
    Add a field to the GMK with new classes
    :param class_features:
    :param field_name:
    :return:
    test1
    """
    if field_exists(gmk_features, field_name):
        print('Target field already exists')
    else:
        arcpy.AddField_management(gmk_features, field_name, 'TEXT', field_length=30)

        # calculate new field:
        expression = 'get_class_name(!Assigned_c!)'
        codeblock = '''def get_class_name(class_value):
            RWS_code_list = [['P1a1'],
                             ['P1a2'],
                             ['p1a2'],
                             ['P2b_tr'],
                             ['P2c'],
                             ['H1']]
            class_list_rws = ['P1a',
                              'P1a',
                              'P1a',
                              'P2b',
                              'P2c',
                              'H1']
            code2class = zip(RWS_code_list, class_list_rws)
            for codes, klasse in code2class:
                for code in codes:
                    if code == class_value.strip():
                        return klasse
                    if code in class_value.strip():
                        return klasse
            return 'Overig'
        '''
        arcpy.CalculateField_management(gmk_features, field_name, expression, "PYTHON3",
                                        codeblock)
def code2class_uu(features, field_name):
    """
    Add a field to the GMK with new classes
    :param features:
    :param field_name:
    :return:
    """
    if field_exists(features, field_name):
        print('Target field already exists')

        arcpy.AddField_management(features, field_name, 'TEXT', field_length=30)
    else:
        # calculate new field:
        expression = 'get_class_name(!class_sub!)'
        codeblock = '''def get_class_name(class_value):
            class_list_uu = [
                         'Schor',
                         'Schor Open Plek',
                         'Schor Pionier',
                         'Schor Meanderende Kreek',
                         'Plaat Laag Energetisch',
                         'Plaat Hoog Vlak',
                         'Plaat Megaribbel',
                         'Hard Substraat']
            sub_class_keys = [
                          'S1a',
                          'S1c',
                          'S2',
                          'S3a',
                          'Plaat Laag',
                          'Plaat Hoog',
                          'megaribbel',
                          'Hard Substraat']
            class2class = dict(zip(sub_class_keys, class_list_uu))
            if class_value.lower() == 'water':
                return 'Water'
            elif class_value.lower() == '_no_class':
                return '_No_Class'
            else:
                for sub, main in class2class.items():
                    if sub.strip().lower() in class_value.strip().lower():
                        return main
            return 'no assigned class'
    '''
        arcpy.CalculateField_management(features, field_name, expression, "PYTHON3",
                                        codeblock)


def add_common_attributes(feature, suffix):
    """
    Add ID and shape area field
    :param feature:
    :param suffix:
    :return:
    """
    # Adding ID
    field_name = 'ID_'+suffix
    if field_exists(feature, field_name):
        print('Target field {} already exists'.format(field_name))
    else:
        print('Adding field {} to {}'.format(field_name, feature))
        arcpy.AddField_management(feature, field_name, 'LONG')

        expression = '!OBJECTID!'
        arcpy.CalculateField_management(feature, field_name, expression)

    # Adding area
    field_name = 'Area_' + suffix
    if field_exists(feature, field_name):
        print('Target field {} already exists'.format(field_name))
    else:
        print('Adding field {} to {}'.format(field_name, feature))
        arcpy.AddField_management(feature, field_name, 'DOUBLE')

        expression = '!SHAPE.area!'
        arcpy.CalculateField_management(feature, field_name, expression, 'PYTHON3')

    # Adding border length
    field_name = 'Length_' + suffix
    if field_exists(feature, field_name):
        print('Target field {} already exists'.format(field_name))
    else:
        print('Adding field {} to {}\n'.format(field_name, feature))
        arcpy.AddField_management(feature, field_name, 'DOUBLE')

        expression = '!SHAPE.length!'
        arcpy.CalculateField_management(feature, field_name, expression, 'PYTHON3')


def dissolve_features(infeatures, dissolved_features, dissolve_fields):
    """
    Dissolve input features
    :param infeatures:
    :param dissolved_features:
    :param dissolve_fields:
    :return:
    """
    if arcpy.Exists(dissolved_features):
        print('{} already exists'.format(dissolved_features))
    else:
        print('Dissolving {} with combined classes'.format(infeatures))
        arcpy.Dissolve_management(infeatures, dissolved_features, dissolve_fields, "",
                                  "SINGLE_PART", "DISSOLVE_LINES")
        print('Dissolving complete\n')


def create_union_features(infeatures, outfeature):
    """
    Create a union from the input features
    :param infeatures:
    :param outfeature:
    :return:
    """
    if arcpy.Exists(outfeature):
        print('{} already exists'.format(outfeature))
    else:
        print('Creating union {}\n'.format(infeatures))
        arcpy.Union_analysis(infeatures, outfeature, 'NO_FID')


def filter_union_result(infeatures, outfeature, expression=''):
    """
    Filter the unioned features to an output that can be used for analysis
    :param infeatures:
    :param outfeature:
    :param expression:
    :return:
    """
    if arcpy.Exists(outfeature):
        print('{} already exists'.format(outfeature))
    else:
        print('filtering {}\n'.format(infeatures))
        data = arcpy.SelectLayerByAttribute_management(infeatures, "NEW_SELECTION",
                                                       expression)

        arcpy.CopyFeatures_management(data, outfeature)


def feature_attributes_to_pandas(feature, field_list):
    """
    Returns a pandas dataframe from the attribute table of the input features
    :param feature: input feature
    :param field_list: fields to load into dataframe
    :return: pandas dataframe of attribute table
    """
    attribute_table = arcpy.da.FeatureClassToNumPyArray(in_table=feature,
                                                        field_names=field_list,
                                                        skip_nulls=False)
    dataframe = df(attribute_table)
    return dataframe
