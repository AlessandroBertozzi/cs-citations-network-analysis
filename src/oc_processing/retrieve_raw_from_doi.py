import gc
import os
import pandas as pd
from tqdm import tqdm
import networkx as nx

def process_cited(directory_path, doi_list, network_level=3, save=True):
    # Dictionary to store results
    path_output = '../../data/OC/test_network/doi/first/'

    # List all files in the directory
    all_files = os.listdir(directory_path)

    # Filter out files that are not CSVs
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

    for level in range(1, network_level):

        dfs = list()

        for csv_file in tqdm(csv_files, desc='Processing csv file: '):
            # Construct the full path to the CSV file
            csv_file_path = os.path.join(directory_path, csv_file)

            # Read the CSV into a Pandas DataFrame
            df = pd.read_csv(csv_file_path, dtype=column_types)

            filtered_df = df[df['cited'].isin(doi_list) | df['citing'].isin(doi_list)]

            # Add the DataFrame to the list
            dfs.append(filtered_df)

        # Merge all DataFrames into a single DataFrame, grouping by 'cited' and summing up the counts
        merged_df = pd.concat(dfs).drop_duplicates().reset_index()

        if save:
            merged_df.to_csv(path_output + f'network_level_{level}.csv', index=False)

        citing = merged_df['citing'].drop_duplicates().tolist()
        cited = merged_df['cited'].drop_duplicates().tolist()

        doi_list = list(set(citing + cited))

        del merged_df, filtered_df, df

        gc.collect()

        print(len(doi_list))

    return doi_list


def build_gephi_csv(csv_file_path, path_output):
    column_types = {
        'oci': str,
        'citing': str,
        'cited': str,
        'creation': str,
        'timespan': str,
        'journal_sc': str,
        'author_sc': str,
    }

    df = pd.read_csv(csv_file_path, dtype=column_types)

    print(len(df))

    df = df[["citing", "cited", "creation", 'timespan']]

    renamed_df = df.rename(columns={"citing": "source", "cited": "target"})

    renamed_df.to_csv(path_output + f'gephi_csv.csv', index=False)

    return renamed_df




if __name__ == '__main__':
    # doi = ['10.1016/j.joi.2016.02.007']
    # all_doi = process_cited('../../data/OC/test_network/first_level_medium', doi)

    df = build_gephi_csv('../../data/OC/test_network/doi/first/network_level_2.csv', '../../data/OC/test_network/graph/')

