import json
import pandas as pd
import datetime

with open('../../data/OC/best_doi.json', 'r') as f:
    data = json.load(f)

list_count = list()
for i in data:
    list_count.append(int(i['citation_count']))

print(min(list_count))


# df = pd.DataFrame.from_records(data)
#
# print(df.columns)
# df['year'] = pd.to_datetime(df['year'], format='%Y', errors='coerce')
#
# # s_datetime = datetime.datetime.strptime('2009', '%Y')
# #
# # df = df[(df['year'] >= s_datetime)]
#
# titles = df['title'].to_list()
#
#
#
# # Defining a dictionary of academic fields with their associated keywords
#
# academic_fields = {
#     "Information Theory": ["information", "communication", "secrecy", "entropy"],
#     "Social Networks": ["social network", "link-prediction"],
#     "Mathematics": ["mathematical", "markov", "calculus", "geometry", "graph theory", "combinatorial"],
#     "Computer Science": ["algorithm", "computing", "simulation", "cloudsim", "computational", "data structure"],
#     "Cryptography": ["cryptosystem", "encryption", "signature", "cipher", "public key", "private key"],
#     "Machine Learning": ["learning", "optimization", "recognition", "neural", "deep", "boosting", "ensemble", "bootstrap", "regression", "classification", "machine translation", "neural network"],
#     "Medical Imaging": ["anatomical", "mri", "image segmentation", "biomedical"],
#     "Computer Vision": ["visualizing", "convolutional", "real-time style", "super-resolution", "coco", "visual", "KITTI", "image", "vision"],
#     "Robotics": ["robotics", "robot"],
#     "Operations Research": ["auction", "routing", "scheduling", "vehicle routing"],
#     "Information Systems": ["information system", "technology usage", "technology acceptance", "IT innovation"],
#     "Natural Language Processing": ["word vectors", "phrase representations", "natural language", "sentence", "word representation", "language processing"],
#     "Data Science": ["data", "statistics", "statistical", "density estimation"],
#     "Others": []
# }
#
# # Matching each title to the most relevant academic field
# title_to_field = {}
#
# for title in titles:
#     matched = False
#     for field, keywords in academic_fields.items():
#         if any(keyword.lower() in title.lower() for keyword in keywords):
#             title_to_field[title] = field
#             matched = True
#             break
#     if not matched:
#         title_to_field[title] = "Others"
#
# with open('title_to_field.json', 'w') as f:
#     json.dump(title_to_field, f)

