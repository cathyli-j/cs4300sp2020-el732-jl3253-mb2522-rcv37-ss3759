import json
import sys
file_name = "../all_restaurants.json"

with open(file_name) as json_file:
    data = json.load(json_file)
    cities = {}
    names = {}
    categories = {}
    ids = {}
    errs = 0
    good = 0
    for d in data:
        try:
            if d['name'].lower() in names:
                names[d['name'].lower()].append(d['business_id'])
            else:
                names[d['name'].lower()] = [d['business_id']]

            if d['city'].lower() in cities:
                cities[d['city'].lower()].append(d['business_id'])
            else:
                cities[d['city'].lower()] = [d['business_id']]

            categories[d['business_id']] = d['categories'].lower().split(", ")

            if d['business_id'].lower() in ids:
                ids[d['business_id']].append(d['name'])
            else:
                ids[d['business_id']] = [d['name']]
            good += 1
        except:
            #print("err with %s" % d)
            errs += 1
    with open('all_splits/id_by_name.json', 'w') as outfile:
        json.dump(names, outfile)
    with open('all_splits/id_by_city.json', 'w') as outfile:
        json.dump(cities, outfile)
    with open('all_splits/cat_by_id.json', 'w') as outfile:
        json.dump(categories, outfile)
    with open('all_splits/name_by_id.json', 'w') as outfile:
        json.dump(ids, outfile)
print("errs: %d" % errs)
print("good: %d" % good)
