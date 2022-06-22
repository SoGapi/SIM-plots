import libs.visualization as vis
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from libs.constants import *

# ----------------------------------------------------------------------
# User input for the location of the files
# ----------------------------------------------------------------------

dataset10 = vis.Arctic(
    directory="output10_1997",
    time="1997-01-01-00-00",
    expno="12",
    datatype="u",
    fig_shape="round",
    save=1,
    resolution=10,
    fig_name_supp="_97",
)

dataset10D = vis.Arctic(
    directory="output10D_1997",
    time="1997-01-01-00-00",
    expno="01",
    datatype="u",
    fig_shape="round",
    save=1,
    resolution=10,
    fig_name_supp="D_97",
)

dataset10Dadv = vis.Arctic(
    directory="output10Dadvection_1997",
    time="1997-01-01-00-00",
    expno="03",
    datatype="u",
    fig_shape="round",
    save=1,
    resolution=10,
    fig_name_supp="Dadv_97",
)


dataset_RGPS = vis.Arctic(
    fig_shape="round", save=1, resolution=12.5, fig_name_supp="_02_RGPS",
)

# ----------------------------------------------------------------------

# dataset10.arctic_plot(dataset10.load())
# dataset.multi_load("01-00-00", "1997-03-31-00-00")

dt = "00-06-00"
time_end = "1997-01-31-18-00"


# ----------------------------------------------------------------------
# load everthing, compute du, mask du with RGPS80
# ----------------------------------------------------------------------

# mask80
# mask80 = dataset_RGPS.mask80("RGPS_data", ti=-1, tf=88)
mask80 = np.load("RGPS_mask/mask80JFM.npy")

# calcul time averaged
u_v = dataset10.multi_load(dt, time_end)
u_v_D = dataset10D.multi_load(dt, time_end)
u_v_Dadv = dataset10Dadv.multi_load(dt, time_end)
u_v = np.where(u_v == 0, np.NaN, u_v)
u_v_D = np.where(u_v_D == 0, np.NaN, u_v_D)
u_v_Dadv = np.where(u_v_Dadv == 0, np.NaN, u_v_Dadv)
u_v_ta = dataset10._time_average(u_v, dt)
u_v_ta_D = dataset10D._time_average(u_v_D, dt)
u_v_ta_Dadv = dataset10Dadv._time_average(u_v_Dadv, dt)

# calcul du
du = dataset10._derivative(u_v_ta[:, :, 0, :], u_v_ta[:, :, 1, :])
du_D = dataset10D._derivative(u_v_ta_D[:, :, 0, :], u_v_ta_D[:, :, 1, :])
du_Dadv = dataset10Dadv._derivative(
    u_v_ta_Dadv[:, :, 0, :], u_v_ta_Dadv[:, :, 1, :]
)
# mask the data
du80 = du
du80_D = du_D
du80_Dadv = du_Dadv
du80[..., 0], mask = dataset10.mask80_times(du[..., 0], mask80)
du80[..., 1] = dataset10.mask80_times(du[..., 1], mask80)[0]
du80[..., 2] = dataset10.mask80_times(du[..., 2], mask80)[0]
du80[..., 3] = dataset10.mask80_times(du[..., 3], mask80)[0]
du80_D[..., 0] = dataset10D.mask80_times(du_D[..., 0], mask80)[0]
du80_D[..., 1] = dataset10D.mask80_times(du_D[..., 1], mask80)[0]
du80_D[..., 2] = dataset10D.mask80_times(du_D[..., 2], mask80)[0]
du80_D[..., 3] = dataset10D.mask80_times(du_D[..., 3], mask80)[0]
du80_Dadv[..., 0] = dataset10Dadv.mask80_times(du_Dadv[..., 0], mask80)[0]
du80_Dadv[..., 1] = dataset10Dadv.mask80_times(du_Dadv[..., 1], mask80)[0]
du80_Dadv[..., 2] = dataset10Dadv.mask80_times(du_Dadv[..., 2], mask80)[0]
du80_Dadv[..., 3] = dataset10Dadv.mask80_times(du_Dadv[..., 3], mask80)[0]

# RGPS data
# deps, div, shear = dataset_RGPS.nc_load("RGPS_data/w0102n_3dys.nc", tf=29)
# load derivatives and mask it
dudx = dataset_RGPS.mask80_times_RGPS(
    np.load("RGPS_derivatives/DUDX.npy"), mask80
)
dudy = dataset_RGPS.mask80_times_RGPS(
    np.load("RGPS_derivatives/DUDY.npy"), mask80
)
dvdx = dataset_RGPS.mask80_times_RGPS(
    np.load("RGPS_derivatives/DVDX.npy"), mask80
)
dvdy = dataset_RGPS.mask80_times_RGPS(
    np.load("RGPS_derivatives/DVDY.npy"), mask80
)

