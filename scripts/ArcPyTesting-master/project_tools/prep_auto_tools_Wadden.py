import os
from shutil import copyfile
from osgeo import gdal
from gdal import ogr
import subprocess


def create_vrt_mosaic(images_folder, output_folder, output_mosaic_name):
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
    if not os.path.exists(output_folder):
        print('Creating output folder: {} \n'.format(output_folder))
        os.mkdir(output_folder)
    else:
        print('Output folder {} already exists\n'.format(output_folder))

    # Check if output file already exists
    output_mosaic_name = f'{output_mosaic_name}.vrt'
    mosaic_file = os.path.join(output_folder, output_mosaic_name)
    if os.path.isfile(mosaic_file):
        print('{} already exists.'.format(mosaic_file))
    else:
        print('Creating vrt mosaic:')
        gdal.BuildVRT(mosaic_file, image_list)
        print('Creating vrt mosaic done!')

        if os.path.exists(image_list_file):
            os.remove(image_list_file)


def gdal_tiling_vrt(inputfile, outputfile, output_folder, tilesize_x, tilesize_y, tile_overlap):
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


def select_vrt_kom(kom_shapefile, tile_dir):
    shapefile = ogr.Open(kom_shapefile)
    layer = shapefile.GetLayer(0)

    tile_index_file = os.path.join(tile_dir, '01b_tiles_index', 'TileIndex.shp')

    # create output folder
    output_dir = os.path.join(tile_dir, 'Deelgebieden')
    if os.path.exists(output_dir):
        print('{} already exists'.format(output_dir))
    else:
        print('Creating new dir {}'.format(output_dir))
        os.mkdir(output_dir)

    outDriver = ogr.GetDriverByName("ESRI Shapefile")

    # Save each feature in a new shapfile and intersect with tile index
    for feature in layer:
        feature_name = feature.GetField('DEELGEBIED')

        feature_dir = os.path.join(output_dir, feature_name)
        if os.path.exists(feature_dir):
            print('{} already exists'.format(feature_dir))
        else:
            print('Creating new dir {}'.format(feature_dir))
            os.mkdir(feature_dir)

        deelgebied_path = os.path.join(feature_dir, f'{feature_name}.shp')
        deelgebied_data_source = outDriver.CreateDataSource(deelgebied_path)
        deelgebied_layer = deelgebied_data_source.CreateLayer("layer", geom_type=ogr.wkbPolygon)
        deelgebied_layer.CreateFeature(feature)
        deelgebied_data_source = None

        output_tile_index = os.path.join(feature_dir, f'tile_index_{feature_name}.shp')

        # create ogr2ogr command
        ogr2ogr_command = ['ogr2ogr', '-f', "ESRI Shapefile",
                           output_tile_index, tile_index_file,
                           '-dialect', 'sqlite', 'sql',
                           f'SELECT TI.Geometry '
                           f'FROM {deelgebied_path}.deelgebied DG, {tile_index_file}.tile_index TI '
                           f'WHERE ST_Contains(DG.geometry, TI.geometry)']
        ogr_process = subprocess.Popen(ogr2ogr_command)
        ogr_process.wait()


def copy_vrt_per_deelgebied(deelgebieden_dir):
    for deelgebied in os.listdir(deelgebieden_dir):
        index_file = os.path.join(deelgebied, 'tiles_index_*.shp')
        shapefile = ogr.Open(index_file)
        layer = shapefile.GetLayer(0)

        vrt_dir = os.path.join(deelgebieden_dir, 'vrt_tiles')

        if os.path.exists(vrt_dir):
            print('{} already exists'.format(vrt_dir))
        else:
            print('Creating new dir {}'.format(vrt_dir))
            os.mkdir(vrt_dir)

        for feature in layer:
            vrt_path = feature.GetField('location')
            copyfile(vrt_path, deelgebieden_dir)
