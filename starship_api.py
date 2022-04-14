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


# This function deletes the starship collection if already present
def delete_starship_collection():
    db.starships.drop()


# This function is used to create a starship collection
def creating_starship_collection():
    db.create_collection("Starships")


# This function is to insert starships collection to the starwars database
def insert_starships_collection():
    for starship in list_of_ships:
        db.starships.insert_one(starship)


# This function is to replace all the pilot urls with the pilot ids
def update_pilot_info():
    # Finds starship documents in the collection
    for ship in db.starship.find({}, {"_id": 1, "name": 1, "pilots": 1}):
        # If pilots are present then run the loop
        if ship["pilots"] != []:
            # List of pilot names for each starship
            pilot_names = [requests.get(pilot_url).json()["name"] for pilot_url in ship["pilots"]]
            # Finding id of pilot from their names
            ids_of_pilot = [next(db.characters.find({"name": name}))["_id"] for name in pilot_names]
            # Updates collection of pilot urls to ids
            db.starships.update_one({"_id": ship["_id"]}, {"$set":{"pilots":ids_of_pilot}})


#run