"""
Functions for preprocessing the aerial photographs before classification and post processing of
eCognition output

Sections indicated with comments
"""
import sys
import os
from shutil import copy
from osgeo import gdal
from osgeo import ogr
import subprocess


def create_dir(dir_path):
    if os.path.isdir(dir_path):
        print(f'directory {dir_path} already exsists')
    else:
        print(f'creating directory {dir_path}')
        os.mkdir(dir_path)

# =============================================================================
# ## Defining functions for processing ##
# =============================================================================
# Functies voor gdal processing


def create_mosaic(images_folder, output_folder, output_mosaic_name, gdal_bat):
    """
    Create a tif mosaic of tiles images.
    :param images_folder: directory with tiles images
    :param output_folder: directory to save mosaic in
    :param output_mosaic_name: name for mosaic
    :param gdal_bat: bat file for gdal processing, makes sure the gdal functions work
    :return: no return function
    """
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
    create_dir(output_folder)

    # Check if output file already exists
    mosaic_file = os.path.join(output_folder, output_mosaic_name)
    if os.path.isfile(mosaic_file):
        print(f'{mosaic_file} already exists.')
    else:
        print('Creating mosaic:')
        com_merge = f'gdal_merge.py --optfile {image_list_file} -o {mosaic_file}'
        print(com_merge)

        # mosaic_cmd = [gdal_bat, 'gdal_merge.py', '--optfile', image_list_file, '-o', mosaic_file]
        
        mosaic_cmd = ['gdal_merge.py', '--optfile', image_list_file, '-o', mosaic_file]

        # mosaic_cmd = 'python c:\Users\Sutan101\.conda\envs\gdal_spyder\Scripts\gdal_merge.py --optfile ' + image_list_file + ' -o ' + mosaic_file
        # print(mosaic_cmd)

        # sys.path.append(r'c:\Program Files\QGIS 3.16.8\apps\Python39\Scripts')
        
        # mosaic_cmd = gdal_bat + ' python "c:\Program Files\QGIS 3.16.8\apps\Python39\Scripts\gdal_merge.py" --optfile ' + image_list_file + ' -o ' + mosaic_file
        
        

        # cmd = 'python "C:\Program Files\QGIS 3.16.8\apps\Python39\Scripts\gdal_merge.py" --optfile ' + image_list_file + ' -o ' + mosaic_file

        # cmd = 'python gdal_merge.py --optfile ' + image_list_file + ' -o ' + mosaic_file

        # print(cmd)
        # os.system(cmd)
        
        # print(mosaic_file)
        
        
        
        print(" ")
        print(mosaic_cmd)
        
        # os.system(mosaic_cmd)
        
        # mosaic_process = subprocess.Popen(mosaic_cmd)
        # mosaic_process = subprocess.check_call(mosaic_cmd,shell=True)
        mosaic_process = subprocess.run(mosaic_cmd, shell = True)
        mosaic_process.wait()

        # pietje

        if mosaic_process.returncode == 0:
            print(f'Creating {mosaic_file} complete!')
        else:
            print(f'Creating {mosaic_file} failed!')

        print('Creating mosaic done!')

        # if os.path.exists(image_list_file): os.remove(image_list_file)
    
    # adding pyramid layer
    if os.path.isfile(mosaic_file):
        if os.path.isfile(mosaic_file + '.ovr'):
            print(f'pyramid overviews for {mosaic_file} already exist')
        else:
            print(f'Creating pyramids/overviews for {mosaic_file}')

            com_addo = f'gdaladdo -r AVERAGE -ro {mosaic_file} 2 4 8 16 32'

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


