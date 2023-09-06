import zipfile
import io
import os
import glob
import pandas as pd
import gc
import json
from tqdm import tqdm

f = open('../../data/doi/transformed/cs_doi.json')
list_doi = json.load(f)

# Directory containing ZIP files
zip_directory = '../../data/OC/raw'  # Replace with the directory you are interested in

# Directory to save filtered CSV files
output_directory = '../../data/OC/filtered'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)


# Construct the full path to the directory
zip_dir_path = os.path.join(os.getcwd(), zip_directory)

# Use glob to find all ZIP files in the directory
zip_files = glob.glob(os.path.join(zip_dir_path, "*.zip"))

# Iterate over each ZIP file
for zip_file in tqdm(zip_files, position=0):
    # Open the ZIP file
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        # Get the list of all files in the ZIP archive
        all_files = zip_ref.namelist()

        # Filter out only the CSV files
        csv_files = [f for f in all_files if f.endswith('.csv')]

        column_types = {
            'oci': str,
            'citing': str,
            'cited': str,
            'creation': str,
            'timespan': str,
            'journal_sc': str,
            'author_sc': str,
        }

        # Iterate over each CSV file
        for csv_file in tqdm(csv_files, leave=False,  position=1):
            # tqdm.write(f"Processing {csv_file} in {zip_file}")

            # Open the CSV file
            with zip_ref.open(csv_file) as myfile:
                # Convert bytes to string
                text = io.TextIOWrapper(myfile, encoding="utf8")

                # Read CSV into a Pandas DataFrame
                df = pd.read_csv(text, dtype=column_types)

                filtered_df = df[df['cited'].isin(list_doi) | df['citing'].isin(list_doi)]

                # Save the filtered DataFrame to a new CSV file
                output_csv_path = os.path.join(
                    output_directory,
                    f"filtered_{os.path.basename(csv_file).replace('/', '_').replace(':', '_').replace('?', '_')}"
                )
                filtered_df.to_csv(output_csv_path, index=False)
                # tqdm.write(f"Saved filtered data to {output_csv_path}")

            # Delete the DataFrame to free up memory
            del df

            del filtered_df

            # Explicitly free up memory
            gc.collect()
