import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset
from matplotlib.ticker import ScalarFormatter

def plot_zonal(lat,p,data,title,c_label,cmap="bwr",levels=None,ticks=None,zero_line=False):
    fig, ax = plt.subplots()
    im = ax.contourf(lat, p, data, cmap=cmap, levels=levels)
    cb = plt.colorbar(im, ticks=ticks, label=c_label)
    ax.set_yscale("log")
    ax.yaxis.set_major_formatter(ScalarFormatter())
    ax.yaxis.set_minor_formatter(ScalarFormatter())
    ax.set_xlabel("Latitude")
    ax.set_ylabel("Pressure [hPa]")
    ax.set_title("Monthly Zonal Mean %s (February)"%title)
    if zero_line:
        ax.contour(lat,p,data,levels=[1])
    plt.gca().invert_yaxis()

    plt.show()
    plt.savefig("Images/Task10_%s.pdf"%title)
    plt.close()

def mean_me(var):
    var = np.asarray(var)
    var = np.mean(var, axis=0)  # monthly mean
    var = np.mean(var, axis=2)  # zonal mean
    return var

def exercise10(level_files):
    cw = []
    ci = []
    rh = []
    for file in level_files:

        nc = Dataset(file)



        time = str(nc.variables["time"][0])
        if int(time[4:6]) != 2:
            continue
        lat = nc.variables["lat"][:].copy()
        p = np.divide(nc.variables["lev"][:].copy(),100) # hPa
        cw.append(np.mean(nc.variables["tot_qc_dia"][:, :, :, :],axis=0)) # time mean over day
        ci.append(np.mean(nc.variables["tot_qi_dia"][:, :, :, :],axis=0)) # time mean over day
        rh.append(np.mean(nc.variables["rh"][:, :, :, :],axis=0)) # time mean over day

    cw = mean_me(cw)
    cw = np.multiply(cw,1e5)
    ci = mean_me(ci)
    ci = np.multiply(ci,1e5)
    rh = mean_me(rh)

    # plot_zonal(lat,p,cw,"Cloud Water","cloud water [10$^{-5}$ kg/kg]",cmap="Blues",
    #            levels = np.linspace(0,7,14),
    #            ticks=np.arange(0,8,1))
    #
    # plot_zonal(lat,p,ci,"Cloud Ice","cloud ice [10$^{-5}$ kg/kg]",cmap="Blues",
    #            levels = np.linspace(0,1,11),
    #            ticks=np.arange(0,1.1,0.1))
    #
    # plot_zonal(lat,p,rh,"Relative Humidity","relative humidity [%]",cmap="Blues",
    #            levels = np.linspace(0,100,21),
    #            ticks=np.arange(0,101,20))

    # Define cloud where rh >= 99%
    threshold = 99
    cc = []
    for file in level_files:

        nc = Dataset(file)

        time = str(nc.variables["time"][0])
        if int(time[4:6]) != 2:
            continue
        lat = nc.variables["lat"][:].copy()
        p = np.divide(nc.variables["lev"][:].copy(), 100)  # hPa
        cc.append(nc.variables["rh"][:, :, :, :])  # time mean over day

    cc = np.asarray(cc)
    cc[np.where(cc < threshold)] = 0
    cc[np.where(cc >= threshold)] = 1

    cc = np.mean(cc,axis=0) # daily mean
    cc = np.mean(cc, axis=0) # monthly mean
    cc = np.mean(cc, axis=2) # zonal mean
    cc = np.multiply(cc,100)

    plot_zonal(lat, p, cc, "Cloud Cover", "cloud cover [%]", cmap="Blues",
                levels=np.linspace(0,25,26),
                ticks=np.arange(0,26,5),
                zero_line=True)



