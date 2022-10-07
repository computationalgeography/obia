

set -x

gdal_translate -b 1 -ot Float32 -of PCRaster ../Westerschelde_2016.tif nir_westerschelde_2016.map   &
gdal_translate -b 2 -ot Float32 -of PCRaster ../Westerschelde_2016.tif red_westerschelde_2016.map   &
gdal_translate -b 3 -ot Float32 -of PCRaster ../Westerschelde_2016.tif green_westerschelde_2016.map &
wait

mapattr -s -P yb2t *.map
rm *.xml

# use at least 24 workers
export PCRASTER_NR_WORKER_THREADS=24

# brightness
pcrcalc brightness_westerschelde_2016.map = "(nir_westerschelde_2016.map + red_westerschelde_2016.map + green_westerschelde_2016.map) / 3" 

# NDVI = (NIR - Red) / (NIR + Red)
pcrcalc ndvi_westerschelde_2016.map = "(nir_westerschelde_2016.map - red_westerschelde_2016.map) / (nir_westerschelde_2016.map + red_westerschelde_2016.map)" 

# use only the classifcation boundaries from 2018
ln -s /scratch/sutan101/rws_obia/make_histograms/gmk_shapefiles/gmk_2018.map 
pcrcalc brightness_westerschelde_2016_mask_2018.map = "if(gmk_2018.map gt 0, brightness_westerschelde_2016.map)"
pcrcalc ndvi_westerschelde_2016_mask_2018.map = "if(gmk_2018.map gt 0, ndvi_westerschelde_2016.map)"

set +x



