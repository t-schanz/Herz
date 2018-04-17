from socket import gethostname
from netCDF4 import Dataset
import glob
from mpl_toolkits.basemap import Basemap, cm
from datetime import datetime as dt
import numpy as np
import matplotlib.pyplot as  plt


# def num2time(num_str):
#     num_str.split(".")
#     f = np.vectorize(dt.strptime("%Y%m%d.%f"))
#     return f(num)

def print_nc_info(nc):
    for key in list(nc.variables.keys()):
        print("==============================================")
        print(nc.variables[key])

def get_zonal_dayly_mean(var,file_list,data_lats):
    cl_dayly = np.zeros([len(file_list), len(data_lats)]).astype(float)
    months = []
    for i, file in enumerate(sorted(file_list)):

        nc = Dataset(file)
        if nc.variables[var][:].ndim == 3:
            cl_dayly[i, :] = np.mean(nc.variables[var][0, :, :].copy(), axis=1)
        else:
            cl_dayly[i, :] = np.mean(nc.variables[var][0, 0, :, :].copy(), axis=1)

        m = str(nc.variables["time"][0].copy())
        m = int(m[:6])
        # print(m)
        months.append(m)

    return cl_dayly

def exercise1(nc):
    # ===================
    # Task 1:
    # ===================
    sfc_T = nc.variables["t_g"][0, :, :].copy()

    print(sfc_T.shape)

    zonal_mean_sfc_T = np.mean(sfc_T, axis=1)
    print(zonal_mean_sfc_T.shape)

    fig1, ax = plt.subplots()
    ax.plot(data_lats, zonal_mean_sfc_T, lw=2)
    ax.set_title("Zonal Mean Sfc Temperature")
    # ax.set_xlim(-90,90)
    ax.set_ylim(270, 300)
    ax.set_xlabel("Latitude [°N]")
    ax.set_ylabel("Temperature [K]")
    ax.grid()

    plt.tight_layout()
    # plt.show()
    plt.savefig("Images/Task1.pdf",dpi=300)
    plt.close()

def exercise2(file_list,data_lats):
    # loading data from all files:
    cl_array = np.zeros([len(file_list),len(data_lats)]).astype(float)
    months = []
    for i,file in enumerate(sorted(file_list)):
        nc = Dataset(file)
        cl_array[i,:] = np.mean(nc.variables["clct"][0,:,:].copy(),axis=1)
        m = str(nc.variables["time"][0].copy())
        m = int(m[:6])
        # print(m)
        months.append(m)

    # averaging over months:
    m_last = months[0]
    same = []
    cl_monthly = np.zeros([2,len(data_lats)]).astype(float)
    counter = 0
    for i,m in enumerate(months):
        if m == m_last:
            same.append(cl_array[i,:])
        else:
            same = np.asarray(same)
            cl_monthly[counter,:] = np.mean(same,axis=0)
            counter += 1
            same = []

        m_last = m


    # plotting results:
    months = np.asarray(months)

    ticks = [0.5,1.5]
    labels = ["January","February"]
    print(data_lats.shape)
    fig2,ax = plt.subplots()
    im = ax.pcolor(data_lats,np.arange(0,3),cl_monthly)
    plt.yticks(ticks,labels)
    plt.colorbar(im, label="Cloud Fraction [%]")
    ax.set_xlabel("Latitude [°N]")
    plt.show()
    plt.savefig("Images/Task2.pdf",dpi=300)
    plt.close()


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




if __name__ == "__main__":

    print(gethostname())

    path = "/work/mh1049/u300844/ICON/icon-nwp/experiments/nh_ape_nwp_ss17/"
    files = glob.glob(path + "nh_ape_nwp*ML*.nc")
    print(files)

    nc = Dataset(files[1])
    data_lons = nc.variables["lon"][:].copy()
    data_lats = nc.variables["lat"][:].copy()
    # data_time = nc.variables["time"][:].copy().astype(str)
    # print_nc_info(nc)
    # exercise1(nc)
    nc.close()

    exercise5(files,data_lats)