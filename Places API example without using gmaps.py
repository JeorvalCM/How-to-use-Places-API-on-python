                    <center> <h1> Google Maps API </h> </center> 
"""
A. Use the [*Nearby Seach*](https://developers.google.com/places/web-service/search) Method to find all the restaurant near to the UPY (20.988459, -89.736768) around 2km. In order to fulfill this item you need to:
* Create a *search_nearby_places* function with the appropiate parameters. It must return a JSON with the results. Places must be ranked by distance.
* Create a table with the following columns: Name, Place Id, Rating, Place Types, Total of User Ratings.
"""
#importing libraries need
import pandas as pd
import json
import requests

#I recommend you to declare the api key as an global variable to not pass it as an argument
#declaring the key of tha api that will be used through all the programm
#Introduce your key
key_api ='*******'

#all the urls are getting from the api documentation
def search_nearby_places(key, lat, lon, distance):
    """
    Docstring
    Description: function to get all the nearby restaurants from a location
    Input: An api_key from google cloud, latitude and longitude of the places you wanto to know the restaurants nearby
    distance is how far can be the restaurant
    output_ return a python dictionary that contains information relative to the nearby places
    """
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={},{}&radius={}&type=restaurant&key={}'.format(lat, lon, distance, key)
   
   #get the file or json from an url
    res = requests.get(url)
    
    #json.loads gets a json a turn into a python dictionary
    results = json.loads(res.content)
    return results
    
 """
 You can changes the type if you want to have more results, but in this case we are looking for only restaurants
 """
 #getting the restaurants nearby a location using the function
restaurants = search_nearby_places(key_api,20.988459, -89.736768, 3000)
print(restaurants)

#transforming the python dictionaty into a dataframe, remember use .dumps to make it a json, because in the function we transformed it
#into a python dictionary
raw_restaurants_nearby = pd.read_json(json.dumps(restaurants['results']), orient='records') 
#checking the columns names
print(raw_restaurants_nearby.columns)

#selecting useful columns
relevant_cols = ['name','place_id', 'rating', 'types','user_ratings_total']
#Getting a dataframe only with the useful columns
restaurants_nearby = raw_restaurants_nearby[relevant_cols]
print(restaurants_nearby.head())

"""
B. Create a function to Find the Place Id given Place Name (String) and Location (Lat/Lont Tuple).
"""

def find_place(PlaceName, Location):
    """
    Docstring
    Description: function that gets a place´s ID given its name and location
    Input: string that contains the place´s name and tuple that contains latitude and longitude of its location
    Output: return the place´s ID
    """
    #this replace must be done because at the url the spaces between words have to be %20
    #could be added more fields and change the radius, but for now it is innecessary
    PlaceName = PlaceName.replace(" ","%20")
    url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={}&inputtype=textquery&fields=place_id&locationbias=circle:2000@{},{}&key={}'.format(PlaceName, Location[0],Location[1], key_api)
    res = requests.get(url)
    results = json.loads(res.content)
    #only return the part of results['candidates'] because is the key that give us the fields that we asked for
    return results['candidates']
    
    """
    C. Find the Place ID of the following places using your functions:
* McCarthy's Irish Pub - Caucel
* Starbucks Montejo (20.984962,-89.6181338)
* Los Trompos Circuito
    """
    #variable declaration for the first place
    #lat_lon are latitude and longitude coordinates
lat_lon1 = (20.9999339,-89.6825716)
place_name1 = 'McCarthy´s Irish Pub'
place_ID1 = find_place(place_name1, lat_lon1)
#variable declaration for the second place
lat_lon2 = (20.984962,-89.6181338)
place_name2 = 'Starbucks Montejo'
place_ID2 = find_place(place_name2, lat_lon2)

#variable declaration for the third place
lat_lon3 = (20.9987668,-89.6175597)
place_name3 = 'Los Trompos'
place_ID3 = find_place(place_name3, lat_lon3)

