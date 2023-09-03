import json


def extract_doi(path_to_arxiv, output_path):
    relevant_data = []

    # Open the file and read it line by line
    with open(path_to_arxiv, 'r') as f:
        for line in f:

            # Load the JSON data from the line
            data = json.loads(line)

            # Check if inside the categories exist a category that starts with cs.
            categories = data['categories'].split(' ')
            cs_exist = map(lambda x: x.startswith('cs.'), categories)

            # exclude all doi Null or not in Computer Science field
            if True in cs_exist and not data['doi'] is None:
                relevant_data.append(data['doi'])
            else:
                continue

    relevant_data = list(set(relevant_data))

    print(f"Total DOI extracted for Computer Science: {len(relevant_data)}")

    with open(output_path, 'w') as f:
        json.dump(relevant_data, f)


if __name__ == "__main__":
    arxiv_path = "../../data/doi/raw/arxiv-metadata-oai-snapshot.json"
    output_path = "../../data/doi/transformed/arxiv_doi.json"
    extract_doi(arxiv_path, output_path)
