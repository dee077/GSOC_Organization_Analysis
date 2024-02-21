import pandas as pd

# Replace these with the actual file names
file_names = ['../data/2023.csv', '../data/2022.csv', '../data/2021.csv', '../data/2020.csv', '../data/2019.csv']

# Read data from each file into separate DataFrames
data_frames = [pd.read_csv(file_name, encoding='latin-1') for file_name in file_names]

# Concatenate the DataFrames to get all unique organizations Organization
all_organizations = pd.concat([df['Organization'] for df in data_frames]).unique()

# Read 2024 data
data_2024 = pd.read_csv('../data/2024.csv', encoding='latin-1')

# Filter 2024 data based on organizations not present in previous years
filtered_data_2024 = data_2024[~data_2024['Organization'].isin(all_organizations)]

# Write the filtered data to new_2024.csv
filtered_data_2024.to_csv('../data/new_2024.csv', index=False)

print("Filtered data has been written to new_2024.csv.")
