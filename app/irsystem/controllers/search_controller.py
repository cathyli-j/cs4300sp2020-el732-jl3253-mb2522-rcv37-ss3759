from . import *  
from app.irsystem.controllers import get_preview
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from sklearn.feature_extraction.text import TfidfVectorizer

project_name = "Better Yelp Recommendations"
net_id = "Emanuele Lusso: el732, Cathy Li: jl3253, Matias Blake: mb2522, Robert Villaluz: rcv37, Saaqeb Siddiqi: ss3759"

with open('app/static/all_splits/id_by_name.json') as json_file:
		id_by_name = json.load(json_file)
with open('app/static/all_splits/cat_by_id.json') as json_file:
		cat_by_id = json.load(json_file)
with open('app/static/all_splits/id_by_city.json') as json_file:
		id_by_city = json.load(json_file)
with open('app/static/all_splits/name_by_id.json') as json_file:
		name_by_id = json.load(json_file)
with open('app/static/all_splits/flat_reviews.json') as json_file:
		flat_reviews = json.load(json_file)
with open('app/static/all_splits/city_reviews_4.json') as json_file:
		city_reviews = json.load(json_file)

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
		#data = basicSearch(query_name, city_without_state)
		data = fullSearch(query_name, city_without_state) #TODO: until this is ready, leaving it as a background task, use print() while the local app is running to see its output in the console
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
Returns top restaurants in the query city ranked by number of matching categories
and cosine similarities between reviews.
"""
def fullSearch(name, city):
	n_feats = 5000
	query_id = id_by_name[name.lower()][0]
	tfidf_vec = create_vectorizer(n_feats, "english")
	# flat_reviews will contain the flattened reviews for all restaurants in a city
	##### Need to append query restaurant's reviews to the end of city reviews when the reviews data is done

	flat_reviews = city_reviews[city.lower()]

	#City needs to be hard-coded for now until we migrate to database/split the reviews another way 
	query_reviews = city_reviews['middleton'][query_id] #Freska Mediterranean Grill in Champaign

	#These next few lines handle if the query restaurant is in the target city. We can't support that case right now so we can't use examples that are from the same city
	#query_reviews = flat_reviews[query_id]
	#if query_id in flat_reviews: 
	#	del flat_reviews[query_id]

	flat_reviews[query_id] = query_reviews
	doc_by_vocab = tfidf_vec.fit_transform([flat_reviews[b_id] for b_id in flat_reviews]).toarray()

	#Restaurants that are in the flat_reviews dataset: Sake Rok, Nadège Patisserie

	#restaurant_id_to_index = TEST_generate_restaurant_id_to_index() #Use this as opposed to the next line until we have reviews split by city
	restaurant_id_to_index = generate_restaurant_id_to_index(city.lower())

	restaurant_id_to_index[query_id] = len(restaurant_id_to_index) # Appends the query restaurant to the city
	restaurant_index_to_id = {v:k for k,v in restaurant_id_to_index.items()}
	n_restaurants = len(restaurant_id_to_index)
	sim_list = get_sim_list(n_restaurants, doc_by_vocab, restaurant_id_to_index, get_cosine_sim)

	sim_list = [(restaurant_index_to_id[i], s) for i,s in enumerate(sim_list)]

	sorted_sim_list = sorted(sim_list, key=lambda x: -x[1])
	sorted_sim_list_inverse = {k:v for (k,v) in sorted_sim_list}

	top_by_cat = basicSearch(name,city) # Asks for top 10 by categories, then filters it down to top 5 by weighing with cosine sim

	#Adjust top results returned by basic search to account for cosine sim
	for (id, score) in top_by_cat.items():
		top_by_cat[id] = score*sorted_sim_list_inverse[id]
	
	print(top_by_cat)
	new_sort_top = sorted(top_by_cat.items(), key=lambda x: -x[1])
		
	top_10 = dict(list(new_sort_top)[0:5])

	data = return_results(top_10)
	print(data) 
	return data


"""
Because we don't have the reviews split by city yet, we use this function to get the IDs in the 
sample flat_reviews dataset
"""
def TEST_generate_restaurant_id_to_index():
	data = flat_reviews.keys()
	restaurant_id_to_index = {restaurant_id:index for index, restaurant_id in enumerate([d for d in data])}
	return restaurant_id_to_index


"""
Assigns an index for each restaurant id in the target city to help access the data in the numpy arrays
"""
def generate_restaurant_id_to_index(city):
	with open('app/static/all_splits/id_by_city.json') as json_file:
		id_by_city = json.load(json_file)
	data = id_by_city[city]
	restaurant_id_to_index = {restaurant_id:index for index, restaurant_id in enumerate([d for d in data])}
	return restaurant_id_to_index


"""
Generates the cosine similarity between the reviews of two restaurants
"""
def get_cosine_sim(idx1, idx2, input_doc_mat, restaurant_id_to_index):
	vec1 = input_doc_mat[idx1]
	vec2 = input_doc_mat[idx2]
	return vec1.dot(vec2)/(np.linalg.norm(vec1) * np.linalg.norm(vec2)) 


"""
Returns a similarity list 
"""
def get_sim_list(n_restaurants, input_doc_mat, restaurant_id_to_index, input_get_sim_method): 
	arr = np.zeros(n_restaurants)
	for i in range(0, n_restaurants-1): # Index n_restaurants-1 will always be the query restaurant
		val = input_get_sim_method(0, i, input_doc_mat, restaurant_id_to_index)
		arr[i] = val
	return arr 

""" 
Displays top results from IDs
"""
def return_results(top):
	data = {}
	for (id, score) in top.items():
		if id in name_by_id: 
			data[name_by_id[id][0]] = score
	return data


"""
Returns top 10 restaurants in the query city ranked by the number of categories matching 
the categories of the query restaurant
"""
def basicSearch(name, city): 
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
	top_10 = dict(list(target_city_restaurants_scores)[0:10]) 
	return top_10
