import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset

def exercise7(file_list,level_file_list,lon,lat):
    d_last = 0
    var = "tot_prec"
    precip = np.zeros([len(file_list),len(lat), len(lon)]).astype(float)
    months = []
    for i, file in enumerate(sorted(file_list)):

        nc = Dataset(file)
        if nc.variables[var][:].ndim == 3:
            precip[i,:, :] = nc.variables[var][0, :, :].copy()
        else:
            precip[i,:, :] = nc.variables[var][0, 0, :, :].copy()

        m = str(nc.variables["time"][0].copy())
        d = int(m[6:8])
        m = int(m[:6])
        # print(m)
        months.append(m)
        if d < d_last:
            print(d,d_last)
            if not "prec_january" in locals():
                prec_january = precip[i,:,:].copy()

        d_last = d
    # print(prec_january)
    prec_feb = precip[-1,:,:].copy()
    # print(prec_feb)

    prec_feb = np.subtract(prec_feb,prec_january)
    prec_feb = np.divide(prec_feb,28)

    # Get wind:
    u = []
    v = []
    for file in sorted(level_file_list):

        nc = Dataset(file)
        time = str(nc.variables["time"][0])
        # print(time[4:6])
        if int(time[4:6]) != 2:
            continue
        print(time[4:6])

        u.append(np.mean(nc.variables["u"][:, -1, :, :],axis=0))
        v.append(np.mean(nc.variables["v"][:, -1, :, :],axis=0))
        nc.close()

    u = np.mean(np.asarray(u),axis=0)
    v = np.mean(np.asarray(v), axis=0)

    dist = 4
    print(u.shape,v.shape)


    fig,ax = plt.subplots()
    im = ax.contourf(lon,lat,prec_feb,levels=np.linspace(0,30,31))
    plt.colorbar(im, label="Precipiation [mm/d]")
    ax.quiver(lon[::dist],lat[::dist],u[::dist,::dist],v[::dist,::dist],color="white",linewidth=10,
              antialiased=True,alpha=0.8)
    ax.set_xlabel("Lonitude")
    ax.set_ylabel("Latitude")
    ax.set_title("Monthly Mean Precipitation and \n Horizontal Wind at Surface (February )")
    plt.show()
    name="Task7"
    plt.savefig("Images/%s.pdf"%name)
    plt.close()

