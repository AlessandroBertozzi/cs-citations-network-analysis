from lxml import etree
from tqdm import tqdm
import json


def load_from_dblp(xml_path):
    elements = []

    # Create a context iterator that will yield elements as they become available
    context = etree.iterparse(xml_path, events=("end",), tag="ee", load_dtd=True, dtd_validation=True,
                              attribute_defaults=True)
    # Iterate through the elements
    for event, elem in tqdm(context):
        elements.append(elem.text)
        elem.clear()  # Free up memory by clearing the element after use

    return elements


def clean_doi_dblp(list_doi, output_path):
    cleaned_doi = list()

    for doi in tqdm(list_doi):
        if 'https://doi.org/' in doi or 'http://doi.org/' in doi:
            cleaned_doi.append(doi.replace('https://doi.org/', '').replace('http://doi.org/', ''))

    cleaned_doi = list(set(cleaned_doi))

    print(f"DOI from dblp: {len(cleaned_doi)}")

    with open(output_path, 'w') as f:
        json.dump(cleaned_doi, f)


if __name__ == '__main__':
    dblp_path = '../../data/doi/raw/dblp.xml'
    output_path = "../../data/doi/transformed/dblp.json"
    clean_doi_dblp(load_from_dblp(dblp_path), output_path)
