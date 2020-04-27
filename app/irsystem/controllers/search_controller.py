from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

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
		output_message = "This is a test " + query_name + " in " + query_city
		city_without_state = query_city.split(', ')[0]
		print(city_without_state)
		data = basicSearch(query_name, city_without_state)
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)


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