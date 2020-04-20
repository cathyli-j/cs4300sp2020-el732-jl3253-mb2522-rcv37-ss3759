import json
import sys
file_name = "all_restaurants.json"

with open(file_name) as json_file:
    data = json.load(json_file)
    id_by_city = {}
    id_by_name = {}
    category_by_id = {}
    name_by_id = {}
    names_list = []
    errs = 0
    good = 0
    for d in data:
        try:
            if d['name'].lower() in id_by_name:
                id_by_name[d['name'].lower()].append(d['business_id'])
            else:
                id_by_name[d['name'].lower()] = [d['business_id']]
                names_list.append(d['name'.lower()])

            if d['city'].lower() in id_by_city:
                id_by_city[d['city'].lower()].append(d['business_id'])
            else:
                id_by_city[d['city'].lower()] = [d['business_id']]

            category_by_id[d['business_id']] = d['categories'].lower().split(", ")

            if d['business_id'].lower() in name_by_id:
                name_by_id[d['business_id']].append(d['name'])
            else:
                name_by_id[d['business_id']] = [d['name']]
            good += 1
        except:
            #print("err with %s" % d)
            errs += 1
    with open('all_splits/id_by_name.json', 'w') as outfile:
        json.dump(id_by_name, outfile)
    with open('all_splits/id_by_city.json', 'w') as outfile:
        json.dump(id_by_city, outfile)
    with open('all_splits/cat_by_id.json', 'w') as outfile:
        json.dump(category_by_id, outfile)
    with open('all_splits/name_by_id.json', 'w') as outfile:
        json.dump(name_by_id, outfile)
    with open('all_splits/restaurant_names.json', 'w') as outfile:
        json.dump(names_list, outfile)
    with open('all_splits/restaurant_prefetch.json', 'w') as outfile:
        json.dump(names_list[:500], outfile) #Prefetch restaurant names are a sample of restaurant names loaded on startup
print("errs: %d" % errs)
print("good: %d" % good)
