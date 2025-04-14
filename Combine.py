import glob
import pandas as pd

# Define the path to your CSV files
path = "CSV-Files"  # Folder where all CSV files are located
csv_files = glob.glob(path + "/*.csv")

# Create an empty list to hold data from each CSV file
dataframes = []

# Loop through the list of CSV files and read them into a DataFrame
for file in csv_files:
    df = pd.read_csv(file)
    dataframes.append(df)

# Concatenate all DataFrames into one
final_df = pd.concat(dataframes, ignore_index=True)

# Remove duplicate rows.
final_df.drop_duplicates(inplace=True)

# Write the combined DataFrame into a new CSV file named 'Final.csv'
final_df.to_csv("Final.csv", index=False)
