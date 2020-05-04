import json
from sklearn.feature_extraction.text import TfidfVectorizer
import traceback
import numpy as np


with open('../all_splits/city_reviews_full.json') as json_file:
	reviews_by_city = json.load(json_file)
with open('../all_splits/id_by_city.json') as json_file:
	id_by_city = json.load(json_file)

ee = '\n\n\n\n\n\n\n\nPRINT\n\n\n\n\n\n\n\n'
def efun(s): print(ee); print(s); print(ee)

cities = ["Champaign, IL", "Charlotte, NC", "Phoenix, AZ", "Cleveland, OH", "Scottsdale, AZ", "Madison, WI", "Mentor, OH", "Pittsburgh, PA", "Concord, NC", "Concord, ON", "Charlotte, SC", "Concord, OH", "Cleveland, FL", "Charlotte, TX", "Phoenix, TX"]

for city in cities:
    city = city.split(', ')[0].lower()
    for (id,_) in reviews_by_city[city].items():
        if id not in id_by_city[city]:
            print((city, id))

print("---------------------------------------")

for city in cities:
    city = city.split(', ')[0].lower()
    for id in id_by_city[city]:
        if id not in reviews_by_city[city]:
            print((city, id))