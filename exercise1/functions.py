import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap


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

def get_monthly_mean(var,file_list):
    """
    Only an idea yet.

    :param var:
    :param file_list:
    :return:
    """
    pass



def plot_2D_data(lon,lat,data,name="Test"):
    fig,ax = plt.subplots()
    im = ax.contourf(lon,lat,data)
    plt.colorbar(im)
    plt.show()
    plt.savefig("Images/%s.pdf"%name,dpi=300 )
    plt.close()


def plot_field_on_map(lat,lon,field,title=""):
    fig = plt.figure(figsize=(8,5))
    # m = Basemap(projection='cyl', llcrnrlat=-85, urcrnrlat=85, llcrnrlon=-180, urcrnrlon=180, resolution=None)
    m = Basemap(projection="mill", lon_0=0)
    parallels = np.arange(-180., 180., 45.)
    meridians = np.arange(-120., 140., 60.)

    m.drawmeridians(meridians, labels=[0, 0, 0, 1])
    m.drawparallels(parallels, labels=[1, 0, 0, 0] )

    # m.drawlsmask(land_color="dimgrey", ocean_color="white", lakes=True)
    m.drawcoastlines()
    m.drawmapboundary(fill_color='aqua')
    # m.fillcontinents(color='coral', lake_color='aqua', alpha=0.5)
    ny,nx = field.shape
    lons,lats = m.makegrid(nx,ny)
    x,y = m(lons,lats)
    # print(x)
    # print(x.shape)
    cs = m.contourf(x,y,field)
    cb = m.colorbar(cs,location="bottom",pad="5%",label="Precipitation")
    # plt.tight_layout()
    # plt.gca()
    # plt.subplots_adjust(bottom=-0.8)
    plt.savefig("Images/map.png",dpi=300)
    plt.show()
    plt.close()


def get_overall_time(files,var,mode="sum"):

    for file in files:
        nc = Dataset(file)
        if not "array" in locals():
            array = nc.variables[var][:].copy()
        else:
            array = np.add(array,nc.variables[var][:].copy())

        nc.close()

        if array.ndim == 3:
            array = array[0,:,:]
        else:
            array = array[0,0,:,:]

        if mode == "mean":
            array = np.divide(array,len(files))

    return array