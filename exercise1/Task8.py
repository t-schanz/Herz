import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset
from matplotlib.ticker import ScalarFormatter

def exercise8(level_files):
    # Get wind:
    z = []
    for file in level_files:

        nc = Dataset(file)
        lat = nc.variables["lat"][:].copy()
        p = np.divide(nc.variables["lev"][:].copy(),100) # hPa


        time = str(nc.variables["time"][0])
        if int(time[4:6]) != 2:
            continue

        z.append(np.mean(nc.variables["u"][:, :, :, :],axis=0)) # time mean over day


    z = np.asarray(z)
    z = np.mean(z,axis=0) # monthly mean
    z = np.mean(z, axis=2) # zonal mean
    print(z.shape)
    fig,ax = plt.subplots()
    im = ax.contourf(lat,p,z,cmap="bwr",levels=np.linspace(-20,50,71))
    cont = ax.contour(lat,p,z,levels=[35])
    cb = plt.colorbar(im,ticks=np.arange(-20,51,5), label="Zonal Windspeed [m/s]")
    cb.add_lines(cont)
    ax.set_yscale("log")
    ax.yaxis.set_major_formatter(ScalarFormatter())
    ax.yaxis.set_minor_formatter(ScalarFormatter())
    ax.set_xlabel("Latitude")
    ax.set_ylabel("Pressure [hPa]")
    ax.set_title("Monthly zonal mean of zonal Windspeed (February)")
    plt.gca().invert_yaxis()

    plt.show()
    plt.savefig("Images/Task8.pdf")
    plt.close()
