import pandas as pd
from src.oc_processing.oc_api import extract_meta


def find_best_doi(count_csv_path, output_path, size_citations='high'):
    df = pd.read_csv(count_csv_path)

    if size_citations == 'medium':
        df = df[
            (df['internal_citations_received'] >= 100) & (df['internal_citations_received'] <= 500) &
            (df['external_citations_received'] >= 100) & (df['external_citations_received'] <= 500)
                ]
    else:
        df = df[(df['internal_citations_received'] >= 1000) & (df['external_citations_received'] >= 1000)]

    # Compute the ratio for each article
    # Added a small value to avoid division by zero
    df['citation_ratio'] = df['internal_citations_received'] / (df['external_citations_received'] + 1e-10)

    # Compute the absolute difference from 1 for each article's ratio
    df['abs_difference_from_1'] = (df['citation_ratio'] - 1).abs()

    # Sort by the absolute difference and get the top articles
    sorted_articles = df.sort_values(by='abs_difference_from_1')

    print(sorted_articles[['doi', 'internal_citations_received', 'external_citations_received', 'citation_ratio']])

    dois = sorted_articles['doi'].tolist()[:100]

    dois_meta = extract_meta(dois, save=True, output_path=output_path + f"best_doi_{size_citations}.json")

    return sorted_articles, dois_meta


if __name__ == '__main__':
    sorted_articles, dois_meta = find_best_doi(count_csv_path="../../data/OC/count/count.csv",
                                               output_path='../../data/OC/')
