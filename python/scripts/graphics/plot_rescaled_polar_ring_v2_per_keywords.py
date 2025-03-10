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
from datetime import date, timedelta

from info.keywords import labels

pd.options.display.float_format = '{:.15f}'.format

# %%
date_vec = [date.fromisoformat('2020-01-01')]
while date_vec[-1] < date.fromisoformat('2023-12-31'):
    date_vec.append(date_vec[-1] + timedelta(days=1))

df = pd.read_pickle(abspath('./data/msv/joined_msvs.pkl'))
coordinate_df = df.copy()

headers = list(df.columns)

angle_vec = list(np.linspace(start=0, stop=2 * np.pi, num=len(date_vec)))
sin_vec = np.sin(angle_vec)
cos_vec = np.cos(angle_vec)

mapper_df = pd.DataFrame({
    "date": date_vec,
    "angle": angle_vec,
    "sin": sin_vec,
    "cos": cos_vec
})

__MAJOR_REFERENCE_DATE = [
    date.fromisoformat('2020-01-01'),
    date.fromisoformat('2021-01-01'),
    date.fromisoformat('2022-01-01'),
    date.fromisoformat('2023-01-01'),
]

__MINOR_REFERENCE_DATE = [
    date.fromisoformat('2020-04-01'),
    date.fromisoformat('2021-04-01'),
    date.fromisoformat('2022-04-01'),
    date.fromisoformat('2023-04-01'),

    date.fromisoformat('2020-07-01'),
    date.fromisoformat('2021-07-01'),
    date.fromisoformat('2022-07-01'),
    date.fromisoformat('2023-07-01'),

    date.fromisoformat('2020-10-01'),
    date.fromisoformat('2021-10-01'),
    date.fromisoformat('2022-10-01'),
    date.fromisoformat('2023-10-01'),
]

# %%
# prune reference vector
angle_vec = angle_vec[:len(df)]
angle_vec.append(angle_vec[0]) # backfill

sin_vec = sin_vec[:len(df)]
cos_vec = cos_vec[:len(df)]

# %%
# Coordinate calculation
for index, header in enumerate(headers):
    msv_vec = df[header].values
    
    coordinate_df.insert((index * 2) + 1, f'{header}_y', np.multiply(msv_vec, sin_vec))
    coordinate_df.insert((index * 2) + 1, f'{header}_x', np.multiply(msv_vec, cos_vec))

coordinate_df.drop(columns=df.columns)

# coordinates = [
#     coordinate_df.iloc[:, [header in checking_header for checking_header in coordinate_df.columns]].values.tolist() for header in headers
# ]


# %%
output_pts = []
for index, header in enumerate(headers):
    fig, axs = plt.subplots(
        nrows=1, 
        ncols=1, 
        layout="constrained",
        sharey=True, 
        figsize=(5, 4.2),
        subplot_kw={'projection': 'polar'},
    )

    current_ax = axs

    """
     Centroid Calculation
    """

    min_x = np.min(coordinate_df[f'{header}_x'])
    max_x = np.max(coordinate_df[f'{header}_x'])
    min_y = np.min(coordinate_df[f'{header}_y'])
    max_y = np.max(coordinate_df[f'{header}_y'])
    rectsys_corr_factor = 1 / max(abs(max_x), abs(min_x), abs(max_y), abs(min_y))

    # msv_vec = list(np.multiply(df[header].values, factor))
    msv_vec = list(np.multiply(df[header].values, 1/np.max(df[header].values)))
    msv_vec.append(msv_vec[0])

    current_ax.plot(angle_vec, msv_vec, label=labels[header], linewidth=1)
    current_ax.set_title(
        labels[header].replace("\n", ""), 
        pad=10,
        # fontname="Arial", 
        # fontsize=8
    )

    """
     Plot centroids
    """
    [centroid_x, centroid_y] = (coordinate_df[[f'{header}_x', f'{header}_y']].mean() * rectsys_corr_factor).values

    centroid_theta_radian = np.arctan2(centroid_y, centroid_x)
    centroid_r = np.sqrt(np.square(centroid_x) + np.square(centroid_y))

    print(f"{centroid_theta_radian=}")
    print(f"{centroid_r=}")

    current_ax.scatter(centroid_theta_radian, centroid_r, color="tab:red", zorder=99)
    # current_ax.scatter(centroid_theta_radian, 1, color="tab:orange")

    """
     Tickers
    """
    major_ticks_luk = [date_value in __MAJOR_REFERENCE_DATE for date_value in mapper_df['date'].values] 
    minor_ticks_luk = [date_value in __MINOR_REFERENCE_DATE for date_value in mapper_df['date'].values] 

    major_theta_df = mapper_df[ major_ticks_luk ]
    minor_theta_df = mapper_df[ minor_ticks_luk ]

    major_theta_df['date_label'] = pd.to_datetime(major_theta_df['date'], format="%Y-%m-%d").dt.strftime("%B\n%Y")
    minor_theta_df['date_label'] = pd.to_datetime(minor_theta_df['date'], format="%Y-%m-%d").dt.strftime("%b\n%Y")

    current_ax.set_xticks(major_theta_df['angle'].values, minor=False)
    current_ax.set_xticks(minor_theta_df['angle'].values, minor=True)
    current_ax.set_xticklabels(major_theta_df['date_label'].values, minor=False)
    current_ax.set_xticklabels(minor_theta_df['date_label'].values, minor=True)

    """
     Set ticker position
    """
    # for tick_index, tick in enumerate(current_ax.xaxis.get_majorticklabels()):
    #     if tick_index == 0:
    #         tick.set_horizontalalignment("left")
    #     elif tick_index == 2:
    #         tick.set_horizontalalignment("right")

    # for tick_index, tick in enumerate(current_ax.xaxis.get_minorticklabels()):
    #     if tick_index == 0 or tick_index == 3:
    #         tick.set_horizontalalignment("left")
    #     elif tick_index == 1 or tick_index == 2:
    #         tick.set_horizontalalignment("right")

    current_ax.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        # labelbottom=False
    ) # labels along the bottom edge are off

    current_ax.tick_params(
        axis='y',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        left=False,      # ticks along the bottom edge are off
        right=False,         # ticks along the top edge are off
        labelleft=False
    ) # labels along the bottom edge are off

    """
     Grid
    """
    current_ax.spines['polar'].set_visible(False)
    current_ax.xaxis.grid(visible=True, which='major', linestyle='-', linewidth=1)
    current_ax.xaxis.grid(visible=True, which='minor', linestyle='--', linewidth=1)
    current_ax.yaxis.grid(visible=True, which='both', linestyle=':', linewidth=1)

    current_ax.set_rmax(1.1)
    current_ax.set_rticks([0.25, 0.5, 0.75, 1.0])


    plt.savefig(f'./graphs/20231120-LCV-PolarPlots/PDF/20231118-RescaledPolarProjection_{index}.pdf')
    plt.savefig(f'./graphs/20231120-LCV-PolarPlots/PNG/20231118-RescaledPolarProjection_{index}.png')

    plt.close()

# axs[3][4].remove()
# axs[3][5].remove()

# plt.savefig('./graphs/20231118-RescaledPolarProjection_v2.pdf')
# plt.savefig('./graphs/20231118-RescaledPolarProjection_v2.png')
# plt.show()