# stack them
du80_RGPS = np.stack((dudx, dudy, dvdx, dvdy), axis=-1)

# ----------------------------------------------------------------------
# plot PDF
# ----------------------------------------------------------------------

du80_stack = [du80, du80_Dadv, du80_RGPS]

dataset10.pdf_du(du80_stack, save=1, fig_name_supp="_97")

# ----------------------------------------------------------------------
# SCALING
# ----------------------------------------------------------------------

# calcul du sclaing spatial
deps10, shear10, div10, scale10 = dataset10.spatial_mean_du(du80, L10)

deps10D, shear10D, div10D, scale10D = dataset10D.spatial_mean_du(du80_D, L10)

(
    deps10Dadv,
    shear10Dadv,
    div10Dadv,
    scale10Dadv,
) = dataset10Dadv.spatial_mean_du(du80_Dadv, L10)

(
    deps_RGPS_du,
    shear_RGPS_du,
    div_RGPS_du,
    scale_RGPS_du,
) = dataset_RGPS.spatial_mean_du(du80_RGPS, L_RGPS)

# meme chose mais pour le scaling temporel
deps10_T, shear10_T, div10_T, scale10_T = dataset10.temporal_mean_du(du80, T10)

deps10D_T, shear10D_T, div10D_T, scale10D_T = dataset10D.temporal_mean_du(
    du80_D, T10
)

(
    deps10Dadv_T,
    shear10Dadv_T,
    div10Dadv_T,
    scale10Dadv_T,
) = dataset10Dadv.temporal_mean_du(du80_Dadv, T10)

(
    deps_RGPS_du_T,
    shear_RGPS_du_T,
    div_RGPS_du_T,
    scale_RGPS_du_T,
) = dataset_RGPS.temporal_mean_du(du80_RGPS, T10)


# ----------------------------------------------------------------------
# save data in file
# ----------------------------------------------------------------------

np.save("processed_data/deps10D.npy", deps10D)
np.save("processed_data/shear10D.npy", shear10D)
np.save("processed_data/div10D.npy", div10D)
np.save("processed_data/scale10D.npy", scale10D)

np.save("processed_data/deps10Dadv.npy", deps10Dadv)
np.save("processed_data/shear10Dadv.npy", shear10Dadv)
np.save("processed_data/div10Dadv.npy", div10Dadv)
np.save("processed_data/scale10Dadv.npy", scale10Dadv)

np.save("processed_data/deps10.npy", deps10)
np.save("processed_data/shear10.npy", shear10)
np.save("processed_data/div10.npy", div10)
np.save("processed_data/scale10.npy", scale10)

# np.save("processed_data/deps_RGPS.npy", deps_RGPS)
# np.save("processed_data/shear_RGPS.npy", shear_RGPS)
# np.save("processed_data/div_RGPS.npy", div_RGPS)
# np.save("processed_data/deps_scale_RGPS.npy", deps_scale_RGPS)
# np.save("processed_data/shear_scale_RGPS.npy", shear_scale_RGPS)
# np.save("processed_data/div_scale_RGPS.npy", div_scale_RGPS)

# ----------------------------------------------------------------------
# load data if previously saved
# ----------------------------------------------------------------------

# deps10 = np.load("processed_data/deps10.npy", allow_pickle=True)
# shear10 = np.load("processed_data/shear10.npy", allow_pickle=True)
# div10 = np.load("processed_data/div10.npy", allow_pickle=True)
# scale10 = np.load("processed_data/scale10.npy", allow_pickle=True)

# deps10D = np.load("processed_data/deps10D.npy", allow_pickle=True)
# shear10D = np.load("processed_data/shear10D.npy", allow_pickle=True)
# div10D = np.load("processed_data/div10D.npy", allow_pickle=True)
# scale10D = np.load("processed_data/scale10D.npy", allow_pickle=True)

# deps10Dadv = np.load("processed_data/deps10Dadv.npy", allow_pickle=True)
# shear10Dadv = np.load("processed_data/shear10Dadv.npy", allow_pickle=True)
# div10Dadv = np.load("processed_data/div10Dadv.npy", allow_pickle=True)
# scale10Dadv = np.load("processed_data/scale10Dadv.npy", allow_pickle=True)

