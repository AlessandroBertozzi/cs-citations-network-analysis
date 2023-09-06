

# extract doi about computer science

from src.extraction_doi import arxiv
from src.extraction_doi import dblp
from src.extraction_doi import doi_union

# extract all csvs from open citations that have in cited or citing a cs doi

from src.oc_processing import read_filter_raw

# count the internal and external citations received

from src.oc_processing.count_citations import process_cited
from src.oc_processing.count_citations import process_citing
from src.oc_processing.count_citations import merge_citation_dfs

# find the most suitable dois for the analysis

from src.count_processing.best_doi import find_best_doi

# rerun on raw OC data with a new list of dois for collect all citations and references, reaching a max number of
# iterations

from src.oc_processing import filter_for_network

# iterate all over the obtained repos for rebuild the network of the dois

from src.oc_processing.retrieve_raw_from_doi import process_cited

# Choose a level of depth and create a single csv

from src.oc_processing.retrieve_raw_from_doi import build_gephi_csv

# use the csv for generate a graph

# apply the Betweenness centrality for finding the most bottle-necked nodes for the graph

# visualize the graph

# apply metrics