def create_overviews_gdal(input_raster, gdal_bat):
    if os.path.isfile(input_raster + '.ovr'):
        print(f'pyramid overviews for {input_raster} already exist')
        return
    # elif not input_raster.endswith('.tif') or input_raster.endswith('.vrt'):
    #     return
    else:
        print(f'Creating pyramids/overviews for {input_raster}')

        com_addo = f'gdaladdo -r AVERAGE -ro {input_raster} 2 4 8 16 32'

        addo_cmd = [gdal_bat, 'gdaladdo', '-r', 'AVERAGE', '-ro', input_raster, '2', '4', '8', '16', '32', '64']
        # addo_cmd = [gdal_bat, 'gdaladdo', '-r', 'AVERAGE', '-ro', input_raster, '16', '32', '64']
        addo_process = subprocess.Popen(addo_cmd)
        addo_process.wait()
        if addo_process.returncode == 0:
            print('Creating pyramid overviews complete!')
        else:
            print('Creating pyramid overviews failed!')
        # print(com_addo)


def create_vrt_mosaic(images_folder, output_folder, output_mosaic_name):
    """
    Create a mosaic in vrt format.
    :param images_folder: input directory with image files to create the mosaic from
    :param output_folder: output directory for mosaic
    :param output_mosaic_name: output mosaic name
    :return: no return value
    """
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
    create_dir(output_folder)

    # Check if output file already exists
    output_mosaic_name = f'{output_mosaic_name}.vrt'
    mosaic_file = os.path.join(output_folder, output_mosaic_name)
    if os.path.isfile(mosaic_file):
        print(f'{mosaic_file} already exists.')
    else:
        print('Creating vrt mosaic:')
        gdal.BuildVRT(mosaic_file, image_list)
        print('Creating vrt mosaic done!')

        if os.path.exists(image_list_file):
            os.remove(image_list_file)


def gdal_tiling_vrt(inputfile, basename_tile, output_folder, tilesize_x, tilesize_y, tile_overlap):
    """
    Create tiles based on the vrt mosaic.
    :param inputfile: input vrt mosaic
    :param basename_tile: basename for the output tiles
    :param output_folder: directory for output tiles
    :param tilesize_x: tile width in pixels for x
    :param tilesize_y: tile height in pixels for y
    :param tile_overlap: overlap between the tiles
    :return: no return value
    """
    # Get image size
    inputfile = f'{inputfile}.vrt'
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
    create_dir(output_folder)

    # create temporary folder
    temp_folder = os.path.join(output_folder, 'temp_vrt_rasters')
    create_dir(temp_folder)

    # Create tiles with tilesize, using tilesteps in the lists
    x_tile_counter = 0  # tile counters for tile names
    for x in xlist:
        x_tile_counter += 1
        y_tile_counter = 0
        for y in ylist:
            y_tile_counter += 1

            output_tile_name = f'{basename_tile}_{y_tile_counter}_{x_tile_counter}.vrt'

            output_temp_path = os.path.join(temp_folder, output_tile_name)

            # check if tiles exist
            if os.path.isfile(output_temp_path):
                print(f'Tile {y_tile_counter}_{x_tile_counter} already exists...')
            else:
                # general gdal function and commands
                gdal_cmd = ['gdal_translate', '-a_srs', 'EPSG:28992', '-of', 'VRT', '-srcwin']
                # add tile specifications
                # gdal_cmd.extend((str(x) + ',', str(y) + ',', str(tilesize_x) + ',', str(tilesize_y)))
                gdal_cmd.extend((f'{x},', f'{y},', f'{tilesize_x},', f'{tilesize_y}'))
                # in and output paths
                gdal_cmd.extend((inputfile, output_temp_path))

                # # command that gdal will read as input
                # com_string = "gdal_translate -a_srs EPSG:28992 -of GTIFF -srcwin " + str(x) + ", " + str(
                #     y) + ", " + str(tilesize_x) + ", " + str(tilesize_y) + " " + str(inputfile) + " " + str(
                #     outputfile + '_') + str(y_tile_counter) + "_" + str(x_tile_counter) + ".tif"
                print(f'Creating tile {y_tile_counter}_{x_tile_counter}:')
                # print(com_string + '\n')

                # subsetting, pass gdal_cmd with subprocess
                translate_process = subprocess.Popen(gdal_cmd)
                translate_process.wait()  # We wait for process to finish

    # for vrt in os.listdir(temp_folder):
    #     if vrt.endswith('.vrt'):
    #         input_path = os.path.join(temp_folder, vrt)
    #         tile_name = f'{vrt[:-4]}.tif'
    #         output_file_path = os.path.join(output_folder, tile_name)
    #
    #         if os.path.exists(output_file_path):
    #             print(f'{tile_name} already exists...')
    #         else:
    #             vrt_data = gdal.Open(input_path)
    #             vrt_nir = vrt_data.GetRasterBand(1)
    #             vrt_stats = vrt_nir.GetStatistics(False, True)
    #             vrt_nir_mean = vrt_stats[2]
    #             print(f'Mean is {vrt_nir_mean}')
    #
    #             if not vrt_nir_mean > 0:
    #                 print(f'{vrt} has no data. Will be skipped')
    #             else:
    #                 print(f'Translating {vrt} to {tile_name}')
    #                 gdal_cmd = ['gdal_translate', '-a_srs', 'EPSG:28992', '-of', 'GTIFF']
    #                 gdal_cmd.extend((input_path, output_file_path))
    #
    #                 translate_process = subprocess.Popen(gdal_cmd)
    #                 translate_process.wait()  # We wait for process to finish
    #
    #                 # creating pyramids
    #                 print(f'Creating pyramids for {tile_name}')
    #                 addo_cmd = ['gdaladdo', '-r', 'AVERAGE', '-ro', output_file_path, '2', '4', '8', '16', '32', '64']
    #                 addo_process = subprocess.Popen(addo_cmd)
    #                 addo_process.wait()

    print('Creating tiles done!')


