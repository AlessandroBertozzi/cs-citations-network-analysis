import unittest
import pandas as pd
from pandas.testing import assert_frame_equal
import os
from src.oc_processing.citations import process_citing, process_cited, merge_citation_dfs


class TestCSVProcessing(unittest.TestCase):

    def setUp(self):
        # Create sample DOI lists and CSV files
        self.doi_list = ['doi1', 'doi2', 'doi3']
        self.data1 = {'citing': ['doi1', 'doi2', 'doi3'], 'cited': ['doi4', 'doi3', 'doi1']}
        self.data2 = {'citing': ['doi4', 'doi3', 'doi2'], 'cited': ['doi1', 'doi2', 'doi4']}
        self.df1 = pd.DataFrame(self.data1)
        self.df2 = pd.DataFrame(self.data2)
        self.test_dir = 'test_csvs'
        os.makedirs(self.test_dir, exist_ok=True)
        self.df1.to_csv(os.path.join(self.test_dir, 'file1.csv'), index=False)
        self.df2.to_csv(os.path.join(self.test_dir, 'file2.csv'), index=False)

    def test_process_csv_files_merged_received(self):
        expected_df = pd.DataFrame({
            'cited': ['doi1', 'doi2', 'doi3', 'doi4'],
            'internal_citations_received': [1, 1, 1, 2],
            'external_citations_received': [1, 0, 0, 0]
        })
        expected_df['in_doi_list'] = expected_df['cited'].isin(self.doi_list)
        result_df = process_cited(self.test_dir, self.doi_list, save=False)
        expected_df['internal_citations_received'] = expected_df['internal_citations_received'].astype('int32')
        expected_df['external_citations_received'] = expected_df['external_citations_received'].astype('int32')
        assert_frame_equal(expected_df, result_df)

    def test_process_csv_files_merged_make(self):
        expected_df = pd.DataFrame({
            'citing': ['doi1', 'doi2', 'doi3', 'doi4'],
            'internal_citations_make': [0, 1, 2, 1],
            'external_citations_make': [1, 1, 0, 0],
        })
        expected_df['in_doi_list'] = expected_df['citing'].isin(self.doi_list)
        expected_df['internal_citations_make'] = expected_df['internal_citations_make'].astype('int32')
        expected_df['external_citations_make'] = expected_df['external_citations_make'].astype('int32')
        result_df = process_citing(self.test_dir, self.doi_list, save=False)
        assert_frame_equal(expected_df, result_df)

    def test_merge_two_dfs_updated(self):

        expected_df = pd.DataFrame({
            'doi': ['doi1', 'doi2', 'doi3', 'doi4'],
            'internal_citations_received': [1, 1, 1, 2],
            'external_citations_received': [1, 0, 0, 0],
            'internal_citations_make': [0, 1, 2, 1],
            'external_citations_make': [1, 1, 0, 0]
        })
        expected_df['internal_citations_received'] = expected_df['internal_citations_received'].astype('int32')
        expected_df['external_citations_received'] = expected_df['external_citations_received'].astype('int32')
        expected_df['internal_citations_make'] = expected_df['internal_citations_make'].astype('int32')
        expected_df['external_citations_make'] = expected_df['external_citations_make'].astype('int32')

        df_received = process_cited(self.test_dir, self.doi_list, save=False)
        df_make = process_citing(self.test_dir, self.doi_list, save=False)
        merged_df = merge_citation_dfs(df_received, df_make)
        assert_frame_equal(expected_df, merged_df)


if __name__ == '__main__':
    unittest.main()
