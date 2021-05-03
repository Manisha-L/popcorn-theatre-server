from flask import Flask, request, jsonify
import pandas as pd
import json
import math
import time
import sys
sys.path.append('CollaborativeFiltering/')
from SimpleUserCF import runUserColaborativeFiltering
from SimpleItemCF import runItemBasedColaborativeFiltering
from flask_cors import CORS

# init app
app = Flask(__name__)
CORS(app)


link_df = pd.read_csv("ml-latest-small/links.csv")

def get_movielensID_from_tmdbID(tmdbID):
    link_df = pd.read_csv("ml-latest-small/links.csv")
    row = link_df[link_df["tmdbId"] == tmdbID]
    if (len(row["movieId"]) == 0):
        return -1
    return int(row["movieId"])

get_movielensID_from_tmdbID(11860)   
    
def get_tmdbID_from_movielensTD(ML_ID):
    link_df = pd.read_csv("ml-latest-small/links.csv")
    row = link_df[link_df["movieId"] == ML_ID]
    print("-------------------row=", row)
    if (len(row["tmdbId"]) == 0):
        return -1
    try:    
        return int(row["tmdbId"])
    except:
        return
        
get_tmdbID_from_movielensTD(356)

def counvert_ratings_to_tuple_format(user_ratings):
    # given the ratings in form of lists [tmdbID, rating] --> [ML_ID, ratind]
    temp_ratings = []
    for [tmdbID, rating] in user_ratings:
        #print("rating = ", rating)
        temp_ratings.append((get_movielensID_from_tmdbID(tmdbID), rating))
    return temp_ratings



def add_user_to_dataset(userID, user_ratings):
    # userID --> actual userID
    # user_ratings = [ [ML_movieID, rating] ]
    usersMap = pd.read_csv("ml-latest-small/users_map.csv")
    a = {"innerId":[],"userId":[]}

    

    isUserInMaps = usersMap['userId'].str.contains(userID)
    isUserInMapsFalse = isUserInMaps.bool() == False
    print('ven checks user id in usermap',isUserInMapsFalse)

    ratings = pd.read_csv("ml-latest-small/ratings.csv")

    print('ven check ratings present all', ratings['userId'].max())

    if(isUserInMaps.empty):
        newUserId = ratings['userId'].max() + 1
    elif(isUserInMapsFalse):
        newUserId = ratings['userId'].max() + 1
    else:
        findExistUserId = usersMap['innerId'][usersMap['userId'].str.find(userID)]
        newUserId = findExistUserId[0]
        print(newUserId)

    print(newUserId)
    if(isUserInMaps.empty):
        a["userId"].append(userID)
        a["innerId"].append(newUserId)
        a_df = pd.DataFrame(a)
        users = pd.concat([usersMap, a_df], axis=0)
        users.to_csv("ml-latest-small/users_map.csv", index=False)

    d = {"userId":[],"movieId":[], "rating":[], "timestamp":[]}
    for rating in user_ratings:
        d["userId"].append(newUserId)
        d["movieId"].append(rating[0])
        d["rating"].append(rating[1])
        d["timestamp"].append(time.time())
    d_df = pd.DataFrame(d)
    print('ven', user_ratings)
    ratings = pd.concat([ratings, d_df], axis=0)
    ratings.to_csv("ml-latest-small/ratings.csv", index=False)
    totalrows = ratings.shape[0]-1
    
    return newUserId
    
        
    
def reset_files():
    reset_ratings = pd.read_csv("reset_ratings.csv")
    reset_ratings.to_csv("ml-latest-small/ratings.csv", index=False)
    print("Ratings file reset")


def colaborativeFilering_UserBased(user_ratings, userID="672"):
    # the ids returned are from the movielens dataset
    recommendatons_movieLens = runUserColaborativeFiltering(testSubject=str(userID))
    print(recommendatons_movieLens)
    recommendations_tmdb = []
    for recommendation in recommendatons_movieLens:
        recommendations_tmdb.append(get_tmdbID_from_movielensTD(int(recommendation)))
    return recommendations_tmdb

def colaborativeFiltering_ItemBased(user_ratings, userID="672"):
    # the ids returned are from the movielens dataset
    print('ven checks user id', userID)
    recommendatons_movieLens = runItemBasedColaborativeFiltering(testSubject=str(userID))
    print(recommendatons_movieLens)
    recommendations_tmdb = []
    for recommendation in recommendatons_movieLens:
        recommendations_tmdb.append(get_tmdbID_from_movielensTD(int(recommendation)))
    return recommendations_tmdb
    
    
    
@app.route("/")
def index():
    return "This is the home route"

@app.route("/recommendations/usercolaborativefiltering", methods=["POST"])
def user_colaborativefiltering() :
    
    userID = request.json["userID"]
    user_ratings = request.json["ratings"]

    print("user id = ", userID)
    print("user_ratings = ", user_ratings)

    user_ratings = json.loads(user_ratings)
    user_ratings = counvert_ratings_to_tuple_format(user_ratings)  
    userID = add_user_to_dataset(userID, user_ratings)
    

    recommendations = colaborativeFilering_UserBased(user_ratings, userID)
    print(recommendations)
    reset_files()
    return jsonify(recommendations)
    
    
@app.route("/recommendations/itemcolaborativefiltering", methods=["POST"])
def item_colaborativefiltering():
    userID = request.json["userID"]
    user_ratings = request.json["ratings"]
    recommender_type = request.json["recommender_type"]
    print("user id = ", userID)
    print("user_ratings = ", user_ratings)
    print("recommender_type = ", recommender_type)
    user_ratings = json.loads(user_ratings)
    user_ratings = counvert_ratings_to_tuple_format(user_ratings)  
    print("user Rating in tuple format = ", user_ratings)
    userID = add_user_to_dataset(userID, user_ratings)
    print("ven checks userId before passing to Itemfilter", request.json["userID"])
    recommendations = colaborativeFiltering_ItemBased(user_ratings, userID)
    print(recommendations)
    reset_files()
    return jsonify(recommendations)

# RunServer
if __name__ == "__main__":
    app.run()