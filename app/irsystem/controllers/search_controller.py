from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from sklearn.feature_extraction.text import TfidfVectorizer

project_name = "Better Yelp Recommendations"
net_id = "Emanuele Lusso: el732, Cathy Li: jl3253, Matias Blake: mb2522, Robert Villaluz: rcv37, Saaqeb Siddiqi: ss3759"

@irsystem.route('', methods=['GET'])
def search():
	query_name = request.args.get('search_restaurant')
	query_city = request.args.get('search_city')

	if not query_name or not query_city:
		data = [] # Since data is blank, search.html doesn't render any message/data
		output_message = ''
	else:
		output_message = "Restaurants most similar to " + query_name + " in " + query_city
		city_without_state = query_city.split(', ')[0]
		data = basicSearch(query_name, city_without_state)
		fullSearch(query_name, city_without_state) #TODO: until this is ready, leaving it as a background task, use print() while the local app is running to see its output in the console
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)

"""
CITATION: Assignment 5
Returns a TfidfVectorizer object with the below preprocessing properties.

Note: This function may log a deprecation warning. This is normal, and you
can simply ignore it.

Params: {max_features: Integer,
					max_df: Float,
					min_df: Float,
					norm: String,
					stop_words: String}
Returns: TfidfVectorizer
"""
def create_vectorizer(max_features, stop_words, max_df=0.8, min_df=10, norm='l2'):
	return TfidfVectorizer(min_df=min_df,max_df=max_df,max_features=max_features,stop_words=stop_words,norm=norm)

"""
Returns top 5 restaurants in the query city ranked by number of matching categories
and cosine similarities between reviews.
"""
def fullSearch(name, city):
	n_feats = 5000

	with open('app/static/all_splits/flat_reviews.json') as json_file:
		flat_reviews = json.load(json_file)

	tfidf_vec = create_vectorizer(n_feats, "english")
	doc_by_vocab = tfidf_vec.fit_transform([flat_reviews[b_id] for b_id in flat_reviews]).toarray()		
	print(doc_by_vocab)


"""
Returns top 5 restaurants in the query city ranked by the number of categories matching 
the categories of the query restaurant
"""
def basicSearch(name, city): 
	with open('app/static/all_splits/id_by_name.json') as json_file:
		id_by_name = json.load(json_file)
	with open('app/static/all_splits/cat_by_id.json') as json_file:
		cat_by_id = json.load(json_file)
	with open('app/static/all_splits/id_by_city.json') as json_file:
		id_by_city = json.load(json_file)
	with open('app/static/all_splits/name_by_id.json') as json_file:
		name_by_id = json.load(json_file)

	query_id = id_by_name[name.lower()][0]
	query_categories = cat_by_id[query_id]
	target_city_ids = id_by_city[city.lower()]
	target_city_restaurants = {}
	target_city_restaurants_scores = {} 

	for id in target_city_ids:
		target_city_restaurants[id] = cat_by_id[id]
	
	for (id, categories) in target_city_restaurants.items():
		target_city_restaurants_scores[id] = len(set(categories).intersection(query_categories))

	target_city_restaurants_scores = sorted(target_city_restaurants_scores.items(), key=lambda x:x[1], reverse=True)
	top_5 = dict(list(target_city_restaurants_scores)[0:5]) 
	data = {}
	for (id, score) in top_5.items():
		data[name_by_id[id][0]] = score
	print(data)
	return data