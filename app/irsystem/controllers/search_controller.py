from . import *  
from app.irsystem.controllers import get_preview
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
import traceback


project_name = "Tastes Like Home"
net_id = "Emanuele Lusso: el732, Cathy Li: jl3253, Matias Blake: mb2522, Robert Villaluz: rcv37, Saaqeb Siddiqi: ss3759"

with open('app/static/all_splits/id_by_name.json') as json_file:
		id_by_name = json.load(json_file)
with open('app/static/all_splits/cat_by_id.json') as json_file:
		cat_by_id = json.load(json_file)
with open('app/static/all_splits/id_by_city.json') as json_file:
		id_by_city = json.load(json_file)
with open('app/static/all_splits/city_by_id.json') as json_file:
		city_by_id = json.load(json_file)
with open('app/static/all_splits/name_by_id.json') as json_file:
		name_by_id = json.load(json_file)
with open('app/static/all_splits/city_reviews_full.json') as json_file:
		reviews_by_city = json.load(json_file)
with open('app/static/all_splits/address_by_id.json') as json_file:
	address_by_id = json.load(json_file)

# PRINTING ###################################################################################################### PRINTING ############################################################################

# master print signal
print_on = False 

# for printing/viewing ease
ee = '\n\n\n\n\n\n\n\nPRINT\n\n\n\n\n\n\n\n'
def efun(s): print(ee); print(s); print(ee)

# print first elt of dict, key if ***e*** is "k" or value if "v"
def print_first_element(s,d,e):
	ii = 0
	for elt in d:
		print((s,elt[:100])) if e == "k" else print((s,d[elt][:100]))
		ii+=1
		if ii:
			break
	return elt

# SEARCH ######################################################################################################### SEARCH ############################################################################

@irsystem.route('', methods=['GET'])
def search():
	query_name = request.args.get('search_restaurant')
	query_city = request.args.get('search_city')

	# have to figure out a way to get these from user input to list format
	ad_hoc_words = ['service', 'good service','delicious','food']

	try:
		if not query_name or not query_city:
			data = [] # Since data is blank, search.html doesn't render any message/data
			output_message = ''
		else:
			output_message = "Restaurants most similar to " + query_name + " in " + query_city
			city_without_state = query_city.split(', ')[0].lower()
			#rawdata = basicSearch(query_name, city_without_state, 5)
			# TODO: until this is ready, leaving it as a background task, use print()
			#while the local app is running to see its output in the console
			rawdata = fullSearch(query_name, city_without_state, 5, ahw = ad_hoc_words) 
			#Transform the data to the output format with return_results()
			data = return_results(rawdata)
	except Exception: 
		print('an error occurred')
		print(traceback.format_exc())
		return render_template('fail.html')
	else: 
		return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)

# END SEARCH ################################################################################################## END SEARCH ############################################################################

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

# FULL_SEARCH ###############################################################################################  FULL_SEARCH ############################################################################

"""
Returns top n restaurants in the query city ranked by number of matching categories
and cosine similarities between reviews.
"""
def fullSearch(name, city, n, ahw):
	n_feats = 5000
	query_id = id_by_name[name.lower()][0]
	tfidf_vec = create_vectorizer(n_feats, "english")
	# flat_reviews will contain the flattened reviews for all restaurants in a city
	##### Need to append query restaurant's reviews to the end of city reviews when the reviews data is done
	
	# flatten the reviews of city ***city***
	flat_reviews = reviews_by_city[city]

	if print_on: efun(type(flat_reviews)); print_first_element("flat_reviews",flat_reviews,"k")


	#City needs to be hard-coded for now until we migrate to database/split the reviews another way 
	query_restaurant_city = city_by_id[query_id].lower()
	query_reviews = reviews_by_city[query_restaurant_city][query_id] #Freska Mediterranean Grill in Champaign

	#These next few lines handle if the query restaurant is in the target city. We can't support that case right now
	#so we can't use examples that are from the same city
	#Removing the query restaurant and appending it later is necessary so the restaurant is in the last index in 
	#the Similarity Matrix. This allows us to keep track of it during the comparisons

	#query_reviews = flat_reviews[query_id]
	#if query_id in flat_reviews: 
	#	del flat_reviews[query_id]

	flat_reviews[query_id] = query_reviews
	doc_by_vocab = tfidf_vec.fit_transform([flat_reviews[b_id] for b_id in flat_reviews]).toarray()

	if print_on: efun((doc_by_vocab.shape,len(doc_by_vocab))); print_first_element("dbvocab",doc_by_vocab,"k")

	#restaurant_id_to_index = TEST_generate_restaurant_id_to_index() #Use this as opposed to the next line until we have reviews split by city
	restaurant_id_to_index = generate_restaurant_id_to_index(city.lower())

	# Appends the query restaurant to the city
	n_restaurants = len(restaurant_id_to_index)
	restaurant_id_to_index[query_id] = n_restaurants
	# Create the index->id dictionary for the inverse lookup
	restaurant_index_to_id = {v:k for k,v in restaurant_id_to_index.items()} 
	
	sim_list = get_sim_list(n_restaurants, doc_by_vocab, restaurant_id_to_index, get_cosine_sim)
	#Add restaurant IDs to their sim list
	sim_list = [(restaurant_index_to_id[i], data) for i,data in enumerate(sim_list)] 

	sorted_sim_list = sorted(sim_list, key=lambda x: -x[1]['score']) 
	sorted_sim_list_inverse = {k:v for (k,v) in sorted_sim_list}

	# number of top restaurants to extract with Jaccard similarity
	initial_num = 10
	#Asks for top ***initial_num*** by categories, then filters it down to top 5 by weighing with cosine sim
	top_by_cat = basicSearch(name,city,initial_num)

	#Adjust the scores of top results returned by basic search to account for cosine sim
	#The "similarities" field in the data is just the common categories for now. I have not implemented a way to find similar words
	# in cosine sim
	avg = 0
	for (id, data) in top_by_cat.items():
		efun(('id data',id,data))
		if print_on: efun(('data[score]',data['score'])); efun(('simlist_inverse[id][score]',sorted_sim_list_inverse[id]['score'])); efun(('product',data['score']*sorted_sim_list_inverse[id]['score']))
		product = data['score']*sorted_sim_list_inverse[id]['score']
		top_by_cat[id]['score'] = product
		avg += product
	
	avg /= initial_num
	# tune similarity score if there are user keywords
	if ahw:
		for (id,data) in top_by_cat.items():
			keywords_in_reviews = 0
			review = flat_reviews[id]
			for word in ahw:
				if word in review: keywords_in_reviews += 1

			# if any of the input keywords are mentioned in the restaurant's reviews
			if keywords_in_reviews:
				# tune similarity score according to ad hoc input correlation
				# tuning: score += (avg/(|score-avg|+3/4))*(k_i_r^(1/(k_i_w+1)**1/2))
				L = avg/((abs(top_by_cat[id]['score'] - avg)) + 0.75)
				R =  keywords_in_reviews ** (1/((keywords_in_reviews + 1) ** 0.5))
				top_by_cat[id]['score'] += L*R

	# sort top n results by score and return them
	top_n = dict(sorted(top_by_cat.items(), key=lambda x: -x[1]['score'])[:n])
	return top_n

