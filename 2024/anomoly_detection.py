# Checks Edison feed for points where the count went down instead of up.
# Usually this happens when a batch of votes are removed for auditing.

import os
import pandas as pd
import re

# Folder containing the CSV files
folder_path = '/Election Data Feed'
output_file = 'total_votes_progression.csv'

# Regular expression to extract date and time from the filename
timestamp_pattern = re.compile(r'Edison_(\d{4}-\d{2}-\d{2})_(\d{2}-\d{2})')

# Dictionary to store 'total_votes' columns with unique names for each timestamp
total_votes_data = {}

# DataFrame to store label columns (first three columns by position)
labels_df = None

# Iterate through each file in the folder
for filename in sorted(os.listdir(folder_path)):
    if filename.startswith("Edison") and filename.endswith('.csv'):
        # Extract the timestamp from the filename
        match = timestamp_pattern.search(filename)
        if match:
            date_str, time_str = match.groups()
            timestamp = f"{date_str} {time_str.replace('-', ':')}"
            
            # Load the CSV file
            file_path = os.path.join(folder_path, filename)
            
            try:
                # Attempt to read the file
                df = pd.read_csv(file_path)
                
                # Check if the 'total_votes' column exists in the file
                if 'total_votes' in df.columns:
                    # If it's the first file, save the first three columns by position as labels
                    if labels_df is None:
                        labels_df = df.iloc[:, :3].copy()  # Select first three columns by position
                    
                    # Add the 'total_votes' column to total_votes_data with the timestamp in the name
                    total_votes_data[f'total_{timestamp}'] = df['total_votes'].values
                
            except pd.errors.EmptyDataError:
                print(f"Skipping file with no data or columns: {filename}")
                continue

# Create a DataFrame from total_votes_data dictionary
progression_df = pd.DataFrame(total_votes_data)

# Concatenate labels with the total_votes progression data
final_df = pd.concat([labels_df, progression_df], axis=1)

# Check for progression in each row, and log details for any decreases
progression_check = []
for _, row in progression_df.iterrows():
    issues = []
    for idx, (x, y) in enumerate(zip(row[:-1], row[1:]), start=1):
        if y < x:  # Flag only true decreases
            issues.append(f"{final_df.columns[idx]} dropped from {x} to {y}")
    
    # Determine progression status and add details if there are issues
    if issues:
        progression_check.append("False Progression: " + "; ".join(issues))
    else:
        progression_check.append("True Progression")

# Add progression check as the last column
final_df['Progression_Check'] = progression_check

# Save the resulting DataFrame to CSV
final_df.to_csv(output_file, index=False)

print(f"Total votes progression data saved to {output_file}")