#output of the places´ID
print(place_ID1)
print(place_ID2)
print(place_ID3)

"""
D. Use the [*Place Details*](https://developers.google.com/places/web-service/details#PlaceDetailsResults) Method to find the Reviews of a Place in English and Spanish. In order to fulfill this item you need to:
* Create a *find_reviews* function with the appropiate parameters. It must return a JSON with the results. 
* Create a table with the following columns: Author Name, Language, Rating, Text, Time.
"""
def find_reviews(PlaceID, language):
    """
    Docstring:
    Description: function that gets the review of a place given its ID
    input: ID of the place we eant its reviews and the language wanted for the reviews
    output: return a python dictionary that contain all the information related to the reviews
    """
    url = 'https://maps.googleapis.com/maps/api/place/details/json?place_id={}&language={}&fields=review&key={}'.format(PlaceID,language,key_api)
    res = requests.get(url)
    results = json.loads(res.content)
    return results
    
#defining ID of the place
ID = 'ChIJJyKKOKB0Vo8RCQcxkUw6hp8'

#getting the reviews
reviews_english = find_reviews(ID, 'en')
reviews_spanish = find_reviews(ID, 'es')

#transforming python dictionary into a dataframe
raw_reviews_English_df = pd.read_json(json.dumps(reviews_english['result']['reviews']), orient='records')
raw_reviews_Spanish_df = pd.read_json(json.dumps(reviews_spanish['result']['reviews']), orient= 'records')

#selecting columns that will be used
rel_columns = ['author_name','language', 'rating','text','time']
reviews_English_df = raw_reviews_English_df[rel_columns]
reviews_Spanish_df = raw_reviews_Spanish_df[rel_columns]

#getting the time from unixtime to real time of rather human
reviews_English_df['time'] = pd.to_datetime(reviews_English_df['time'], unit='s')
reviews_Spanish_df['time'] = pd.to_datetime(reviews_Spanish_df['time'], unit='s')

print(reviews_English_df)
print(reviews_Spanish_df)

"""
E. Find similar places to Los Trompos Circuito. Rank them by its "Prominence". In order to fulfill this item you need to:
* Create a *find_similar* function with the appropiate parameters. It must return a JSON with the results.
* Create a table with the following columns: Place Name, Plaece Id, Rating, Total of Use Ratings.
"""

def find_similar(key_api, coordinates, radius, types):
    """
    Docstring:
    Description: function that get similar places to one given and sort by its prominence
    Input: coordinates of the place , radius to know how far the competition can be and type of the place you look for
    Output: return a python dictionary that contains all the information to all the places that are the competition
    sorted by its prominence
    """
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={},{}&radius={}&rankby=prominence&type={}&key={}'.format(coordinates[0],coordinates[1], radius, types, key_api)
    res = requests.get(url)
    result = json.loads(res.content)
    return result
    
#coordinates of the places that we want to get is competition in this case, Los trompos
coordinates = (20.9987668,-89.6175597)
radius = 1500
types = 'restaurant'

#getting the places
raw_data = find_similar(key_api, coordinates, radius, types)
#transforming into a dataframe
raw_dataframe = pd.read_json(json.dumps(raw_data['results']), orient='records')

#getting the rows with restaurants that are not all similar as the one that are bars and cafes
limpieza = raw_dataframe['types']
#comprenhension list to gets the number that containt row the must be eliminated
get_nomatching = [i for i in range(0,len(limpieza)) if "bar" in limpieza[i] or "cafe" in limpieza[i]]

raw_dataframe = raw_dataframe.drop(get_nomatching, axis = 0)

#selecting the useful columns
colRel = ['name','place_id','rating','user_ratings_total'] 
#eliminating the trompos of the dataframe
dataframe = raw_dataframe[colRel].drop([4],axis = 0).reset_index(drop = True)
dataframe.head(8)

"""
Congratulations you have finished, therefore, you should practice more to dominate the Place API :)
"""
