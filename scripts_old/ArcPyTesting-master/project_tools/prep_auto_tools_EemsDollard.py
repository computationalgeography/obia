"""
Functions for preprocessing the aerial photographs before classification and post processing of
eCognition output

Sections indicated with comments
"""
import os
from osgeo import gdal
from gdal import ogr
import subprocess
import numpy as np

# =============================================================================
# ## Defining functions for processing ##
# =============================================================================
# Functies voor gdal processing


def create_mosaic(images_folder, output_folder, output_mosaic_name, gdal_bat):
    # Create list of images in the image folder
    image_list = []
    for file in os.listdir(images_folder):
        if file.endswith('.tif'):
            image_list.append(os.path.join(images_folder, file))

    # Write text file with image paths
    image_list_file = os.path.join(images_folder, 'images2mosaic.txt')
    imgfile = open(image_list_file, 'w')
    for image in image_list:
        imgfile.write(image + '\n')
    imgfile.close()

    # Creating output folder
    if os.path.exists(output_folder) == False:
        print('Creating output folder: {} \n'.format(output_folder))
        os.mkdir(output_folder)
    else:
        print('Output folder {} already exists\n'.format(output_folder))

    # Check if output file already exists
    mosaic_file = os.path.join(output_folder, output_mosaic_name)
    if os.path.isfile(mosaic_file):
        print('{} already exists.'.format(mosaic_file))
    else:
        print('Creating mosaic:')
        com_merge = 'gdal_merge.py --optfile {} -o {}'.format(image_list_file, mosaic_file)
        print(com_merge)

        mosaic_cmd = [gdal_bat, 'gdal_merge.py', '--optfile', image_list_file, '-o', mosaic_file]
        mosaic_process = subprocess.Popen(mosaic_cmd)
        mosaic_process.wait()

        if mosaic_process.returncode == 0:
            print('Creating {} complete!'.format(mosaic_file))
        else:
            print('Creating {} failed!'.format(mosaic_file))

        print('Creating mosaic done!')

        if os.path.exists(image_list_file):
            os.remove(image_list_file)
    # adding pyramid layer
    if os.path.isfile(mosaic_file):
        if os.path.isfile(mosaic_file + '.ovr'):
            print('pyramid overviews for {} already exist'.format(mosaic_file))
        else:
            print('Creating pyramids/overviews for {}'.format(mosaic_file))

            com_addo = 'gdaladdo -r AVERAGE -ro {} 2 4 8 16 32'.format(mosaic_file)

            addo_cmd = ['gdaladdo', '-r', 'AVERAGE', '-ro', mosaic_file, '2', '4', '8', '16', '32', '64']
            addo_process = subprocess.Popen(addo_cmd)
            addo_process.wait()
            if addo_process.returncode == 0:
                print('Creating pyramid overviews complete!')
            else:
                print('Creating pyramid overviews failed!')
            print(com_addo)
    else:
        print('There is no file to calculate pyramid overviews for.')


