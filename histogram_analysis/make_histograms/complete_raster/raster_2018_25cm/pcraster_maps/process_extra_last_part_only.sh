
set -x

#~ pcrcalc nir_ratio_westerschelde_2018_mask_2018.map = "if(gmk_2018.map gt 0, nir_ratio_westerschelde_2018.map)" &
#~ pcrcalc nir_westerschelde_2018_mask_2018.map       = "if(gmk_2018.map gt 0, nir_westerschelde_2018.map)"       &
#~ pcrcalc green_westerschelde_2018_mask_2018.map     = "if(gmk_2018.map gt 0, green_westerschelde_2018.map)"     &
#~ pcrcalc red_westerschelde_2018_mask_2018.map       = "if(gmk_2018.map gt 0, red_westerschelde_2018.map)"       &

#~ wait

pcrcalc plaat_nir_ratio_westerschelde_2018_mask_2018.map = "if(ndvi_westerschelde_2018_mask_2018.map gt -0.25, if(ndvi_westerschelde_2018_mask_2018.map lt 0.04, nir_ratio_westerschelde_2018_mask_2018.map))" &
pcrcalc plaat_nir_westerschelde_2018_mask_2018.map = "if(ndvi_westerschelde_2018_mask_2018.map gt -0.25, if(ndvi_westerschelde_2018_mask_2018.map lt 0.04, nir_westerschelde_2018_mask_2018.map))" &
pcrcalc plaat_green_westerschelde_2018_mask_2018.map = "if(ndvi_westerschelde_2018_mask_2018.map gt -0.25, if(ndvi_westerschelde_2018_mask_2018.map lt 0.04, green_westerschelde_2018_mask_2018.map))" &

wait

pcrcalc plaat_red_westerschelde_2018_mask_2018.map = "if(ndvi_westerschelde_2018_mask_2018.map gt -0.25, if(ndvi_westerschelde_2018_mask_2018.map lt 0.04, red_westerschelde_2018_mask_2018.map))" &
pcrcalc plaat_brightness_westerschelde_2018_mask_2018.map = "if(ndvi_westerschelde_2018_mask_2018.map gt -0.25, if(ndvi_westerschelde_2018_mask_2018.map lt 0.04, brightness_westerschelde_2018_mask_2018.map))" &

wait

set +x

