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

import json
from os.path import abspath

from info.keywords import labels, tag_to_cluters, tag_to_colors

pd.options.display.float_format = '{:.15f}'.format

# %%
df = pd.read_pickle(abspath('./data/msv/joined_msvs.pkl'))
headers = list(df.columns)

angle_vec = np.linspace(start=0, stop=2 * np.pi, num=len(df))
cos_vec = np.cos(angle_vec)
sin_vec = np.sin(angle_vec)

print(len(angle_vec), angle_vec)
print(len(cos_vec), cos_vec)
print(len(sin_vec), sin_vec)

# %%
for index, header in enumerate(headers):
    msv_vec = df[header].values
    
    df.insert((index * 2) + 1, f'{header}_y', np.multiply(msv_vec, sin_vec))
    df.insert((index * 2) + 1, f'{header}_x', np.multiply(msv_vec, cos_vec))

df.drop(columns=headers, inplace=True)
# print(df.head())

# %%
coordinates = [df.iloc[:, [header in checking_header for checking_header in df.columns]].values.tolist() for header in headers]
# print(coordinates)

# # %%
# # print(df.values.flatten().tolist())
# # pdfFile = PdfPages('PolarPlots.pdf')
# for index, header in enumerate(headers):
#     luk = [header in checking_header for checking_header in df.columns]
#     # print(luk, "\t", header)
#     # print(df.iloc[:, luk].shape)
#     coordinates = df.iloc[:, luk].values.tolist()
#     print()
# #     fig = sns.scatterplot(data=df, x=header+"_x", y=header+"_y")
# #     plt.savefig('PolarPlots.%02d.pdf' % index)
# #     pdfFile.savefig(fig)
# # pdfFile.close()

# %%
fig, axs = plt.subplots(
    nrows=1, 
    ncols=5, 
    layout="constrained",
    sharey=True, 
    figsize=(18, 7.5),
)
fig.subplots_adjust(
    top=0.99,
    bottom=0.365,
    left=0.01,
    right=0.99,
    hspace=0.145,
    wspace=0.05,
)
output_pts = []
for index, header in enumerate(headers):

    # f = open("Polygon-%02d.json" % index, 'w')
    # f.write(json.dumps({
    #     "type": "Polygon",
    #     "coordinates": coordinates[index] + [coordinates[index][0]]
    # }))
    # f.close()

    #polygon_coordinates = coordinates[index] + [coordinates[index][0]]
    polygon_coordinates = coordinates[index]
    polygon = shapely.Polygon(polygon_coordinates)

    polygon_coordinate_matrix = np.array(polygon_coordinates)
    [min_x, min_y] = np.min(polygon_coordinate_matrix, axis=0)
    [max_x, max_y] = np.max(polygon_coordinate_matrix, axis=0)

    print(f"{header=}", polygon_coordinate_matrix)
    print(f"{header=}", max_x - min_x)
    print(f"{header=}", max_y - min_y)

    factor = 1 / max(abs(max_x), abs(min_x), abs(max_y), abs(min_y))
    print(f"{header=}", f"{factor=}")

    rescaled_polygon = scale(polygon, xfact=factor, yfact=factor, origin=(0, 0))
    print(f"{polygon=}")
    print(f"{rescaled_polygon=}")

    print(f"{rescaled_polygon.exterior.xy=}")

    axs[tag_to_cluters[header]].plot(*rescaled_polygon.exterior.xy, alpha=0.5, label=labels[header])
    axs[tag_to_cluters[header]].legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
                                       ncol=2)
    
    axs[tag_to_cluters[header]].tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        labelbottom=False
    ) # labels along the bottom edge are off

    axs[tag_to_cluters[header]].tick_params(
        axis='y',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        left=False,      # ticks along the bottom edge are off
        right=False,         # ticks along the top edge are off
        labelleft=False
    ) # labels along the bottom edge are off
    # plt.show()

    centroid_pt = shapely.centroid(
        # shapely.Polygon(polygon_coordinates)
        rescaled_polygon
    )
    print(index, centroid_pt.x, centroid_pt.y)

    output_pts.append([header, labels[header], tag_to_cluters[header], centroid_pt.x, centroid_pt.y])
plt.show()

# top=1.0,
# bottom=0.246,
# left=0.025,
# right=1.0,
# hspace=0.14,
# wspace=0.004

centroid_df = pd.DataFrame(output_pts, columns=['tag', 'label', 'cluster', 'x', 'y']).sort_values(by='cluster', axis=0)

centroid_df['label_x'] = centroid_df['x'] - 0.007
centroid_df['label_y'] = centroid_df['y'] + 0.01

centroid_df.to_csv('data/centroid.csv')

# %%
centroid_df['cluster'] = centroid_df['cluster'].astype(str)
sns.scatterplot(centroid_df, x='x', y='y', hue='cluster')
def label_point(x, y, val, ax):
    a = pd.concat({'x': x, 'y': y, 'val': val}, axis=1)
    for i, point in a.iterrows():
        ax.text(point['x']-.007, point['y']-0.01, str(point['val']))

label_point(centroid_df.x, centroid_df.y, centroid_df.label, plt.gca())

plt.show()