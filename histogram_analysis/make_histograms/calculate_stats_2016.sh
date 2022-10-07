
set -x

gdalinfo -approx_stats complete_raster/raster_2016_25cm/pcraster_maps/plaat_ndvi_westerschelde_2016_mask_2018.map       > approx_stats_plaat_ndvi_westerschelde_2016_mask_2018.map.txt       &
gdalinfo -approx_stats complete_raster/raster_2016_25cm/pcraster_maps/plaat_nir_ratio_westerschelde_2016_mask_2018.map  > approx_stats_plaat_nir_ratio_westerschelde_2016_mask_2018.map.txt  &
gdalinfo -approx_stats complete_raster/raster_2016_25cm/pcraster_maps/plaat_nir_westerschelde_2016_mask_2018.map        > approx_stats_plaat_nir_westerschelde_2016_mask_2018.map.txt        &
gdalinfo -approx_stats complete_raster/raster_2016_25cm/pcraster_maps/plaat_brightness_westerschelde_2016_mask_2018.map > approx_stats_plaat_brightness_westerschelde_2016_mask_2018.map.txt &
gdalinfo -approx_stats complete_raster/raster_2016_25cm/pcraster_maps/plaat_green_westerschelde_2016_mask_2018.map      > approx_stats_plaat_green_westerschelde_2016_mask_2018.map.txt      &
gdalinfo -approx_stats complete_raster/raster_2016_25cm/pcraster_maps/brightness_westerschelde_2016_mask_2018.map       > approx_stats_brightness_westerschelde_2016_mask_2018.map.txt       &
wait

gdalinfo -stats complete_raster/raster_2016_25cm/pcraster_maps/plaat_ndvi_westerschelde_2016_mask_2018.map              > stats_plaat_ndvi_westerschelde_2016_mask_2018.map.txt       &
gdalinfo -stats complete_raster/raster_2016_25cm/pcraster_maps/plaat_nir_ratio_westerschelde_2016_mask_2018.map         > stats_plaat_nir_ratio_westerschelde_2016_mask_2018.map.txt  &
gdalinfo -stats complete_raster/raster_2016_25cm/pcraster_maps/plaat_nir_westerschelde_2016_mask_2018.map               > stats_plaat_nir_westerschelde_2016_mask_2018.map.txt        &
gdalinfo -stats complete_raster/raster_2016_25cm/pcraster_maps/plaat_brightness_westerschelde_2016_mask_2018.map        > stats_plaat_brightness_westerschelde_2016_mask_2018.map.txt &
gdalinfo -stats complete_raster/raster_2016_25cm/pcraster_maps/plaat_green_westerschelde_2016_mask_2018.map             > stats_plaat_green_westerschelde_2016_mask_2018.map.txt      &
gdalinfo -stats complete_raster/raster_2016_25cm/pcraster_maps/brightness_westerschelde_2016_mask_2018.map              > stats_brightness_westerschelde_2016_mask_2018.map.txt       &
wait

gdalinfo -hist complete_raster/raster_2016_25cm/pcraster_maps/plaat_ndvi_westerschelde_2016_mask_2018.map               > hist_plaat_ndvi_westerschelde_2016_mask_2018.map.txt       &
gdalinfo -hist complete_raster/raster_2016_25cm/pcraster_maps/plaat_nir_ratio_westerschelde_2016_mask_2018.map          > hist_plaat_nir_ratio_westerschelde_2016_mask_2018.map.txt  &
gdalinfo -hist complete_raster/raster_2016_25cm/pcraster_maps/plaat_nir_westerschelde_2016_mask_2018.map                > hist_plaat_nir_westerschelde_2016_mask_2018.map.txt        &
gdalinfo -hist complete_raster/raster_2016_25cm/pcraster_maps/plaat_brightness_westerschelde_2016_mask_2018.map         > hist_plaat_brightness_westerschelde_2016_mask_2018.map.txt &
gdalinfo -hist complete_raster/raster_2016_25cm/pcraster_maps/plaat_green_westerschelde_2016_mask_2018.map              > hist_plaat_green_westerschelde_2016_mask_2018.map.txt      &
wait

gdalinfo -hist complete_raster/raster_2016_25cm/pcraster_maps/brightness_westerschelde_2016_mask_2018.map               > hist_brightness_westerschelde_2016_mask_2018.map.txt       &
gdalinfo -hist complete_raster/raster_2016_25cm/pcraster_maps/ndvi_westerschelde_2016_mask_2018.map                     > hist_ndvi_westerschelde_2016_mask_2018.map.txt             &
wait

set +x

