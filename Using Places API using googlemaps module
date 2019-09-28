#importing needed libraries
import pandas as pd
import json
import googlemaps as gmaps

"""
A. Use the [*Nearby Seach*](https://developers.google.com/places/web-service/search) Method to find all the restaurant near to the UPY (20.988459, -89.736768) around 2km. In order to fulfill this item you need to:
* Create a *search_nearby_places* function with the appropiate parameters. It must return a JSON with the results. Places must be ranked by distance.
* Create a table with the following columns: Name, Place Id, Rating, Place Types, Total of User Ratings.
"""
#global variable declaration but in this case you do not need it, only saving the gmaps.client in a variables is requiered
kep_api = "*****"

#declaration of our client id to be able to access to API Places
api = gmaps.Client(key =key_api)

#Variable declaration, where the first one are the coordinates of the location, and the second one the radius
lat_lon_G = (20.988459, -89.736768)
"""
using functions from the googlemaps module and specifying in the arguments, where location you give it the coordinates
rank_by you have two options distance or prominence, distance it has a predetermined radius and by prominence you need to add
the argument radius= (the distance you wanna specified), advices rank_by = 'distance' cannot be used with radius 
"""
restaurantsG = api.places_nearby(location = lat_lon_G, rank_by='distance', type='restaurant')

#transforming the python dictionaty into a dataframe
"""
where we have to use read_json and inside a json.dumps because remember we have a python dictionary no a json,
we select the key 'results' because contains the results from the API and in orient records because is the orientation of the json
"""
raw_restaurants_nearbyG = pd.read_json(json.dumps(restaurantsG['results']), orient='records') 
print(raw_restaurants_nearbyG.columns)

#selecting useful columns
relevant_cols = ['name','place_id', 'rating', 'types','user_ratings_total']
#Getting a dataframe only with the useful columns
restaurants_nearbyG = raw_restaurants_nearbyG[relevant_cols]

"""
B. Create a function to Find the Place Id given Place Name (String) and Location (Lat/Lont Tuple).
C. Find the Place ID of the following places using your functions:
* McCarthy's Irish Pub - Caucel
* Starbucks Montejo (20.984962,-89.6181338)
* Los Trompos Circuito
"""
# It is not neccessary to make a function due to googlemaps has a similar function "find_place"
#variable declaration for the first place
"""
in find.place(the first arguments is the name of the place, input_type is whant kind of input is in this case we have to 
specify is a textquery, a simple text, fields we introduce the place id, but we can send other tipe of references(it is in the API documentation)
location_bias is the coordinates and you need to put it as circle:(the radius)@latitude@longitude
"""
lat_lon1G = [20.9999339,-89.6825716]
place_name1G = 'McCarthy´s Irish Pub'
place_ID1G = api.find_place(place_name1G ,input_type='textquery', fields = ['place_id'], location_bias = 'circle:1000@{},{}'.format(lat_lon1G[0],lat_lon1G[1]))
#variable declaration for the second place
lat_lon2G = [20.984962,-89.6181338]
place_name2G = 'Starbucks Montejo'
place_ID2G = api.find_place(place_name2G,input_type='textquery' ,fields = ['place_id'], location_bias = 'circle:1000@{},{}'.format(lat_lon2G[0],lat_lon2G[1]))

#variable declaration for the third place
lat_lon3G = [20.9987668,-89.6175597]
place_name3G = 'Los Trompos'
place_ID3G = api.find_place(place_name3G,input_type='textquery', fields = ['place_id'], location_bias = 'circle:1000@{},{}'.format(lat_lon3G[0],lat_lon3G[1]))

#output of the places´ID
print(place_ID1G)
print(place_ID2G)
print(place_ID3G)

"""
D. Use the [*Place Details*](https://developers.google.com/places/web-service/details#PlaceDetailsResults) Method to find the Reviews of a Place in English and Spanish. In order to fulfill this item you need to:
* Create a *find_reviews* function with the appropiate parameters. It must return a JSON with the results. 
* Create a table with the following columns: Author Name, Language, Rating, Text, Time.
"""

#defining ID of the place
IDG = 'ChIJJyKKOKB0Vo8RCQcxkUw6hp8'

#getting the reviews, using the funcion .place
"""
Where place_id is the unique id of the place that google gives it, fields is want you want for  this place(check documentation)
and language is the language of the reviews all the languages are in the documentation
"""
reviews_englishG = api.place(place_id = IDG,fields = ['review'] ,language =  'en')
reviews_spanishG = api.place(place_id = IDG,fields = ['review'] ,language ='es')

#transforming python dictionary into a dataframe
raw_reviews_English_dfG = pd.read_json(json.dumps(reviews_englishG['result']['reviews']), orient='records')
raw_reviews_Spanish_dfG = pd.read_json(json.dumps(reviews_spanishG['result']['reviews']), orient= 'records')

#selecting columns that will be used
rel_columns = ['author_name','language', 'rating','text','time']
reviews_English_dfG = raw_reviews_English_dfG[rel_columns]
reviews_Spanish_dfG = raw_reviews_Spanish_dfG[rel_columns]

#getting the time from unixtime to real time of rather human, where unit=to the scale of time 
reviews_English_dfG['time'] = pd.to_datetime(reviews_English_dfG['time'], unit='s')
reviews_Spanish_dfG['time'] = pd.to_datetime(reviews_Spanish_dfG['time'], unit='s')

print(reviews_English_dfG)

"""
E. Find similar places to Los Trompos Circuito. Rank them by its "Prominence". In order to fulfill this item you need to:
* Create a *find_similar* function with the appropiate parameters. It must return a JSON with the results.
* Create a table with the following columns: Place Name, Plaece Id, Rating, Total of Use Ratings.
"""
#Using find_places nearby with the characteristics we want

#coordinates of the places that we want to get is competition in this case, Los trompos
coordinatesG = (20.9987668,-89.6175597)
radiusG = 1500
typesG = 'restaurant'
competitionG = api.places_nearby(location = coordinatesG, radius = radiusG, rank_by='prominence', type=typesG)

#transforming into a dataframe
raw_dataframeG = pd.read_json(json.dumps(competitionG['results']), orient='records')

#gets the rows with restaurants that are not all similar as the one that are bars and cafes
limpiezaG = raw_dataframeG['types']
#comprenhension list to gets the number that containt row the must be eliminated
get_nomatchingG = [i for i in range(0,len(limpiezaG)) if "bar" in limpiezaG[i] or "cafe" in limpiezaG[i]]

#eliminating no so similar restaurants
raw_dataframeG = raw_dataframeG.drop(get_nomatchingG, axis = 0)

#selecting the useful columns
colRel = ['name','place_id','rating','user_ratings_total'] 
#eliminating our restaurant ("Los trompos")
dataframeG = raw_dataframeG[colRel].drop([4], axis = 0).reset_index(drop=True)
dataframeG.head()

"""
As a conclusion as we see the googlemaps library is easier to use than the first method we did, are kind of similar because the 
arguments are most the same, but knowing how to use an API is useful to later know how it works instead of only depending on libraries
"""
