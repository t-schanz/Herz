import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset
from functions import plot_2D_data

def exercise6(files,lon,lat):
    nc = Dataset(files[1])
    data = nc.variables["tot_prec"][0,:,:].copy()
    nc.close()

    plot_2D_data(lon,lat,data,"Task6")