def cut_overlap_from_tiles(input_folder, output_folder, tile_overlap):
    # Create list of images in the image folder
    image_list = []
    tile_row_list = []
    tile_column_list = []
    for files in os.listdir(input_folder):
        if files.endswith('.tif'):
            image_list.append(files)
            tile_row_list.append(int(files[:-4].split('_')[-2]))
            tile_column_list.append(int(files[:-4].split('_')[-1]))

    # Get amount of tiles
    min_row_number = min(tile_row_list)
    max_row_number = max(tile_row_list)
    min_column_number = min(tile_column_list)
    max_column_number = max(tile_column_list)
    print(f'Minimum row number = {min_row_number}, Maximum row number ={max_row_number}')
    print(f'Minimum column number = {min_column_number}, Maximum column number = {max_column_number}')

    # Get raster tile dimensions
    test_raster = os.path.join(input_folder, image_list[0])
    ds = gdal.Open(test_raster)
    band = ds.GetRasterBand(1)
    tile_size_x = band.XSize
    tile_size_y = band.YSize

    ovrlp_div_2 = tile_overlap / 2
    # Creating output folder
    if os.path.exists(output_folder) == False:
        print('Creating output folder: {} \n'.format(output_folder))
        os.mkdir(output_folder)
    else:
        print('Output folder {} already exists\n'.format(output_folder))

    temp_output_folder = os.path.join(output_folder, 'temp_tile_rasters')
    # Creating output folder
    if os.path.exists(temp_output_folder) == False:
        print('Creating output folder: {} \n'.format(temp_output_folder))
        os.mkdir(temp_output_folder)
    else:
        print('Output folder {} already exists\n'.format(temp_output_folder))

    vrt_list = []

    for files in os.listdir(input_folder):

        if files.endswith('.tif'):
            image_path = os.path.join(input_folder, files)
            output_tile_name = os.path.join(temp_output_folder, files[:-4] + '.vrt')
            vrt_list.append(output_tile_name)
            tile_row, tile_column = files[:-4].split('_')[-2:]
            tile_row = int(tile_row)
            tile_column = int(tile_column)
            # general gdal function and commands
            gdal_cmd = ['gdal_translate', '-a_srs', 'EPSG:28992', '-of', 'VRT', '-srcwin']

            if os.path.exists(output_tile_name):
                print('{} Already exists'.format(output_tile_name))
            else:
                print('Processing {}'.format(output_tile_name))
                print(f'Tile {tile_row}_{tile_column}')
                # First row
                if tile_row == min_row_number and tile_column == min_column_number:
                    # add tile specifications
                    gdal_cmd.extend((str(0) + ',', str(0) + ',',  # Start x and y
                                     str(tile_size_x - ovrlp_div_2) + ',',
                                     str(tile_size_y - ovrlp_div_2)))  # Window size
                    print('First Row, first tile')
                    print(f'Cutting tile with coords: (0, 0)',
                          f'({tile_size_x - ovrlp_div_2}, {tile_size_y - ovrlp_div_2})')
                    # in and output paths
                    gdal_cmd.extend((image_path, output_tile_name))
                    # subsetting, pass gdal_cmd with subprocess
                    translate_process = subprocess.Popen(gdal_cmd)
                    translate_process.wait()  # We wait for process to finish
                    continue
                if tile_row == min_row_number and tile_column != min_column_number and tile_column != max_column_number:
                    gdal_cmd.extend((str(0 + ovrlp_div_2) + ',', str(0) + ',',
                                     str(tile_size_x - tile_overlap) + ',', str(tile_size_y - ovrlp_div_2)))
                    print('First Row, middle tile')
                    print(f'Cutting tile with coords: ({0 + ovrlp_div_2}, 0)',
                          f'({tile_size_x - tile_overlap}, {tile_size_y - ovrlp_div_2})')
                    gdal_cmd.extend((image_path, output_tile_name))
                    translate_process = subprocess.Popen(gdal_cmd)
                    translate_process.wait()
                    continue
                if tile_row == min_row_number and tile_column == max_column_number:
                    gdal_cmd.extend((str(0 + ovrlp_div_2) + ',', str(0) + ',',
                                     str(tile_size_x - ovrlp_div_2) + ',', str(tile_size_y - ovrlp_div_2)))
                    print('First Row, last tile')
                    print(f'Cutting tile with coords: ({0 + ovrlp_div_2}, 0)',
                          f'({tile_size_x - ovrlp_div_2}, {tile_size_y - ovrlp_div_2})')
                    gdal_cmd.extend((image_path, output_tile_name))
                    translate_process = subprocess.Popen(gdal_cmd)
                    translate_process.wait()
                    continue

                # Middel rows
                if tile_row != min_row_number and tile_row != max_row_number and tile_column == min_column_number:
                    gdal_cmd.extend((str(0) + ',', str(0 + ovrlp_div_2) + ',',
                                     str(tile_size_x - ovrlp_div_2) + ',', str(tile_size_y - tile_overlap)))
                    print('Middle Row, first tile')
                    print(f'Cutting tile with coords: ({0}, {0 + ovrlp_div_2})',
                          f'({tile_size_x - ovrlp_div_2}, {tile_size_y - tile_overlap})')
                    gdal_cmd.extend((image_path, output_tile_name))
                    translate_process = subprocess.Popen(gdal_cmd)
                    translate_process.wait()
                    continue
                if tile_row != min_row_number and tile_row != max_row_number and tile_column != min_column_number and tile_column != max_column_number:
                    gdal_cmd.extend((str(0 + ovrlp_div_2) + ',', str(0 + ovrlp_div_2) + ',',
                                     str(tile_size_x - tile_overlap) + ',', str(tile_size_y - tile_overlap)))
                    print('Middle Row, middle tile')
                    print(f'Cutting tile with coords: ({0 + ovrlp_div_2}, {0 + ovrlp_div_2})',
                          f'({tile_size_x - tile_overlap}, {tile_size_y - tile_overlap})')
                    gdal_cmd.extend((image_path, output_tile_name))
                    translate_process = subprocess.Popen(gdal_cmd)
                    translate_process.wait()
                    continue
                if tile_row != min_row_number and tile_row != max_row_number and tile_column == max_column_number:
                    gdal_cmd.extend((str(0 + ovrlp_div_2) + ',', str(0 + ovrlp_div_2) + ',',
                                     str(tile_size_x - ovrlp_div_2) + ',', str(tile_size_y - tile_overlap)))
                    print('Middle Row, last tile')
                    print(f'Cutting tile with coords: ({0 + ovrlp_div_2}, {0 + ovrlp_div_2})',
                          f'({tile_size_x - ovrlp_div_2}, {tile_size_y - tile_overlap})')
                    gdal_cmd.extend((image_path, output_tile_name))
                    translate_process = subprocess.Popen(gdal_cmd)
                    translate_process.wait()
                    continue

                # Last row
                if tile_row == max_row_number and tile_column == min_column_number:
                    gdal_cmd.extend((str(0) + ',', str(0 + ovrlp_div_2) + ',',
                                     str(tile_size_x - ovrlp_div_2) + ',', str(tile_size_y - ovrlp_div_2)))
                    print('Last Row, first tile')
                    print(f'Cutting tile with coords: ({0}, {0 + ovrlp_div_2})',
                          f'({tile_size_x - ovrlp_div_2}, {tile_size_y - ovrlp_div_2})')
                    gdal_cmd.extend((image_path, output_tile_name))
                    translate_process = subprocess.Popen(gdal_cmd)
                    translate_process.wait()
                    continue
                if tile_row == max_row_number and tile_column != min_column_number and tile_column != max_column_number:
                    gdal_cmd.extend((str(0 + ovrlp_div_2) + ',', str(0 + ovrlp_div_2) + ',',
                                     str(tile_size_x - tile_overlap) + ',', str(tile_size_y - ovrlp_div_2)))
                    print('Last Row, middle tile')
                    print(f'Cutting tile with coords: ({0 + ovrlp_div_2}, {0 + ovrlp_div_2})',
                          f'({tile_size_x - tile_overlap}, {tile_size_y - ovrlp_div_2})')
                    gdal_cmd.extend((image_path, output_tile_name))
                    translate_process = subprocess.Popen(gdal_cmd)
                    translate_process.wait()
                    continue
                if tile_row == max_row_number and tile_column == max_column_number:
                    gdal_cmd.extend((str(0 + ovrlp_div_2) + ',', str(0 + ovrlp_div_2) + ',',
                                     str(tile_size_x - ovrlp_div_2) + ',', str(tile_size_y - ovrlp_div_2)))
                    print('Last Row, last tile')
                    print(f'Cutting tile with coords: ({0 + ovrlp_div_2}, {0 + ovrlp_div_2})',
                          f'({tile_size_x - ovrlp_div_2}, {tile_size_y - ovrlp_div_2})')
                    gdal_cmd.extend((image_path, output_tile_name))
                    translate_process = subprocess.Popen(gdal_cmd)
                    translate_process.wait()
                    continue

    image_list_file = os.path.join(temp_output_folder, 'vrt2mosaic.txt')
    imgfile = open(image_list_file, 'w')
    for vrt in vrt_list:
        imgfile.write(vrt + '\n')
    imgfile.close()

    # build mosaic
    mosaic_name = image_list[0].split('_')[0] + '_' + image_list[0].split('_')[1]
    mosaic_output_path = os.path.join(output_folder, mosaic_name + '.vrt')
    mosaic_output_path_tif = mosaic_output_path[:-4] + '.tif'
    mosaic_cmd = ['gdalbuildvrt', '-input_file_list', image_list_file, mosaic_output_path]

    #    mosaic_process = subprocess.Popen(mosaic_cmd)
    #    mosaic_process.wait()

    translate_cmd = ['gdal_translate', '-of', 'Gtiff', mosaic_output_path, mosaic_output_path_tif]


