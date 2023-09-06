import requests
from tqdm import tqdm
import json


def extract_meta(dois, output_path=None, save=False):
    result = list()
    chunk_size = 10

    for i in tqdm(range(0, len(dois), chunk_size)):
        chunk = dois[i:i + chunk_size]
        r = requests.get(f"https://opencitations.net/index/coci/api/v1/metadata/{'__'.join(chunk)}")
        result += r.json()

    if save:
        with open(output_path, 'w') as f:
            json.dump(result, f)

    return result
