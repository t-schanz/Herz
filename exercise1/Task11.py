import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset


def exercise11(files):
    rain = []
    for file in sorted(files,reverse=False):

        nc = Dataset(file)

        time = str(nc.variables["time"][0])
        if int(time[4:6]) != 2:
            continue
        lat = nc.variables["lat"][:].copy()
        trop_high = np.max(np.where(lat <= 30))
        trop_low = np.min(np.where(lat >= -30))
        rain.append(np.sum(nc.variables["tot_prec"][:, trop_low:trop_high, :],axis=0 ))  # only tropics, daily mean

    # convert accumulated values to total values:
    rain = np.asarray(rain)
    rain_1 = np.roll(rain,1,axis=0)
    rain = np.subtract(rain,rain_1)
    rain[0] = rain[-1]

    # get daily mean:
    rain = np.reshape(rain,rain.shape[0]*rain.shape[1]*rain.shape[2])
    print(rain)
    print(rain.shape)

    binwidth=1
    fig,ax = plt.subplots()
    num_bins = np.arange(min(rain), max(rain) + binwidth, binwidth)
    ax.hist(rain, bins=num_bins)
    # ax.set_yscale("log")
    ax.set_ylim(0,4000)
    ax.set_xlim(0,1000)
    ax.set_title("Daily rain rates in the Tropics (February)")
    ax.set_ylabel("Number of Events")
    ax.set_xlabel("Rain Rate [mm/d]")
    plt.show()
    plt.savefig("Images/Task11_normal.pdf")
    plt.close()

    # PDF:
    fig, ax = plt.subplots()
    n, bins, patches = ax.hist(rain, bins=num_bins, density=1)
    ax.set_title("PDF of daily rain rates in the Tropics (February)")
    ax.set_xlabel("Rain Rate [mm/d]")
    ax.set_ylabel("Probability")
    ax.set_xlim(0,1000)
    ax.set_ylim(0,0.03)
    plt.show()
    plt.savefig("Images/Task11_PDF.pdf")
    plt.close()


