import pandas as pd
import os

# Replace these with the actual file names
file_names = ['../data/2023.csv', '../data/2022.csv', '../data/2021.csv', '../data/2020.csv', '../data/2019.csv']

# Create an empty DataFrame to store the filtered data
filtered_data = pd.DataFrame(columns=['Organization', 'Technologies', 'Topics', 'Selected_Students', 'Source_File'])

# Read each CSV file, filter data, and append to the new DataFrame
for file_name in file_names:
    df = pd.read_csv(file_name, encoding='ISO-8859-1')
    
    # Apply filters (topics not containing "machine learning" or "artificial intelligence" and selected students >= 5)
    mask = ~df['Topics'].str.contains('machine learning|artificial intelligence', case=False)
    mask &= (df['Selected_Students'] >= 10)
    
    # Add the Source_File column
    df['Source_File'] = os.path.basename(file_name)
    
    # Append filtered data to the new DataFrame
    filtered_data = pd.concat([filtered_data, df[mask]], ignore_index=True)

# Save the new DataFrame to a CSV file
filtered_data.to_csv('../data/shortlisted.csv', index=False)

# Print the filtered data
print(filtered_data)
