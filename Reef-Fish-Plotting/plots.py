# Import sys so the script can use the current Python interpreter.
import sys

# Import subprocess so Python can run package installation commands.
import subprocess

# Import importlib.util to check whether packages are installed.
import importlib.util

# Import Path to create Windows-compatible file paths.
from pathlib import Path

# Check whether pandas is installed.
if importlib.util.find_spec("pandas") is None:
    # Install pandas using the Python interpreter running this script.
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas"])

# Check whether matplotlib is installed.
if importlib.util.find_spec("matplotlib") is None:
    # Install matplotlib using the Python interpreter running this script.
    subprocess.check_call([sys.executable, "-m", "pip", "install", "matplotlib"])

# Import pandas for reading and grouping CSV data.
import pandas as pd

# Import pyplot for creating plots.
import matplotlib.pyplot as plt

# Find the folder containing this Python file.
project_folder = Path(__file__).parent

# Create the path to the CSV data file.
csv_file = project_folder / "ReefFish.csv"

# Read the CSV file into a pandas DataFrame.
data = pd.read_csv(csv_file)

# Set the correct order for the months on the graph.
month_order = ["January", "February"]

# Group abundance by reef, month, and species.
abundance = data.groupby(["Site", "Month", "Species"], as_index=False)["Abundance"].sum()

# Create two side-by-side panels with a shared vertical axis.
fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)

# Loop through each panel and reef name.
for axis, reef in zip(axes, sorted(abundance["Site"].unique())):
    # Select data for the current reef.
    reef_data = abundance[abundance["Site"] == reef]

    # Loop through each species found at the current reef.
    for species in sorted(reef_data["Species"].unique()):
        # Select data for the current species.
        species_data = reef_data[reef_data["Species"] == species]

        # Use months as row labels and arrange them chronologically.
        species_data = species_data.set_index("Month").reindex(month_order)

        # Plot abundance changes for the current species.
        axis.plot(month_order, species_data["Abundance"], marker="o", label=species)

    # Add the reef name to the panel title.
    axis.set_title(reef)

    # Label the horizontal axis.
    axis.set_xlabel("Month")

    # Label the vertical axis.
    axis.set_ylabel("Total abundance")

    # Display the species legend.
    axis.legend()

    # Add a light grid to the panel.
    axis.grid(True, alpha=0.3)

# Add one title above both panels.
fig.suptitle("Changes in Fish Abundance Over Time")

# Adjust spacing between the title and panels.
fig.tight_layout()

# Create the output image path.
output_file = project_folder / "reef_fish_abundance_over_time.png"

# Save the plot as a high-resolution PNG image.
plt.savefig(output_file, dpi=300)

# Display the plot window.
plt.show()