def select_vrt_kom(kom_shapefile, tile_dir, deelgebied_field, deelgebied):
    """
    Select from all vrt tiles the vrt tiles that intersect with the kom Extent
    :param kom_shapefile:
    :param tile_dir:
    :param deelgebied_field:
    :param deelgebied:
    :return:
    """
    shapefile = ogr.Open(kom_shapefile)
    layer = shapefile.GetLayer(0)

    tile_index_file = os.path.join(tile_dir, '01b_tiles_index', 'TileIndex.shp')

    # create output folder
    output_dir = os.path.join(tile_dir, deelgebied)
    create_dir(output_dir)

    out_driver = ogr.GetDriverByName("ESRI Shapefile")

    # Save each feature in a new shapfile and intersect with tile index
    for feature in layer:
        feature_name = str(feature.GetField(deelgebied_field)).replace(' ', '_')

        feature_dir = os.path.join(output_dir, feature_name)
        create_dir(feature_dir)

        deelgebied_path = os.path.join(feature_dir, f'Sectie_{feature_name}.shp')
        deelgebied_data_source = out_driver.CreateDataSource(deelgebied_path)
        deelgebied_layer = deelgebied_data_source.CreateLayer("deelgebied", geom_type=ogr.wkbPolygon)
        deelgebied_layer.CreateFeature(feature)
        deelgebied_data_source = None

        output_tile_index = os.path.join(feature_dir, f'tile_index_{feature_name}.shp')

        # create ogr2ogr command
        ogr2ogr_command = ['ogr2ogr', '-f', "ESRI Shapefile",
                           output_tile_index, tile_index_file,
                           '-dialect', 'sqlite', '-sql',
                           f'SELECT TI.Geometry, TI.location, TI.TileNumber '
                           f'FROM "{deelgebied_path}".Sectie_{feature_name} DG, TileIndex TI '
                           f'WHERE ST_Intersects(TI.geometry, DG.geometry)']
        ogr_process = subprocess.Popen(ogr2ogr_command)
        ogr_process.wait()


def copy_vrt_per_deelgebied(deelgebieden_dir):
    for deelgebied in os.listdir(deelgebieden_dir):
        print(deelgebied)
        index_file = os.path.join(deelgebieden_dir, deelgebied, f'tile_index_{deelgebied}.shp')
        print(index_file)
        shapefile = ogr.Open(index_file)
        layer = shapefile.GetLayer(0)

        vrt_dir = os.path.join(deelgebieden_dir, deelgebied, 'vrt_tiles')

        create_dir(vrt_dir)

        for feature in layer:
            vrt_path = feature.GetField('location')
            copy(vrt_path, vrt_dir)


