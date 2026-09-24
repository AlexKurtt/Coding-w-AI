# Visualize mass data
# The point of this script is to visualize how bee mass changes across altitudes using two species
# of bees. Each species has specimens from both low and high altitudes. 
# Data is stored in a csv file names Bee mass dist.csv

# This line imports the pandas library, which gives us tools to read CSV files and work with data in a table-like structure called a DataFrame.
import pandas as pd

# This line imports the os library, which allows us to interact with the computer's file system and create file paths that work correctly on different systems.
import os

# This line imports matplotlib.pyplot, which is the part of Matplotlib used to make charts and plots in Python.
import matplotlib.pyplot as plt

# This line imports numpy so we can add a little random jitter to each data point when overlaying them on the violin plots.
import numpy as np

# This line creates the folder path to the Bee Mass Distributions folder where the data file is saved.
# It uses the folder where this script is stored, so the path stays tied to this project folder.
script_dir = os.path.dirname(os.path.abspath(__file__))

# This line combines the Bee Mass Distributions folder path with the CSV file name.
# This gives Python the exact location of the data file and keeps the code simple and easy to understand.
data_path = os.path.join(script_dir, "Bee mass dist.csv")

# This line reads the CSV file into a DataFrame, which is like a spreadsheet in Python where rows and columns are easy to access.
# pd.read_csv tells pandas to open the file and convert it into a table.
df = pd.read_csv(data_path)

# This line keeps only the three columns we need for this analysis: the bee species, the altitude, and the mass.
# The double brackets create a new DataFrame with only those selected columns.
df = df[["species code", "altitude", "mass"]]

# This line changes the column name "species code" to "species" so the column name is shorter and easier to work with.
# The rename method creates a dictionary that matches the old name to the new name.
df = df.rename(columns={"species code": "species"})

# This line creates an empty list called grouped_data.
# This list will hold the average mass for each species at each altitude after we calculate it.
grouped_data = []

# This line starts a loop that goes through the DataFrame grouped by both species and altitude.
# df.groupby(["species", "altitude"]) creates groups for every unique combination of species and altitude.
# For each group, Python gives two values: species and group.
for species, group in df.groupby(["species", "altitude"]):

# This line calculates the mean mass for the current group of bees.
# group["mass"] selects the mass values in that group, and .mean() finds the average value.
    mean_mass = group["mass"].mean()

# This line appends a new tuple to grouped_data containing the species name, altitude, and mean mass.
# A tuple is a fixed collection of values, and append adds it to the list.
    grouped_data.append((species[0], species[1], mean_mass))

# This line converts the list of grouped values into a new DataFrame.
# pd.DataFrame creates a table from a list of rows, and columns names are given so each column has a label.
grouped_df = pd.DataFrame(grouped_data, columns=["species", "altitude", "mean_mass"])

# This line creates a figure with two plot panels side by side.
# plt.subplots(1, 2, figsize=(10, 5)) means 1 row, 2 columns, with each plot being 10 inches wide and 5 inches tall.
fig, axes = plt.subplots(1, 2, figsize=(10, 5))

# This line adds a title to the full figure so the viewer knows the chart compares bee mass across altitude for both species.
fig.suptitle("Bee Mass Across Altitude by Species")

# This line starts a loop that goes through each subplot and each species name.
# zip(axes, ["amel", "ecin"]) pairs the first subplot with "amel" and the second subplot with "ecin".
for ax, species_name in zip(axes, ["amel", "ecin"]):

# This line creates a new DataFrame with only the rows for the current species.
# grouped_df["species"] == species_name compares the species column to the active species name and keeps only matching rows.
    species_df = grouped_df[grouped_df["species"] == species_name]

# This line sorts the DataFrame by altitude from lowest to highest.
# This keeps the points in ascending altitude order so the line connects them correctly.
    species_df = species_df.sort_values("altitude")

# This line draws a line graph for the current species.
# ax.plot uses x-values = altitude and y-values = mean mass, with markers at each point and a line connecting them.
    ax.plot(species_df["altitude"], species_df["mean_mass"], marker="o", linewidth=2)

# This line labels the x-axis as Altitude so the reader knows the horizontal axis shows altitude values.
    ax.set_xlabel("Altitude")

# This line labels the y-axis as Mass (g) so the reader knows the vertical axis shows bee mass in grams.
    ax.set_ylabel("Mass (g)")

# This line sets the title for the current subplot to the species name and the word bees.
# f"{species_name} bees" inserts the species name into the title text.
    ax.set_title(f"{species_name} bees")

# This line adds a light dashed grid to the plot to make it easier to read values.
# True turns the grid on, linestyle="--" makes dashed lines, and alpha controls transparency.
    ax.grid(True, linestyle="--", alpha=0.5)

# This line adjusts the spacing around the plots so labels and titles do not overlap or get cut off.
plt.tight_layout()


# Start of boxplot code--------------------

# This line creates a second figure for boxplots so we can compare the distribution of mass values instead of only the mean mass.
# plt.subplots(1, 2, figsize=(10, 5)) again creates 2 side-by-side panels for the boxplots.
fig2, axes2 = plt.subplots(1, 2, figsize=(10, 5))

