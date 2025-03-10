# %%
import sys
sys.path.append("D:\\OneDrive - HKUST\\LongCOVIDCode\\scripts")

# %%
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from shapely.geometry import mapping, shape
from shapely.affinity import scale, translate
import shapely

from os.path import abspath

from info.keywords import labels

pd.options.display.float_format = '{:.15f}'.format

# %%
df = pd.read_pickle(abspath('./data/msv/joined_msvs.pkl'))
df = df.rolling(14).mean().iloc[13:, :]
coordinate_df = df.copy()

headers = list(df.columns)

angle_vec = list(np.linspace(start=0, stop=2 * np.pi, num=len(df)))
cos_vec = np.cos(angle_vec)
sin_vec = np.sin(angle_vec)

# %%
for index, header in enumerate(headers):
    # print(f"{header=}")
    msv_vec = df[header].values
    
    coordinate_df.insert((index * 2) + 1, f'{header}_y', np.multiply(msv_vec, sin_vec))
    coordinate_df.insert((index * 2) + 1, f'{header}_x', np.multiply(msv_vec, cos_vec))
coordinate_df.drop(columns=df.columns)


# %%
coordinates = [
    coordinate_df.iloc[:, [header in checking_header for checking_header in coordinate_df.columns]].values.tolist() for header in headers
]

# %%
fig, axs = plt.subplots(
    nrows=4, 
    ncols=6, 
    layout="constrained",
    sharey=True, 
    figsize=(8, 7.5),
    subplot_kw={'projection': 'polar'},
)
# axs.set_rticks([0.25, 0.5, 0.75, 1])

angle_vec.append(angle_vec[0])

output_pts = []
for index, header in enumerate(headers):
    row_number = int(index / 6)
    col_number = index % 6

    current_ax = axs[row_number][col_number]

    polygon_coordinates = coordinates[index]
    polygon = shapely.Polygon(polygon_coordinates)

    min_x = np.min(coordinate_df[f'{header}_x'])
    max_x = np.max(coordinate_df[f'{header}_x'])
    min_y = np.min(coordinate_df[f'{header}_y'])
    max_y = np.max(coordinate_df[f'{header}_y'])
    factor = 1 / max(abs(max_x), abs(min_x), abs(max_y), abs(min_y))

    msv_vec = list(np.multiply(df[header].values, factor))
    msv_vec.append(msv_vec[0])

    rescaled_polygon = scale(polygon, xfact=factor, yfact=factor, origin=(0, 0))

    current_ax.plot(angle_vec, msv_vec, label=labels[header])
    current_ax.set_title(labels[header], fontname="Arial", fontsize=8)

    centroid_pt = shapely.centroid(
        rescaled_polygon
    )
    centroid_radian = np.arctan2(centroid_pt.y, centroid_pt.x) / np.pi * 180
    centroid_distance = np.sqrt( np.square(centroid_pt.x) + np.square(centroid_pt.y) )
    print(f"{centroid_pt.x=}", f"{centroid_pt.y=}")
    print(f"{centroid_radian=}", f"{centroid_distance=}")

    current_ax.plot(
        centroid_radian,
        centroid_distance,
        marker="x",
        # markersize=20,
        markeredgecolor="tab:red",
        markerfacecolor="tab:red"
    )

    current_ax.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        labelbottom=False
    ) # labels along the bottom edge are off

    current_ax.tick_params(
        axis='y',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        left=False,      # ticks along the bottom edge are off
        right=False,         # ticks along the top edge are off
        labelleft=False
    ) # labels along the bottom edge are off

    current_ax.spines['polar'].set_visible(False)

for i in range(4):
    for j in range(6):
        axs[i][j].set_rmax(1.25)
        axs[i][j].set_rticks([0.25, 0.5, 0.75, 1.0])

axs[3][4].remove()
axs[3][5].remove()

plt.savefig('./graphs/20231118-RescaledPolarProjection_v2_MA(14).pdf')
plt.savefig('./graphs/20231118-RescaledPolarProjection_v2_MA(14).png')
plt.show()