def vrt2tif(input_file_dir):
    """
    Change vrt file to tiffs. Input a vrt file or directory.
    Output will be made in the same directory when input as a file or same parent directory as vrt files in 'tif_tiles'
    :param input_file_dir: input vrt file, or directory with vrts.
    :return:
    """
    if os.path.isdir(input_file_dir):
        tif_dir = os.path.join(os.path.dirname(input_file_dir), 'tif_tiles')
        create_dir(tif_dir)
        for vrt in os.listdir(input_file_dir):
            if vrt.endswith('.vrt'):
                input_path = os.path.join(input_file_dir, vrt)
                tile_name = f'{vrt[:-4]}.tif'
                output_file_path = os.path.join(tif_dir, tile_name)

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
    else:
        vrt = os.path.basename(input_file_dir)
        if vrt.endswith('.vrt'):
            tile_name = f'{vrt[:-4]}.tif'
            output_file_path = os.path.join(os.path.dirname(input_file_dir), tile_name)

            if os.path.exists(output_file_path):
                print(f'{tile_name} already exists...')
            else:
                vrt_data = gdal.Open(input_file_dir)
                vrt_nir = vrt_data.GetRasterBand(1)
                vrt_stats = vrt_nir.GetStatistics(False, True)
                vrt_nir_mean = vrt_stats[2]
                print(f'Mean is {vrt_nir_mean}')

                if not vrt_nir_mean > 0:
                    print(f'{vrt} has no data. Will be skipped')
                else:
                    print(f'Translating {vrt} to {tile_name}')
                    gdal_cmd = ['gdal_translate', '-a_srs', 'EPSG:28992', '-of', 'GTIFF']
                    gdal_cmd.extend((input_file_dir, output_file_path))

                    translate_process = subprocess.Popen(gdal_cmd)
                    translate_process.wait()  # We wait for process to finish

                    # creating pyramids
                    print(f'Creating pyramids for {tile_name}')
                    addo_cmd = ['gdaladdo', '-r', 'AVERAGE', '-ro', output_file_path, '2', '4', '8', '16', '32', '64']
                    addo_process = subprocess.Popen(addo_cmd)
                    addo_process.wait()
        else:
            print(f'Input file format is {-4:}, please select a .vrt format')


def vrt2tif_deelgebieden(deelgebieden_dir):
    """
    change vrt to tifs for all deelgebieden. Used for wadden deelgebieden.
    :param deelgebieden_dir: directory with deelgebieden tiles
    :return:
    """
    for deelgebied in os.listdir(deelgebieden_dir):
        vrt_dir = os.path.join(deelgebieden_dir, deelgebied, 'vrt_tiles')
        tif_dir = os.path.join(deelgebieden_dir, deelgebied, 'tif_tiles')
        create_dir(tif_dir)

        for vrt in os.listdir(vrt_dir):
            if vrt.endswith('.vrt'):
                input_path = os.path.join(vrt_dir, vrt)
                tile_name = f'{vrt[:-4]}.tif'
                output_file_path = os.path.join(tif_dir, tile_name)

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


