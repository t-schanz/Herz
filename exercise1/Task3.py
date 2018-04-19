import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset

def exercise3(file_list,data_lats):

    vars = ["clct","clcl","clcm","clch"]
    names = ["total","low-level","middle-level","heigh-level"]

    # vars = ["clct"]
    # names = ["total"]
    for var,name in zip(vars,names):
        cl_dayly = np.zeros([len(file_list),len(data_lats)]).astype(float)
        months = []
        for i,file in enumerate(sorted(file_list)):
            nc = Dataset(file)
            if nc.variables[var][:].ndim == 3:
                cl_dayly[i,:] = np.mean(nc.variables[var][0,:,:].copy(),axis=1)
            else:
                cl_dayly[i,:] = np.mean(nc.variables[var][0,0,:,:].copy(),axis=1)

            m = str(nc.variables["time"][0].copy())
            m = int(m[:6])
            # print(m)
            months.append(m)

        # Global Cloudfraction:
        global_cl = np.mean(cl_dayly)
        print("Global Mean %s Cloudfraction: %.2f%%"%(name,global_cl))

        # Tropical Cloudfraction:
        trop_high = np.max(np.where(data_lats <= 30))
        trop_low = np.min(np.where(data_lats >= -30))
        # print(trop_low,trop_high)

        # print(cl_dayly.shape)
        tropical_cl = np.mean(cl_dayly[:,trop_low:trop_high])
        print("Tropical Mean %s Cloudfraction: %.2f%%" % (name, tropical_cl))

        # Subtropical cloud fraction:
        sub_high = np.max(np.where(data_lats <= 60))
        sub_low = np.min(np.where(data_lats >= 30))
        subtropical_cl = np.mean(cl_dayly[:,sub_low:sub_high])
        print("Subtropical Mean %s Cloudfraction: %.2f%%" % (name, subtropical_cl))