import json
import sys
import nltk
from nltk.tokenize import word_tokenize 
# Used: split -l 130000 ../yelp_academic_dataset_review.json review
from os import listdir
from os.path import isfile, join
review_splits = [("../review_splits/" + f) for f in listdir("../review_splits") if isfile(join("../review_splits", f))]
stop_words = {"i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"}
with open("../all_restaurants.json") as restaurants:
    indexed_restaurants = [b['business_id'] for b in json.load(restaurants)]
print(len(indexed_restaurants))

"""
Returns a string with stop words removed
"""
def remove_stopwords(text):
    review_text = text.lower()
    review_tokens = word_tokenize(review_text) 
    filtered_review_text = ""
    for w in review_tokens: 
        if w not in stop_words: 
            filtered_review_text += ' ' + w
    return filtered_review_text    

print("Flattening and tokenizing reviews")
flat_reviews = {}
errs = 0
good = 0
for file_name in review_splits:
    print("Loading " + file_name)
    with open(file_name) as json_file:
        print("Successfully opened " + file_name)
        for line in json_file:
            r = json.loads(line)
            try:
                if r['business_id'] in indexed_restaurants:
                    if r['business_id'] in flat_reviews:
                        flat_reviews[r['business_id']] += ' ' + remove_stopwords(r['text'])
                    else:
                        flat_reviews[r['business_id']] = remove_stopwords(r['text'])
                    good += 1
                    print(good)
            except:
                # print("err with %s" % r)
                errs += 1
    with open('../all_splits/flat_reviews.json', 'w') as outfile:
        json.dump(flat_reviews, outfile)
print("errs: %d" % errs)
print("good: %d" % good)