def gdal_tiling(inputfile, outputfile, output_folder, tilesize_x, tilesize_y, tile_overlap):
    """
    Tiling using gdal. Equal to the function for vrt tiles, output as tif instead.
    :param inputfile:
    :param outputfile:
    :param output_folder:
    :param tilesize_x:
    :param tilesize_y:
    :param tile_overlap:
    :return:
    """
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
    create_dir(output_folder)

    # Create tiles with tilesize, using tilesteps in the lists
    x_tile_counter = 0  # tile counters for tile names
    for x in xlist:
        x_tile_counter += 1
        y_tile_counter = 0
        for y in ylist:
            y_tile_counter += 1

            output_tile_name = f'{outputfile}_{y_tile_counter}_{x_tile_counter}.tif'

            # check if tiles exist
            if os.path.isfile(output_tile_name):
                print(f'Tile {y_tile_counter}_{x_tile_counter} already exists...')
            else:
                # general gdal function and commands
                gdal_cmd = ['gdal_translate', '-a_srs', 'EPSG:28992', '-of', 'GTIFF', '-srcwin']
                # add tile specifications
                gdal_cmd.extend((str(x) + ',', str(y) + ',', str(tilesize_x) + ',', str(tilesize_y)))
                # in and output paths
                gdal_cmd.extend((inputfile, output_tile_name))

                # command that gdal will read as input
                com_string = "gdal_translate -a_srs EPSG:28992 -of GTIFF -srcwin " + str(x) + ", " + str(
                    y) + ", " + str(tilesize_x) + ", " + str(tilesize_y) + " " + str(inputfile) + " " + str(
                    outputfile + '_') + str(y_tile_counter) + "_" + str(x_tile_counter) + ".tif"
                print(f'Creating tile {y_tile_counter}_{x_tile_counter}:')
                print(com_string + '\n')

                # subsetting, pass gdal_cmd with subprocess
                translate_process = subprocess.Popen(gdal_cmd)
                translate_process.wait()  # We wait for process to finish
                # creating pyramids
                addo_cmd = ['gdaladdo', '-r', 'AVERAGE', '-ro', output_tile_name, '2', '4', '8', '16', '32', '64']
                addo_process = subprocess.Popen(addo_cmd)
                addo_process.wait()

                if translate_process.returncode == 0:
                    print(f'Creating tile {y_tile_counter}_{x_tile_counter} complete!\n')
                else:
                    print(f'Creating tile {y_tile_counter}_{x_tile_counter} failed!\n')
    print('Creating tiles done!')


def create_tile_extents(input_raster_dir_path,
                        output_extents_path, tile_extents_name):
    """
    Create an index file with extents of the input rasters.
    :param input_raster_dir_path: directory with rasters of which to create the index
    :param output_extents_path: directory where the output file should go
    :param tile_extents_name: name of the new file.
    :return:
    """
    images_folder = input_raster_dir_path

    # Creating output folder
    create_dir(output_extents_path)

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
        print(f'output file {output} already exists')
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
            tile_number = f'{tile_name_parts[3]}_{tile_name_parts[4]}'
            feature.SetField('TileNumber', tile_number)
            layer.SetFeature(feature)
        layer.ResetReading()
        shapefile = None


def raster_subset_with_tileindex_tiles(tile_index_shapefile, input_raster,
                                       output_path):
    """
    Use tile extents from the tile-index file to subset rasters from a raster file.
    :param tile_index_shapefile: Tile index shapefile created with 'create_tile_extents'
    :param input_raster: Raster to subset
    :param output_path: output directory for new raster tiles
    :return:
    """
    shapefile = ogr.Open(tile_index_shapefile)
    layer = shapefile.GetLayer(0)

    # Create temp shapefile
    new_raster_folder = output_path
    create_dir(new_raster_folder)

    temp_shp = os.path.join(new_raster_folder, 'temp_shape.shp')

    out_driver = ogr.GetDriverByName("ESRI Shapefile")
    # delete shapefile if it exists
    if os.path.exists(temp_shp):
        out_driver.DeleteDataSource(temp_shp)
        print(f'deleting file {temp_shp}')
    # Create the output shapefile
    # temp_data_source = out_driver.CreateDataSource(temp_shp)
    # temp_layer = temp_data_source.CreateLayer("layer", geom_type=ogr.wkbPolygon)

    for feature in layer:
        tile_number = feature.GetField('TileNumber')
        # Create the output shapefile
        temp_data_source = out_driver.CreateDataSource(temp_shp)
        temp_layer = temp_data_source.CreateLayer("layer", geom_type=ogr.wkbPolygon)
        temp_layer.CreateFeature(feature)
        temp_data_source = None

        hoogte_raster_tile = os.path.join(new_raster_folder, f'tile_{tile_number}.tif')

        if os.path.exists(hoogte_raster_tile):
            print(f'{hoogte_raster_tile} already exists')
        else:
            print(f'Creating tile {hoogte_raster_tile}')
            gdal.Warp(hoogte_raster_tile, input_raster,
                      cutlineDSName=temp_shp,
                      cropToCutline=True)

        if os.path.exists(temp_shp):
            #        print 'resetting {}' %(temp_shp)
            out_driver.DeleteDataSource(temp_shp)
    layer.ResetReading()
    shapefile = None