#    translate_process = subprocess.Popen(translate_cmd)
#    translate_process.wait()

def gdal_tiling(inputfile, outputfile, output_folder, tilesize_x, tilesize_y, tile_overlap):
    # Get image size
    ds = gdal.Open(inputfile)
    band = ds.GetRasterBand(1)
    xsize = band.XSize
    ysize = band.YSize

    # Determine tile stepsizes
    xlist = []
    ylist = []

    a = 0
    while a < xsize:
        xlist.append(a)
        a += tilesize_x - tile_overlap
    b = 0
    while b < ysize:
        ylist.append(b)
        b += tilesize_y - tile_overlap

    # Creating output folder
    if not os.path.exists(output_folder):
        print('Creating output dir: {} \n'.format(output_folder))
        os.mkdir(output_folder)
    else:
        print('Output folder {} already exists\n'.format(output_folder))

    # create temporary folder
    temp_folder = os.path.join(output_folder, 'temp_vrt_rasters')
    if not os.path.exists(temp_folder):
        print('Creating temp dir: {} \n'.format(temp_folder))
        os.mkdir(temp_folder)
    else:
        print('Output folder {} already exists\n'.format(temp_folder))

    # Create tiles with tilesize, using tilesteps in the lists
    x_tile_counter = 0  # tile counters for tile names
    y_tile_counter = 0
    for x in xlist:
        x_tile_counter += 1
        y_tile_counter = 0
        for y in ylist:
            y_tile_counter += 1

            output_tile_name = '{}_{}_{}.vrt'.format(outputfile, y_tile_counter, x_tile_counter)

            output_temp_path = os.path.join(temp_folder, output_tile_name)

            # check if tiles exist
            if os.path.isfile(output_temp_path):
                print('Tile {}_{} already exists...'.format(y_tile_counter, x_tile_counter))
            else:
                # general gdal function and commands
                gdal_cmd = ['gdal_translate', '-a_srs', 'EPSG:28992', '-of', 'VRT', '-srcwin']
                # add tile specifications
                gdal_cmd.extend((str(x) + ',', str(y) + ',', str(tilesize_x) + ',', str(tilesize_y)))
                # in and output paths
                gdal_cmd.extend((inputfile, output_temp_path))

                # # command that gdal will read as input
                # com_string = "gdal_translate -a_srs EPSG:28992 -of GTIFF -srcwin " + str(x) + ", " + str(
                #     y) + ", " + str(tilesize_x) + ", " + str(tilesize_y) + " " + str(inputfile) + " " + str(
                #     outputfile + '_') + str(y_tile_counter) + "_" + str(x_tile_counter) + ".tif"
                print('Creating tile {}_{}:'.format(y_tile_counter, x_tile_counter))
                # print(com_string + '\n')

                # subsetting, pass gdal_cmd with subprocess
                translate_process = subprocess.Popen(gdal_cmd)
                translate_process.wait()  # We wait for process to finish

    for vrt in os.listdir(temp_folder):
        if vrt.endswith('.vrt'):
            input_path = os.path.join(temp_folder, vrt)
            tile_name = f'{vrt[:-4]}.tif'
            output_file_path = os.path.join(output_folder, tile_name)

            if os.path.exists(output_file_path):
                print(f'{tile_name} already exists...')
            else:
                vrt_data = gdal.Open(input_path)
                vrt_nir = vrt_data.GetRasterBand(1)
                vrt_stats = vrt_nir.GetStatistics(False, True)
                vrt_nir_mean = vrt_stats[2]
                print(f'Mean is {vrt_nir_mean}')

                if not vrt_nir_mean > 0:
                    print(f'{vrt} has no data. Will be skipped')
                else:
                    print(f'Translating {vrt} to {tile_name}')
                    gdal_cmd = ['gdal_translate', '-a_srs', 'EPSG:28992', '-of', 'GTIFF']
                    gdal_cmd.extend((input_path, output_file_path))

                    translate_process = subprocess.Popen(gdal_cmd)
                    translate_process.wait()  # We wait for process to finish

                    # creating pyramids
                    print(f'Creating pyramids for {tile_name}')
                    addo_cmd = ['gdaladdo', '-r', 'AVERAGE', '-ro', output_file_path, '2', '4', '8', '16', '32', '64']
                    addo_process = subprocess.Popen(addo_cmd)
                    addo_process.wait()

    print('Creating tiles done!')


