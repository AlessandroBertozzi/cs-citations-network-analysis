import glob
import pandas as pd
import gc
import json
import zipfile
import io
import os
from tqdm import tqdm
import os


def read_and_filter(list_doi, zip_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Construct the full path to the directory
    zip_dir_path = os.path.join(os.getcwd(), zip_directory)

    # Use glob to find all ZIP files in the directory
    zip_files = glob.glob(os.path.join(zip_dir_path, "*.zip"))

    dfs = list()
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
            for csv_file in tqdm(csv_files, leave=False, position=1):
                # Open the CSV file
                with zip_ref.open(csv_file) as myfile:
                    # Convert bytes to string
                    text = io.TextIOWrapper(myfile, encoding="utf8")

                    # Read CSV into a Pandas DataFrame
                    df = pd.read_csv(text, dtype=column_types)

                    filtered_df = df[df['cited'].isin(list_doi) | df['citing'].isin(list_doi)]

                    # Add the DataFrame to the list
                    dfs.append(filtered_df)

                    # Save the filtered DataFrame to a new CSV file
                    output_csv_path = os.path.join(
                        output_directory,
                        f"filtered_{os.path.basename(csv_file).replace('/', '_').replace(':', '_').replace('?', '_')}"
                    )
                    filtered_df.to_csv(output_csv_path, index=False)

                    # Delete the DataFrame to free up memory
                    del df, filtered_df

                    # Explicitly free up memory
                    gc.collect()

            merged_df = pd.concat(dfs).drop_duplicates().reset_index()
            citing = merged_df['citing'].drop_duplicates().tolist()
            cited = merged_df['cited'].drop_duplicates().tolist()

            doi_list = list(set(citing + cited))

    return doi_list


def extract_dois(list_meta):
    result = list()

    for item in tqdm(list_meta):
        citation = [citation.strip() for citation in item['citation'].split(';') if citation != '']
        reference = [reference.strip() for reference in item['reference'].split(';') if reference != '']
        result += citation + reference

    result = list(set(result))
    return result


if __name__ == '__main__':

    citations_size = 'high'

    with open(f'../../data/OC/best_doi_{citations_size}.json') as f:
        data = json.load(f)

    list_doi = extract_dois(data)

    print(len(list_doi))

    # Directory containing ZIP files
    zip_directory = '../../data/OC/raw'

    for depth_level in ['first', 'second', 'third', 'fourth']:
        # Directory to save filtered CSV files
        output_directory = f'../../data/OC/test_network/network_raw/{citations_size}/{depth_level}_level_{citations_size}'

        list_doi = read_and_filter(list_doi, zip_directory=zip_directory, output_directory=output_directory)

        print(len(list_doi))
