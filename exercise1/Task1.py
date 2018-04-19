import matplotlib.pyplot as plt
import numpy as np

def exercise1(nc,data_lats):
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
    ax.set_ylim(270, 310)
    ax.set_xlabel("Latitude")
    ax.set_ylabel("Temperature [K]")
    ax.grid()

    plt.tight_layout()
    # plt.show()
    plt.savefig("Images/Task1.pdf")
    plt.close()