# END FULL_SEARCH ############################################################################################ END FULL_SEARCH ############################################################################


"""
TEMPORARY FUNCTION 

Because we don't have the reviews split by city yet, we use this function to get the IDs in the 
sample flat_reviews dataset (this sample dataset contains the first 3000 reviews, which are not necessarily
from restaurants)
"""
def TEST_generate_restaurant_id_to_index():
	data = reviews_by_city.keys()
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
Returns a similarity list generated using the method input_get_sim_method (Cosine Sim, etc)

Each element in the list has the following format:
{{'score': int , 'similarities': [ ] }}

Similarities represents which words were the most similar between the restaurants compared. 
It is just an empty list for now because this has not been implemented. 

"""
def get_sim_list(n_restaurants, input_doc_mat, restaurant_id_to_index, input_get_sim_method): 
	arr = [dict() for x in range(n_restaurants)]
	for i in range(0, n_restaurants-1): # Index n_restaurants-1 will always be the query restaurant
		val = input_get_sim_method(0, i, input_doc_mat, restaurant_id_to_index)
		arr[i] = {'score': val, 'similarities': []}
	arr[n_restaurants-1] = {'score': -1, 'similarities': []}
	return arr 

"""
Returns the top results in the appropraite format. 

Input format: 
{
	id: restaurant id
	{
		'score': final similarity score
		'similarities': similar keywords, categories, etc

	}      
}

Return format:
{
	'name': restaurant name, 
	'address': restaurant address,
	'score': final similarity score,
	'metrics': similar keywords, categories, etc
}
"""
def return_results(top):
	#top = dict(list(top)[0:5]) #Truncate to only 5 results
	data = {}
	i = 0
	for (id, info) in top.items():
		if id in name_by_id: 
			data[id] = {'name': name_by_id[id][0], 'address':address_by_id[id], 'score':info['score'], 'similarities': info['similarities']}
	return data

# BASIC_SEARCH ################################################################################################ BASIC_SEARCH ############################################################################

"""
Returns top n restaurants in the query city ranked by the number of categories matching 
the categories of the query restaurant.

Each result has the following format: 
{id: {'score': int , 'similarities': [ ] }}

Where score is the Jaccard similarity and categories is the list of categories that the restaurants have in common. 
"""
def basicSearch(name, city, n): 
	query_id = id_by_name[name.lower()][0]
	query_categories = cat_by_id[query_id]
	target_city_ids = id_by_city[city.lower()]
	target_city_restaurants = {}
	target_city_restaurants_scores = {} 

	for id in target_city_ids:
		target_city_restaurants[id] = cat_by_id[id]
	
	for (id, categories) in target_city_restaurants.items():
		if not print_on: efun(('most possible categories',len(set(categories).union(query_categories))))
		common_categories = set((categories)).intersection(query_categories)
		target_city_restaurants_scores[id] = {'score': len(common_categories), 'similarities': common_categories}

	target_city_restaurants_scores = sorted(target_city_restaurants_scores.items(), key=lambda x:x[1]['score'], reverse=True)
	top_n = dict(list(target_city_restaurants_scores)[0:n]) 
	return top_n

# END BASIC_SEARCH ############################################################################################ END BASIC_SEARCH ############################################################################

@irsystem.route('/get_img', methods=['GET'])
def get_img_src():
	bid = request.args.get('bid')
	return get_preview.get_img_src(bid)