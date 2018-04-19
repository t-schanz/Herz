import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset
from functions import get_zonal_dayly_mean

def exercise5(file_list,data_lats):
    prec = ["rain","snow"]
    vars = ["tot_prec","_gsp", "_con"]
    names = ["total","large-scale","convective"]

    for var,name in zip(vars,names):
        if not var[0] == "_":
            cl_dayly = get_zonal_dayly_mean(var,file_list,data_lats)
        else:
            for pr in prec:
                var_new = pr + var
                if not "dl" in locals():
                    dl = get_zonal_dayly_mean(var_new,file_list,data_lats)
                else:
                    dl = np.add(dl, get_zonal_dayly_mean(var_new,file_list,data_lats))
            cl_dayly = dl
            del dl


        # Global precip:
        global_cl = np.mean(cl_dayly)
        print("Global Mean %s Precipitation: %.2f kg/m2"%(name,global_cl))

        # Tropical precip:
        trop_high = np.max(np.where(data_lats <= 30))
        trop_low = np.min(np.where(data_lats >= -30))
        # print(trop_low,trop_high)

        tropical_cl = np.mean(cl_dayly[:,trop_low:trop_high])
        print("Tropical Mean %s Precipitation: %.2f kg/m2" % (name, tropical_cl))

        # Subtropical precipitation:
        sub_high = np.max(np.where(data_lats <= 60))
        sub_low = np.min(np.where(data_lats >= 30))
        subtropical_cl = np.mean(cl_dayly[:,sub_low:sub_high])
        print("Subtropical Mean %s Precipitation: %.2f kg/m2" % (name, subtropical_cl))