def create_tile_extents(input_raster_dir_path,
                        output_extents_path, tile_extents_name):
    images_folder = input_raster_dir_path

    # Creating output folder
    if os.path.exists(output_extents_path) == False:
        print('Creating output folder: {} \n'.format(output_extents_path))
        os.mkdir(output_extents_path)
    else:
        print('Output folder {} already exists\n'.format(output_extents_path))

    image_list_file = os.path.join(output_extents_path, 'RasterList.txt')

    image_list = []
    for file in os.listdir(images_folder):
        if file.endswith('.tif') or file.endswith('.vrt'):
            image_list.append(os.path.join(images_folder, file))
    imgfile = open(image_list_file, 'w')
    for image in image_list:
        imgfile.write(image + '\n')
    imgfile.close()

    output = os.path.join(output_extents_path, tile_extents_name)
    gdal_command = 'gdaltindex'
    optfile = '--optfile'

    # print ('{} {} {}') %(gdal_command, output, images)
    cmd = [gdal_command,
           output,
           optfile,
           image_list_file]

    index_process = subprocess.Popen(cmd)
    if os.path.exists(output):
        print('output file {} already exists'.format(output))
    else:
        index_process.wait()

        if index_process.returncode == 0:
            print('Creating raster tiles index complete')
        else:
            print('Creating raster tiles index failed')

        shapefile = ogr.Open(output, 1)
        layer = shapefile.GetLayer(0)

        tile_number_field = ogr.FieldDefn('TileNumber', ogr.OFTString)
        layer.CreateField(tile_number_field)

        for feature in layer:
            location = feature.GetField('location')
            tile_name = location.split('\\')
            tile_name_parts = tile_name[-1][:-4].split('_')
            tile_number = '{}_{}'.format(tile_name_parts[3], tile_name_parts[4])
            feature.SetField('TileNumber', tile_number)
            layer.SetFeature(feature)
        layer.ResetReading()
        shapefile = None


