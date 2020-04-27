import json
import sys
file_name = "3000reviews.json" # TODO: We need to change this to the full scope of reviews we're interested in

with open(file_name) as json_file:
    data = json.load(json_file)
    flat_reviews = {}
    errs = 0
    good = 0
    print("Flattening reviews")
    for r in data['reviews']:
        try:
            if r['business_id'] in flat_reviews:
                flat_reviews[r['business_id']] += ' ' + r['text'].lower()
            else:
                flat_reviews[r['business_id']] = r['text'].lower()
            good += 1
        except:
            #print("err with %s" % r)
            errs += 1
    with open('all_splits/flat_reviews.json', 'w') as outfile:
        json.dump(flat_reviews, outfile)
print("errs: %d" % errs)
print("good: %d" % good)