# This line adds a title to the full boxplot figure so the reader knows the chart is showing mass distribution across altitude.
fig2.suptitle("Bee Mass Distribution Across Altitude by Species")

# This line starts a loop that creates one boxplot panel for each bee species.
for ax, species_name in zip(axes2, ["amel", "ecin"]):

# This line keeps only the rows from the original dataframe that match the current species.
# This helps isolate the data for one species before building the boxplot.
    species_df = df[df["species"] == species_name]

# This line creates a two-item list of mass values for each altitude group.
# For species "amel", the low altitude is 200 and the high altitude is 2100.
# For species "ecin", the low altitude is 300 and the high altitude is 1250.
# This list is then used as the data input for the boxplot.
    altitude_groups = [species_df[species_df["altitude"] == 200]["mass"], species_df[species_df["altitude"] == 2100]["mass"]] if species_name == "amel" else [species_df[species_df["altitude"] == 300]["mass"], species_df[species_df["altitude"] == 1250]["mass"]]

# This line draws a boxplot using the two groups of mass values.
# A boxplot shows the median, quartiles, and possible outliers for each group.
    ax.boxplot(altitude_groups, patch_artist=True)

# This line sets the text labels under each box to show the altitude groups being compared.
# The first box is "Low altitude" and the second is "High altitude".
    ax.set_xticklabels(["Low altitude", "High altitude"])

# This line labels the x-axis as Altitude group so the viewer knows the boxes compare two altitude levels.
    ax.set_xlabel("Altitude group")

# This line labels the y-axis as Mass (g) so the viewer knows the measurements are bee masses in grams.
    ax.set_ylabel("Mass (g)")

# This line sets the title for the current subplot to the species name and the word bees.
    ax.set_title(f"{species_name} bees")

# This line adds a light dashed horizontal grid to the boxplot to make the values easier to read.
    ax.grid(True, axis="y", linestyle="--", alpha=0.5)

# This line adjusts the spacing around the second figure so all labels and titles fit neatly.
plt.tight_layout()


# -----------------------------------------------------------------------------------------------------------
# Create an even more comprehensive version of the previous plots, using violin graphs instead of boxplots
# To make the data more readily visible, I also want each data point for all bees overlayed on the violins

# This line creates a third figure for violin plots so we can compare the full mass distribution for each altitude group.
fig3, axes3 = plt.subplots(1, 2, figsize=(12, 5))

# This line adds a title to the overall violin plot figure so it is clear the chart compares distributions by species and altitude.
fig3.suptitle("Bee Mass Violin Plot Across Altitude by Species")

# This line loops over each bee species and draws a violin plot for the low and high altitude groups.
for ax, species_name in zip(axes3, ["amel", "ecin"]):

# This line keeps only the rows for the current species before creating the two altitude groups.
    species_df = df[df["species"] == species_name]

# This line chooses the exact low and high altitude values for the current species.
    altitude_levels = [200, 2100] if species_name == "amel" else [300, 1250]

# This line creates a list of mass values for each altitude, so the violin plot can be drawn for both groups.
    altitude_groups = [species_df[species_df["altitude"] == altitude]["mass"].tolist() for altitude in altitude_levels]

# This line draws the violin plot for the two altitude groups and shows the mean line inside each violin.
    violin_parts = ax.violinplot(altitude_groups, positions=[1, 2], widths=0.6, showmeans=True)

# This line styles the violin bodies so they are easy to distinguish and view.
    for body in violin_parts["bodies"]:
        body.set_facecolor("#8ecae6")
        body.set_edgecolor("black")
        body.set_alpha(0.75)

# This line overlays each individual bee mass as a scatter point with a tiny bit of horizontal jitter for readability.
    for i, group in enumerate(altitude_groups):
        if len(group) == 0:
            continue
        jitter = np.random.normal(0, 0.04, len(group))
        ax.scatter(np.full(len(group), i + 1) + jitter, group, color="#1f77b4", s=18, alpha=0.75, zorder=3)

# This line sets the x-tick labels so the viewer knows the two boxes represent low and high altitude.
    ax.set_xticks([1, 2])
    ax.set_xticklabels(["Low altitude", "High altitude"])

# This line labels the x-axis and y-axis so the plot is easy to interpret.
    ax.set_xlabel("Altitude group")
    ax.set_ylabel("Mass (g)")

# This line sets the title for the current subplot to the species name.
    ax.set_title(f"{species_name} bees")

# This line adds a light grid to make the mass values easier to read.
    ax.grid(True, axis="y", linestyle="--", alpha=0.5)

# This line adjusts spacing so the title, labels, and points all fit properly inside the figure.
plt.tight_layout()

# This line saves the final violin plot as a PNG in the folder containing this script.
fig3.savefig(os.path.join(script_dir, "bee_mass_violin_plot.png"), dpi=300, bbox_inches="tight")

# This line tells Python to display the final violin plot figure so the user can compare species and altitude distributions.
plt.show()