def create_hoogte_tiles_from_tilesindex(tile_index_shapefile, hoogte_raster,
                                        output_path):
    shapefile = ogr.Open(tile_index_shapefile)
    layer = shapefile.GetLayer(0)

    # Create temp shapefile
    new_raster_folder = output_path
    if os.path.exists(new_raster_folder):
        print('{} already exists'.format(new_raster_folder))
    else:
        print('Creating new dir {}'.format(new_raster_folder))
        os.mkdir(new_raster_folder)

    temp_shp = os.path.join(new_raster_folder, 'temp_shape.shp')

    outDriver = ogr.GetDriverByName("ESRI Shapefile")
    # delete shapefile if it exists
    if os.path.exists(temp_shp):
        outDriver.DeleteDataSource(temp_shp)
        print('deleting file {}'.format(temp_shp))
    ## Create the output shapefile
    # temp_DataSource = outDriver.CreateDataSource(temp_shp)
    # tempLayer = temp_DataSource.CreateLayer("layer", geom_type=ogr.wkbPolygon)

    for feature in layer:
        tile_number = feature.GetField('TileNumber')
        # Create the output shapefile
        temp_DataSource = outDriver.CreateDataSource(temp_shp)
        tempLayer = temp_DataSource.CreateLayer("layer", geom_type=ogr.wkbPolygon)
        tempLayer.CreateFeature(feature)
        temp_DataSource = None

        hoogte_raster_tile = os.path.join(new_raster_folder, 'tile_' + tile_number + '.tif')

        if os.path.exists(hoogte_raster_tile):
            print('{} already exists'.format(hoogte_raster_tile))
        else:
            print('Creating tile {}'.format(hoogte_raster_tile))
            gdal.Warp(hoogte_raster_tile, hoogte_raster,
                      cutlineDSName=temp_shp,
                      cropToCutline=True)

        if os.path.exists(temp_shp):
            #        print 'resetting {}' %(temp_shp)
            outDriver.DeleteDataSource(temp_shp)
    layer.ResetReading()
    shapefile = None


