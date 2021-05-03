
from MovieLens import MovieLens
from NewItemMovieLens import NewItemMovieLens
from surprise import KNNBasic
import heapq
from collections import defaultdict
from operator import itemgetter
  

def runItemBasedColaborativeFiltering(testSubject = '85',k = 10):
    ml = MovieLens()
    niml = NewItemMovieLens()
    data = niml.loadMovieLensLatestSmall()

    usermvs =  ml.getUserMovies(float(testSubject))
    allmvs = niml.getAllMovies()
    allGenres = ml.getGenres()
    # allGenres1 = niml.getGenres()

    print('ven to see whether actual user is getting here', allmvs)
    print('ven to see whether actual user is getting here', usermvs)

    recommendedMovie = []
    
    for mvid in usermvs:
        if(mvid >= 0):
            for allmvid in allmvs:
                recommendedMovie.append(niml.computeGenreSimilarity( allmvid, mvid, allGenres))
                print('ven checks grec', ml.computeGenreSimilarity( allmvid, mvid, allGenres)) 

    # for allmvid in allmvs:
    #     for mvid in usermvs:
    #         if(mvid >= 0):
    #             recommendedMovie.append(niml.computeGenreSimilarity(  mvid, allmvid, allGenres))  
    
    # wrong
    # for allmvid in allmvs:
    #     for mvid in usermvs:
    #         print('ven checks grec', ml.computeGenreSimilarity( allmvid, mvid, allGenres))  

    # for mvid in usermvs:
    #     print('ven checks grec', mvid)   

    # for mvid in allmvs:
    #     print('ven checks grec', mvid)
    



    # print('check data', data)
    # trainSet = data.build_full_trainset()
    
    # sim_options = {'name': 'cosine',
    #                'user_based': False}
    
    # model = KNNBasic(sim_options=sim_options)
    # model.fit(trainSet)
    # simsMatrix = model.compute_similarities()
    
    # testUserInnerID = trainSet.to_inner_uid(testSubject)


    # print('check usermovies', usermvs)



     

    

    # for movieId in grec:
    #     print(ml.getMovieName(int(movieId)))


    # # Get the top K items we rated
    # testUserRatings = trainSet.ur[testUserInnerID]
    # kNeighbors = heapq.nlargest(k, testUserRatings, key=lambda t: t[1])
    
    # # Get similar items to stuff we liked (weighted by rating)
    # candidates = defaultdict(float)
    # for itemID, rating in kNeighbors:
    #     similarityRow = simsMatrix[itemID]
    #     for innerID, score in enumerate(similarityRow):
    #         candidates[innerID] += score * (rating / 5.0)
        
    # # Build a dictionary of stuff the user has already seen
    # watched = {}
    # for itemID, rating in trainSet.ur[testUserInnerID]:
    #     watched[itemID] = 1
        
    # # Get top-rated items from similar users:
    # pos = 0
    # recommendations = []
    # print("\n\n-------------------<><><><>--------------------")
    # for itemID, ratingSum in sorted(candidates.items(), key=itemgetter(1), reverse=True):
    #     if not itemID in watched:
    #         movieID = trainSet.to_raw_iid(itemID)
    #         movieID = float(movieID)
    #         movieID = int(movieID)
    #         recommendations.append(int(movieID))
    #         print(ml.getMovieName(int(movieID)), ratingSum)
    #         pos += 1
    #         if (pos > 20):
    #             break
    # print("\n\n-------------------<><><><>--------------------")

    pos = 0
    # return recommendations
    recommendations = []
    from operator import itemgetter
    isPositiveRec =  max(recommendedMovie,key=itemgetter(1))[1]
    positiveRec =  max(recommendedMovie,key=itemgetter(1))[0]

    if(isPositiveRec > 0.0):
        recommendations.append(positiveRec)


    # print("\n\n-------------------<><><><>--------------------")
    # for itemID, ratingSum in recommendedMovie:
    #     # movieID = trainSet.to_raw_iid(itemID)
    #     # movieID = float(movieID)
    #     movieID = itemID
    #     recommendations.append(int(movieID))
    #     print(ml.getMovieName(int(movieID)), ratingSum)
    #     pos += 1
    #     if (pos > 20):
    #         break
    # print("\n\n-------------------<><><><>--------------------")

        
    return recommendations

    