def cut_overlap_from_tiles(input_folder, output_folder, tile_overlap):
    """
    Remove overlap from the raster tiles and output as vrt.
    :param input_folder: input directory with original raster tiles
    :param output_folder: output directory for output vrt files
    :param tile_overlap: overlap of the tiles.
    :return:
    """
    # Create list of images in the image folder
    image_list = []
    tile_row_list = []
    tile_column_list = []
    for files in os.listdir(input_folder):
        if files.endswith('.tif') or files.endswith('.vrt'):
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
    create_dir(output_folder)

    # Creating tempoutput folder
    temp_output_folder = os.path.join(output_folder, 'temp_tile_rasters')
    create_dir(temp_output_folder)

    vrt_list = []

    for files in os.listdir(input_folder):

        if files.endswith('.tif') or files.endswith('.vrt'):
            image_path = os.path.join(input_folder, files)
            output_tile_name = os.path.join(temp_output_folder, files[:-4] + '.vrt')
            vrt_list.append(output_tile_name)
            tile_row, tile_column = files[:-4].split('_')[-2:]
            tile_row = int(tile_row)
            tile_column = int(tile_column)
            # general gdal function and commands
            gdal_cmd = ['gdal_translate', '-a_srs', 'EPSG:28992', '-of', 'VRT', '-srcwin']

            if os.path.exists(output_tile_name):
                print(f'{output_tile_name} Already exists')
            else:
                print(f'Processing {output_tile_name}')
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


def create_mosaic_from_shp_tiles(tile_index_shapefile, shapefile_input_folder,
                                 output_path, output_shp_name, gdal_bat,
                                 mosaic=True):
    """
    Cut the shapefiles into the correct extent with a tile index of the tile extents without overlap.
    Merge the resulting shapefiles into a mosaic.
    :param tile_index_shapefile: tile index of the tiles without overlap
    :param shapefile_input_folder: directory for with classification result shapefiles
    :param output_path: directory for output
    :param output_shp_name: output name prefix
    :param gdal_bat: batfile for gdal.
    :param mosaic: Boolean value. True creates a mosaic, False skips the mosaic part.
    :return:
    """
    shapefile = ogr.Open(tile_index_shapefile)
    layer = shapefile.GetLayer(0)

    # Create temp shapefile
    clipped_shapefile_folder = os.path.join(output_path, '01_Clipped_Tiles')
    create_dir(clipped_shapefile_folder)

    temp_shp = os.path.join(clipped_shapefile_folder, 'temp_shape.shp')

    out_driver = ogr.GetDriverByName("ESRI Shapefile")
    # delete shapefile if it exists
    if os.path.exists(temp_shp):
        out_driver.DeleteDataSource(temp_shp)
        print(f'deleting file {temp_shp}')

    # Create the output shapefile
    # temp_data_source = out_driver.CreateDataSource(temp_shp)
    # temp_layer = temp_data_source.CreateLayer("layer", geom_type=ogr.wkbPolygon)

    for feature in layer:
        tile_number = feature.GetField('TileNumber')
        # Create the output shapefile
        temp_data_source = out_driver.CreateDataSource(temp_shp)
        temp_layer = temp_data_source.CreateLayer("layer", geom_type=ogr.wkbPolygon)
        temp_layer.CreateFeature(feature)
        temp_data_source = None

        # shapefile_input = os.path.join(shapefile_input_folder,
        #                              'tile_' + tile_number + '.shp')
        # clipped_shapefile = os.path.join(clipped_shapefile_folder,
        #                                'tile_' + tile_number + '.shp')

        shapefile_input = os.path.join(shapefile_input_folder,
                                      'class_tile_' + tile_number + '.shp')
        clipped_shapefile = os.path.join(clipped_shapefile_folder,
                                        'tile_' + tile_number + '.shp')


        if os.path.exists(clipped_shapefile):
            print(f'{clipped_shapefile} already exists')
        elif not os.path.exists(shapefile_input):
            print(f'There is no {shapefile_input} for input')
        else:
            print(f'Creating tile {clipped_shapefile}')
            ogr2ogr_cmd = [gdal_bat,  # making sure ogr functions work
                           'ogr2ogr',  # ogr function
                           '-clipsrc', temp_shp,  # clipping extent
                           clipped_shapefile, shapefile_input,  # out- and input
                           '-nlt', 'POLYGON',  # output type
                           '-skipfailures']  # skip failed features
            #            for item in ogr2ogr_cmd[1:]:
            #                print item,

            ogr2ogr_cmd = ['ogr2ogr',  # ogr function
                           '-clipsrc', temp_shp,  # clipping extent
                           clipped_shapefile, shapefile_input,  # out- and input
                           '-nlt', 'POLYGON',  # output type
                           '-skipfailures']  # skip failed features
            #            for item in ogr2ogr_cmd[1:]:

            # ogr2ogr_process = subprocess.Popen(ogr2ogr_cmd)
            ogr2ogr_process = subprocess.check_call(ogr2ogr_cmd)
            #ogr2ogr_process.wait()

            #check = ogr2ogr_process.returncode
            check = 0
            if check == 0:
                print(f'\nClipping tile {clipped_shapefile} complete!\n')
            else:
                print(f'\nClipping tile {clipped_shapefile} failed!\n')

        if os.path.exists(temp_shp):
            #        print 'resetting {}' %(temp_shp)
            out_driver.DeleteDataSource(temp_shp)

    layer.ResetReading()
    shapefile = None

    if mosaic:
        shapefile_mosaic_path = os.path.join(output_path, output_shp_name + '.shp')
        print("Creating mosaic")

        if not os.path.exists(shapefile_mosaic_path):
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
                    print(f'Merging {file_} with {output_shp_name}.shp')

                    merge_process = subprocess.Popen(shp_merge_cmd)
                    merge_process.wait()
        else:
            print('Mosaic already exists')


