import pandas as pd


df = pd.read_csv("../data/OC/count/count.csv")

print(f"external received: {df['external_citations_received'].max()}")
print(f"external make: {df['external_citations_make'].max()}")
print(f"internal received: {df['internal_citations_received'].max()}")
print(f"internal make: {df['internal_citations_make'].max()}")

# Compute the ratio for each article
df['citation_ratio'] = df['internal_citations_received'] / (df['external_citations_received'] + 1e-10)  # Added a small value to avoid division by zero

# Filter articles with a balanced ratio
# balanced_articles = df[(df['citation_ratio'] >= 0.9) & (df['citation_ratio'] <= 1.0)]

# Compute the absolute difference from 1 for each article's ratio
df['abs_difference_from_1'] = (df['citation_ratio'] - 1).abs()

# Sort by the absolute difference and get the top articles
sorted_articles = df.sort_values(by='abs_difference_from_1').head()


print(sorted_articles[['doi', 'internal_citations_received', 'external_citations_received', 'citation_ratio']])