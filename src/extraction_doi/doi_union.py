import json


def union_doi(list_path, output_path):

    result = list()

    for file in list_path:
        with open(file, 'r') as f:
            data = json.load(f)

        result = result + data

    result = list(set(result))
    print(f"DOI from Computer Science: {len(result)}")
    with open(output_path, 'w') as f:
        json.dump(result, f)


if __name__ == '__main__':
    arxiv_path = '../../data/doi/transformed/arxiv_doi.json'
    dblp_path = '../../data/doi/transformed/dblp.json'
    output_path = '../../data/doi/transformed/cs_doi.json'
    union_doi([arxiv_path, dblp_path], output_path)
