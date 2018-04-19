import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset

def mean_me(var):
    var = np.asarray(var)
    tot_1 = np.roll(var, 1, axis=0)
    var = np.subtract(var, tot_1)
    var[0] = tot_1[-1]
    var = np.mean(var, axis=0)
    var = np.mean(var, axis=1)
    return var

def exercise4(files):
    tot = []
    conv = []
    large = []
    for file in sorted(files, reverse=False):

        nc = Dataset(file)

        time = str(nc.variables["time"][0])
        if int(time[4:6]) != 2:
            continue
        lat = nc.variables["lat"][:].copy()
        tot.append(np.mean(nc.variables["tot_prec"][:, :, :], axis=0))  # daily mean
        conv.append(np.mean(np.add(
            nc.variables["snow_con"][:, :, :],
            nc.variables["rain_con"][:, :, :],
            ), axis=0))  #  daily mean
        large.append(np.mean(np.add(
            nc.variables["snow_gsp"][:, :, :],
            nc.variables["rain_gsp"][:, :, :],
            ), axis=0))  #  daily mean

    # convert accumulated values to total values:
    tot = mean_me(tot)
    conv = mean_me(conv)
    large = mean_me(large)

    fig,ax = plt.subplots()
    ax.plot(lat,tot,label="total")
    ax.plot(lat, conv, label="convective")
    ax.plot(lat, large,label="large-scale")
    ax.set_title("Zonal Mean Precipitation (February)")
    ax.set_xlabel("Latitude")
    ax.set_ylabel("Precipitation [mm/m2]")
    ax.set_xlim(-90,90)
    ax.set_ylim(0,20)

    plt.legend(loc="upper right")

    plt.show()
    plt.savefig("Images/Task4.pdf")
    plt.close()