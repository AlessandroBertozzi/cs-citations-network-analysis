import os
import pandas as pd
import json
from tqdm import tqdm


def process_citing(directory_path, doi_list, save=True):
    # Dictionary to store results
    path_output = '../../data/OC/count/citing/'

    dfs = list()

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

    for csv_file in tqdm(csv_files, desc='Processing csv file: '):
        # Construct the full path to the CSV file
        csv_file_path = os.path.join(directory_path, csv_file)

        # Read the CSV into a Pandas DataFrame
        df = pd.read_csv(csv_file_path, dtype=column_types)

        # Create a boolean mask for internal and external citations
        internal_mask = df['cited'].isin(doi_list)
        external_mask = ~internal_mask

        # Group by 'citing' and sum up the internal and external citations
        internal_counts = df.loc[internal_mask].groupby('citing')['cited'].count()
        external_counts = df.loc[external_mask].groupby('citing')['cited'].count()

        # Combine the counts into a single DataFrame
        counts_df = pd.DataFrame(
            {'internal_citations_make': internal_counts, 'external_citations_make': external_counts}).fillna(
            0).astype(int).reset_index()

        # Add the DataFrame to the list
        dfs.append(counts_df)

    # Merge all DataFrames into a single DataFrame, grouping by 'cited' and summing up the counts
    merged_df = pd.concat(dfs).groupby('citing').agg({
        'internal_citations_make': 'sum',
        'external_citations_make': 'sum'
    }).reset_index()

    # Add a column to indicate if the 'cited' DOI is in the doi_list or not
    merged_df['in_doi_list'] = merged_df['citing'].isin(doi_list)

    if save:
        merged_df.to_csv(path_output + 'count_citing.csv', index=False)

    return merged_df


def process_cited(directory_path, doi_list, save=True):
    dfs = list()

    # Dictionary to store results
    path_output = '../../data/OC/count/cited/'

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

    for csv_file in tqdm(csv_files, desc='Processing csv file: '):
        # Construct the full path to the CSV file
        csv_file_path = os.path.join(directory_path, csv_file)

        # Read the CSV into a Pandas DataFrame
        df = pd.read_csv(csv_file_path, dtype=column_types)

        # Create a boolean mask for internal and external citations
        internal_mask = df['citing'].isin(doi_list)
        external_mask = ~internal_mask

        # Group by 'citing' and sum up the internal and external citations
        internal_counts = df.loc[internal_mask].groupby('cited')['citing'].count()
        external_counts = df.loc[external_mask].groupby('cited')['citing'].count()

        # Combine the counts into a single DataFrame
        counts_df = pd.DataFrame(
            {'internal_citations_received': internal_counts, 'external_citations_received': external_counts}).fillna(
            0).astype(int).reset_index()

        # Add the DataFrame to the list
        dfs.append(counts_df)

    # Merge all DataFrames into a single DataFrame, grouping by 'cited' and summing up the counts
    merged_df = pd.concat(dfs).groupby('cited').agg({
        'internal_citations_received': 'sum',
        'external_citations_received': 'sum'
    }).reset_index()

    # Add a column to indicate if the 'cited' DOI is in the doi_list or not
    merged_df['in_doi_list'] = merged_df['cited'].isin(doi_list)

    if save:
        merged_df.to_csv(path_output + 'count_cited.csv', index=False)

    return merged_df


def merge_citation_dfs(df1, df2, doi_list, key1='cited', key2='citing', save=True):

    # Dictionary to store results
    path_output = '../../data/OC/count/'

    # Merge the two DataFrames on their respective keys
    merged_df = pd.merge(df1, df2, left_on=key1, right_on=key2, how='outer', suffixes=('_received', '_make'))

    # Rename the key columns to a single 'doi' column
    merged_df['doi'] = merged_df[key1].combine_first(merged_df[key2])

    # Drop the original key columns
    merged_df.drop([key1, key2], axis=1, inplace=True)

    # Fill NaN values with 0 and convert counts to integers
    cols_to_fill = ['internal_citations_received', 'external_citations_received', 'internal_citations_make',
                    'external_citations_make']
    merged_df[cols_to_fill] = merged_df[cols_to_fill].fillna(0).astype(int)

    # Handle the 'in_doi_list' column (not included in the final DataFrame as per the new requirements)
    # merged_df['in_doi_list'] = merged_df['in_doi_list_received'].fillna(False) | merged_df['in_doi_list_make'].fillna(False)

    # Drop the intermediate 'in_doi_list' columns (not needed as per the new requirements)
    # merged_df.drop(['in_doi_list_received', 'in_doi_list_make'], axis=1, inplace=True)

    # Reorder the columns
    merged_df = merged_df[
        ['doi', 'internal_citations_received', 'external_citations_received', 'internal_citations_make',
         'external_citations_make']]

    merged_df['in_doi_list'] = merged_df['doi'].isin(doi_list)

    if save:
        merged_df.to_csv(path_output + 'count.csv', index=False)

    return merged_df


if __name__ == '__main__':
    f = open('../../data/doi/transformed/cs_doi.json')
    list_doi = json.load(f)

    # df1 = process_cited('../../data/OC/filtered', list_doi)
    # df2 = process_citing('../../data/OC/filtered', list_doi)
    df1 = pd.read_csv('../../data/OC/count/cited/count_cited.csv')
    df2 = pd.read_csv('../../data/OC/count/citing/count_citing.csv')

    merge_citation_dfs(df1, df2, list_doi)

