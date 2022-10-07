
#~ (pcrglobwb_python3) sutan101@velocity.geo.uu.nl:/scratch/sutan101/rws_obia/make_histograms$ ls -lah complete_raster/raster_2018_25cm/pcraster_maps/*mask_2018.map
#~ -r--r--r-- 1 sutan101 users 67G Nov 15 01:08 complete_raster/raster_2018_25cm/pcraster_maps/brightness_westerschelde_2018_mask_2018.map
#~ -r--r--r-- 1 sutan101 users 67G Nov 24 15:22 complete_raster/raster_2018_25cm/pcraster_maps/green_westerschelde_2018_mask_2018.map
#~ -r--r--r-- 1 sutan101 users 67G Nov 15 01:55 complete_raster/raster_2018_25cm/pcraster_maps/ndvi_westerschelde_2018_mask_2018.map
#~ -r--r--r-- 1 sutan101 users 67G Nov 24 15:23 complete_raster/raster_2018_25cm/pcraster_maps/nir_ratio_westerschelde_2018_mask_2018.map
#~ -r--r--r-- 1 sutan101 users 67G Nov 24 15:21 complete_raster/raster_2018_25cm/pcraster_maps/nir_westerschelde_2018_mask_2018.map
#~ -r--r--r-- 1 sutan101 users 67G Nov 24 17:33 complete_raster/raster_2018_25cm/pcraster_maps/plaat_brightness_westerschelde_2018_mask_2018.map
#~ -r--r--r-- 1 sutan101 users 67G Nov 24 17:11 complete_raster/raster_2018_25cm/pcraster_maps/plaat_green_westerschelde_2018_mask_2018.map
#~ -r--r--r-- 1 sutan101 users 67G Nov 18 22:46 complete_raster/raster_2018_25cm/pcraster_maps/plaat_ndvi_westerschelde_2018_mask_2018.map
#~ -r--r--r-- 1 sutan101 users 67G Nov 24 17:12 complete_raster/raster_2018_25cm/pcraster_maps/plaat_nir_ratio_westerschelde_2018_mask_2018.map
#~ -r--r--r-- 1 sutan101 users 67G Nov 24 17:11 complete_raster/raster_2018_25cm/pcraster_maps/plaat_nir_westerschelde_2018_mask_2018.map
#~ -r--r--r-- 1 sutan101 users 67G Nov 24 17:32 complete_raster/raster_2018_25cm/pcraster_maps/plaat_red_westerschelde_2018_mask_2018.map
#~ -r--r--r-- 1 sutan101 users 67G Nov 24 15:23 complete_raster/raster_2018_25cm/pcraster_maps/red_westerschelde_2018_mask_2018.map

set -x

gdalinfo -approx_stats complete_raster/raster_2018_25cm/pcraster_maps/plaat_ndvi_westerschelde_2018_mask_2018.map       > approx_stats_plaat_ndvi_westerschelde_2018_mask_2018.map.txt       &
gdalinfo -approx_stats complete_raster/raster_2018_25cm/pcraster_maps/plaat_nir_ratio_westerschelde_2018_mask_2018.map  > approx_stats_plaat_nir_ratio_westerschelde_2018_mask_2018.map.txt  &
gdalinfo -approx_stats complete_raster/raster_2018_25cm/pcraster_maps/plaat_nir_westerschelde_2018_mask_2018.map        > approx_stats_plaat_nir_westerschelde_2018_mask_2018.map.txt        &
gdalinfo -approx_stats complete_raster/raster_2018_25cm/pcraster_maps/plaat_brightness_westerschelde_2018_mask_2018.map > approx_stats_plaat_brightness_westerschelde_2018_mask_2018.map.txt &
gdalinfo -approx_stats complete_raster/raster_2018_25cm/pcraster_maps/plaat_green_westerschelde_2018_mask_2018.map      > approx_stats_plaat_green_westerschelde_2018_mask_2018.map.txt      &
gdalinfo -approx_stats complete_raster/raster_2018_25cm/pcraster_maps/brightness_westerschelde_2018_mask_2018.map       > approx_stats_brightness_westerschelde_2018_mask_2018.map.txt       &
wait

gdalinfo -stats complete_raster/raster_2018_25cm/pcraster_maps/plaat_ndvi_westerschelde_2018_mask_2018.map              > stats_plaat_ndvi_westerschelde_2018_mask_2018.map.txt       &
gdalinfo -stats complete_raster/raster_2018_25cm/pcraster_maps/plaat_nir_ratio_westerschelde_2018_mask_2018.map         > stats_plaat_nir_ratio_westerschelde_2018_mask_2018.map.txt  &
gdalinfo -stats complete_raster/raster_2018_25cm/pcraster_maps/plaat_nir_westerschelde_2018_mask_2018.map               > stats_plaat_nir_westerschelde_2018_mask_2018.map.txt        &
gdalinfo -stats complete_raster/raster_2018_25cm/pcraster_maps/plaat_brightness_westerschelde_2018_mask_2018.map        > stats_plaat_brightness_westerschelde_2018_mask_2018.map.txt &
gdalinfo -stats complete_raster/raster_2018_25cm/pcraster_maps/plaat_green_westerschelde_2018_mask_2018.map             > stats_plaat_green_westerschelde_2018_mask_2018.map.txt      &
gdalinfo -stats complete_raster/raster_2018_25cm/pcraster_maps/brightness_westerschelde_2018_mask_2018.map              > stats_brightness_westerschelde_2018_mask_2018.map.txt       &
wait

gdalinfo -hist complete_raster/raster_2018_25cm/pcraster_maps/plaat_ndvi_westerschelde_2018_mask_2018.map               > hist_plaat_ndvi_westerschelde_2018_mask_2018.map.txt       &
gdalinfo -hist complete_raster/raster_2018_25cm/pcraster_maps/plaat_nir_ratio_westerschelde_2018_mask_2018.map          > hist_plaat_nir_ratio_westerschelde_2018_mask_2018.map.txt  &
gdalinfo -hist complete_raster/raster_2018_25cm/pcraster_maps/plaat_nir_westerschelde_2018_mask_2018.map                > hist_plaat_nir_westerschelde_2018_mask_2018.map.txt        &
gdalinfo -hist complete_raster/raster_2018_25cm/pcraster_maps/plaat_brightness_westerschelde_2018_mask_2018.map         > hist_plaat_brightness_westerschelde_2018_mask_2018.map.txt &
gdalinfo -hist complete_raster/raster_2018_25cm/pcraster_maps/plaat_green_westerschelde_2018_mask_2018.map              > hist_plaat_green_westerschelde_2018_mask_2018.map.txt      &
wait

gdalinfo -hist complete_raster/raster_2018_25cm/pcraster_maps/brightness_westerschelde_2018_mask_2018.map               > hist_brightness_westerschelde_2018_mask_2018.map.txt       &
gdalinfo -hist complete_raster/raster_2018_25cm/pcraster_maps/ndvi_westerschelde_2018_mask_2018.map                     > hist_ndvi_westerschelde_2018_mask_2018.map.txt             &
wait

set +x