# deps_RGPS = np.load("processed_data/deps_RGPS.npy", allow_pickle=True)
# shear_RGPS = np.load("processed_data/shear_RGPS.npy", allow_pickle=True)
# div_RGPS = np.load("processed_data/div_RGPS.npy", allow_pickle=True)
# deps_scale_RGPS = np.load(
#     "processed_data/deps_scale_RGPS.npy", allow_pickle=True
# )
# shear_scale_RGPS = np.load(
#     "processed_data/shear_scale_RGPS.npy", allow_pickle=True
# )
# div_scale_RGPS = np.load(
#     "processed_data/div_scale_RGPS.npy", allow_pickle=True
# )

# ----------------------------------------------------------------------
# plots at 10 km
# ----------------------------------------------------------------------

# dataset10.pdf_plot_vect(def10, L10)
# dataset10.cdf_plot(data_box10)
mean_deps, mean_scale, __ = dataset10.scale_plot_vect(
    deps10, scale10, L10, save=0, fig_name_supp="_dedt_97"
)
mean_depsD, mean_scaleD, __ = dataset10D.scale_plot_vect(
    deps10D, scale10D, L10, save=0, fig_name_supp="D_dedt_97"
)
mean_depsDadv, mean_scaleDadv, __ = dataset10Dadv.scale_plot_vect(
    deps10Dadv, scale10Dadv, L10, save=0, fig_name_supp="Dadv_dedt_97"
)

# ----------------------------------------------------------------------
# plots RGPS 12.5 km
# ----------------------------------------------------------------------

(mean_deps_RGPS_du, mean_scale_RGPS_du, __,) = dataset_RGPS.scale_plot_vect(
    deps_RGPS_du,
    scale_RGPS_du,
    L_RGPS,
    save=0,
    fig_name_supp="_dedt_02_RGPS_du",
)

# ----------------------------------------------------------------------
# multiplot scaling
# ----------------------------------------------------------------------

mean_deps_stack = np.stack(
    (mean_deps, mean_depsDadv, mean_deps_RGPS_du), axis=1,
)
mean_scale_stack = np.stack(
    (mean_scale, mean_scaleDadv, mean_scale_RGPS_du), axis=1,
)

mean_deps_stack_T = np.stack((deps10_T, deps10Dadv_T, deps_RGPS_du_T), axis=1,)
mean_scale_stack_T = np.stack(
    (scale10_T, scale10Dadv_T, scale_RGPS_du_T), axis=1,
)

dataset10.multi_plot_spatial(
    mean_deps_stack, mean_scale_stack, fig_name_supp="_dedt_97"
)

dataset10.multi_plot_temporal(
    mean_deps_stack_T, mean_scale_stack_T, fig_name_supp="_dedt_97"
)

# ----------------------------------------------------------------------
# multifractality
# ----------------------------------------------------------------------

# spatial
parameters10, coeff10 = dataset10.multifractal_spatial(3, deps10, scale10,)

parameters10D, coeff10D = dataset10D.multifractal_spatial(
    3, deps10D, scale10D,
)

parameters10Dadv, coeff10Dadv = dataset10Dadv.multifractal_spatial(
    3, deps10Dadv, scale10Dadv,
)

parametersRGPS, coeffRGPS = dataset_RGPS.multifractal_spatial(
    3, deps_RGPS_du, scale_RGPS_du, RGPS=1,
)

param_stack = np.stack(
    (parameters10, parameters10Dadv, parametersRGPS), axis=1,
)

coeff_stack = np.stack((coeff10, coeff10Dadv, coeffRGPS), axis=1,)

dataset10.multifractal_plot(param_stack, coeff_stack, 3, 1, "_param_97")

# temporal
parameters10_T, coeff10_T = dataset10.multifractal_temporal(3, du80)

parameters10D_T, coeff10D_T = dataset10D.multifractal_temporal(3, du80_D)

parameters10Dadv_T, coeff10Dadv_T = dataset10Dadv.multifractal_temporal(
    3, du80_Dadv
)

parametersRGPS_T, coeffRGPS_T = dataset_RGPS.multifractal_temporal(
    3, du80_RGPS
)

param_stack_T = np.stack(
    (parameters10_T, parameters10Dadv_T, parametersRGPS_T), axis=1,
)

coeff_stack_T = np.stack((coeff10_T, coeff10Dadv_T, coeffRGPS_T), axis=1,)

dataset10.multifractal_plot(
    param_stack_T, coeff_stack_T, 3, 1, "T_param_97", temp=1
)