# Functies voor eCognition cmd client
def create_ecog_workspace(workspace_cmd_client, workspace_file, image_folder,
                          import_template, import_template_path):
    """
    Creates an eCognition workspace using the command line interface of eCognition.
    :param workspace_cmd_client: command line client executable of eCognition workspace
    :param workspace_file: filename for the workspace
    :param image_folder: directory with images, or root directory in case of using the customized import
    :param import_template: name of the template for the customized import algorithm
    :param import_template_path: directory with import templates (xml files)
    :return:
    """
    wsp_cmd = [workspace_cmd_client,
               workspace_file,
               image_folder,
               import_template,
               "",
               import_template_path]

    if os.path.exists(workspace_file):
        print(f'Workspace already exists {workspace_file}...')
    else:
        print(f'Creating workspace {workspace_file}...')
        create_wsp_process = subprocess.Popen(wsp_cmd)
        create_wsp_process.wait()  # We wait for process to finish

        if create_wsp_process.returncode == 0:
            print('Creating workspace succesfull!')
        else:
            print('creating workspace failed!')


def analyze_ecog_workspace(ecognition_cmd_client, workspace_file, ruleset_path):
    """
    Send the ecognition workspace up for analysis using the ecognition server.
    With the nature of the project when developing this, the use of this function is not that usefull
    :param ecognition_cmd_client: command line client executable of eCognition
    :param workspace_file: workspace file
    :param ruleset_path: path for the ruleset to be used for the workspace analysis.
    :return:
    """
    analyze_cmd = [ecognition_cmd_client,
                   'sw',
                   workspace_file,
                   ruleset_path]

    print(f'Analysing images in workspace {workspace_file}...')
    analyze_process = subprocess.Popen(analyze_cmd)
    analyze_process.wait()  # We wait for process to finish

    if analyze_process.returncode == 0:
        print('Processing images succesfull')
    else:
        print('Processing images failed')