def Create_mosaic_from_shp_tiles(tile_index_shapefile, shapefile_input_folder,
                                 output_path, output_shp_name, gdal_bat):
    shapefile = ogr.Open(tile_index_shapefile)
    layer = shapefile.GetLayer(0)

    # Create temp shapefile
    clipped_shapefile_folder = os.path.join(output_path, '01_Clipped_Tiles')

    if os.path.exists(clipped_shapefile_folder):
        print('{} already exists'.format(clipped_shapefile_folder))
    else:
        print('Creating new dir {}'.format(clipped_shapefile_folder))
        os.mkdir(clipped_shapefile_folder)

    temp_shp = os.path.join(clipped_shapefile_folder, 'temp_shape.shp')

    outDriver = ogr.GetDriverByName("ESRI Shapefile")
    # delete shapefile if it exists
    if os.path.exists(temp_shp):
        outDriver.DeleteDataSource(temp_shp)
        print('deleting file {}'.format(temp_shp))

    ## Create the output shapefile
    # temp_DataSource = outDriver.CreateDataSource(temp_shp)
    # tempLayer = temp_DataSource.CreateLayer("layer", geom_type=ogr.wkbPolygon)

    for feature in layer:
        tile_number = feature.GetField('TileNumber')
        # Create the output shapefile
        temp_DataSource = outDriver.CreateDataSource(temp_shp)
        tempLayer = temp_DataSource.CreateLayer("layer", geom_type=ogr.wkbPolygon)
        tempLayer.CreateFeature(feature)
        temp_DataSource = None

        shapefile_input = os.path.join(shapefile_input_folder,
                                       'tile_' + tile_number + '.shp')
        clipped_shapefile = os.path.join(clipped_shapefile_folder,
                                         'tile_' + tile_number + '.shp')

        if os.path.exists(clipped_shapefile):
            print('{} already exists'.format(clipped_shapefile))
        elif os.path.exists(shapefile_input) == False:
            print('There is no {} for input'.format(shapefile_input))
        else:
            print('Creating tile {}'.format(clipped_shapefile))
            ogr2ogr_cmd = [gdal_bat,  # making sure ogr functions work
                           'ogr2ogr',  # ogr function
                           '-clipsrc', temp_shp,  # clipping extent
                           clipped_shapefile, shapefile_input,  # out- and input
                           '-nlt', 'POLYGON',  # output type
                           '-skipfailures']  # skip failed features
            #            for item in ogr2ogr_cmd[1:]:
            #                print item,

            ogr2ogr_process = subprocess.Popen(ogr2ogr_cmd)
            ogr2ogr_process.wait()

            if ogr2ogr_process.returncode == 0:
                print('\nClipping tile {} complete!\n'.format(clipped_shapefile))
            else:
                print('\nClipping tile {} failed!\n'.format(clipped_shapefile))

        if os.path.exists(temp_shp):
            #        print 'resetting {}' %(temp_shp)
            outDriver.DeleteDataSource(temp_shp)

    layer.ResetReading()
    shapefile = None

    output_shp_name
    shapefile_mosaic_path = os.path.join(output_path, output_shp_name + '.shp')

    if os.path.exists(shapefile_mosaic_path) == False:
        for file_ in os.listdir(clipped_shapefile_folder):
            if file_.endswith('.shp'):
                file_path = os.path.join(clipped_shapefile_folder, file_)
                shp_merge_cmd = ['ogr2ogr',
                                 '-f',
                                 'ESRI Shapefile',
                                 '-update',
                                 '-append',
                                 shapefile_mosaic_path,
                                 file_path,
                                 '-nln',
                                 output_shp_name]
                print("Merging {} with {}.shp".format(file_, output_shp_name))

                merge_process = subprocess.Popen(shp_merge_cmd)
                merge_process.wait()
    else:
        print('Mosaic already exists')


# Functies voor eCognition cmd client
def create_eCogWSP(workspace_cmd_client, workspaceFile, image_folder,
                   import_template, import_template_path):
    wsp_cmd = [workspace_cmd_client,
               workspaceFile,
               image_folder,
               import_template,
               "",
               import_template_path]

    if os.path.exists(workspaceFile):
        print('Workspace already exists...')
    else:
        print('Creating workspace...')
        create_wsp_process = subprocess.Popen(wsp_cmd)
        create_wsp_process.wait()  # We wait for process to finish

        if create_wsp_process.returncode == 0:
            print('Creating workspace succesfull!')
        else:
            print('creating workspace failed!')


def analyze_eCogWSP(eCognition_cmd_client, workspace_file, ruleset_path):
    analyze_cmd = [eCognition_cmd_client,
                   'sw',
                   workspace_file,
                   ruleset_path]

    print('Analysing images in workspace...')
    analyze_process = subprocess.Popen(analyze_cmd)
    analyze_process.wait()  # We wait for process to finish

    if analyze_process.returncode == 0:
        print('Processing images succesfull')
    else:
        print('Processing images failed')
