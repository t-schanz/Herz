import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset

def windspeed(u,v):
    s = np.add(np.power(u,2),np.power(v,2))

    return np.sqrt(s)

def exercise9(level_files):
    # Get wind:
    u = []
    v = []
    for file in sorted(level_files):

        nc = Dataset(file)

        time = str(nc.variables["time"][0])
        # print(time[4:6])
        if int(time[4:6]) != 2:
            continue
        print(time[4:6])
        lat = nc.variables["lat"][:].copy()
        lon = nc.variables["lon"][:].copy()
        u.append(np.mean(nc.variables["u"][:,:, :, :],axis=0)) # daily mean
        v.append(np.mean(nc.variables["v"][:,:, :, :],axis=0)) # daily mean
        nc.close()

    u = np.asarray(u)
    v = np.asarray(v)
    u = np.mean(u,axis=0) # monthly mean
    v = np.mean(v,axis=0) # monthly mean
    u = np.sum(u, axis=0)  # sum up all heights
    v = np.sum(v, axis=0)  # sum up all heights
    s = windspeed(u,v)

    fig,ax = plt.subplots()

    im = ax.contourf(lon,lat,s,cmap="Oranges",levels=np.linspace(0,400,41))
    cb = plt.colorbar(im, label="summed windspeed [m/s]")
    conts = ax.contour(lon,lat,s,levels=[220])
    cb.add_lines(conts)
    ax.set_title("Monthly mean horizontal absolute windspeed \nsummed over all Heights (February)")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    plt.show()
    plt.savefig("Images/Task9.pdf")
    plt.close()
