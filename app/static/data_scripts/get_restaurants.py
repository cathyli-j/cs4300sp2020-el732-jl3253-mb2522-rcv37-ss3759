import json
import sys
file_name = "../yelp_academic_dataset_business.json"

category_list = ['Restaurants','Food','Sandwiches','Breakfast & Brunch','Chinese','Mexican','American (New)','Japanese','Coffee & Tea','Pizza','Cafes','American (Traditional)','Seafood','Italian','Sushi Bars','Burgers','Salad','Delis','Vietnamese','Noodles','Food Stands','Asian Fusion','Fast Food','Mediterranean','Thai','Food Trucks','Indian','Bakeries','Korean','Latin American','Dim Sum','Desserts','Barbeque','Ramen','Chicken Wings','Juice Bars & Smoothies','French','Soup','Diners','Sports Bars','Specialty Food','Grocery','Tacos','Cantonese','Hot Dogs','Gluten-Free','Halal','Middle Eastern','Tapas/Small Plates','Caterers','Pop-Up Restaurants','Bagels','Vegan','Vegetarian','Filipino','Lounges','Steakhouses','Bubble Tea','Chicken Shop','Creperies','Hot Pot','Comfort Food','Gastropubs','Greek','Salvadoran','Beer Bar','Hawaiian','Peruvian','Poke','Ice Cream & Frozen Yogurt','Street Vendors','Pakistani','Pubs','Donuts','Turkish','Izakaya','Southern','Tapas Bars','Himalayan/Nepalese','Hong Kong Style Cafe','Szechuan','Buffets','Cajun/Creole','Spanish','Brazilian','Cheesesteaks','Breweries','Burmese','Caribbean','German','Soul Food','Taiwanese','Japanese Curry']
with open(file_name) as json_file:
    data = json.load(json_file)
    restaurants = []
    errs = 0
    good = 0

    for d in data: 
        try:
            if len(list(filter(lambda x: x in d['categories'], category_list))) > 0: 
                restaurants.append(d)
                good += 1
        except Exception as e: 
            print(e)
            errs += 1
    with open('all_restaurants.json', 'w') as outfile:
        json.dump(restaurants, outfile)
    print("errs: %d" % errs)
    print("good: %d" % good)
