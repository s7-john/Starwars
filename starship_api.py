import requests
from pprint import pprint
import pymongo

starships_url = "https://swapi.dev/api/starships/"
list_of_ships = []

#This functiom is to dynamically go through the pages of starships using a while loop.
def url_results():
    page = starships_url
    while page:
        json_return = requests.get(page).json()
        for ship in json_return["results"]:
            list_of_ships.append(ship)  # The ships and details from the url will be added to this empty list.
        page = json_return["next"]


#    pprint(list_of_ships)

# url_results()


client = pymongo.MongoClient()
db = client['starwars']


# This function deletes the starship collection
def delete_starship_collection():
    db.starships.drop()


# This function is used to create a starship collection
def creating_starship_collection():
    db.create_collection("Starships")


# This function is to insert starships collection to the starwars database
def insert_starships_collection():
    for starship in list_of_ships:
        db.starships.insert_one(starship)

