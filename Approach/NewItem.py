
from MovieLens import MovieLens
from NewItemMovieLens import NewItemMovieLens
from surprise import KNNBasic
import heapq
from collections import defaultdict
from operator import itemgetter
  

def runItemBasedFiltering(testSubject = '85',k = 10):
    ml = MovieLens()
    niml = NewItemMovieLens()
    data = niml.loadMovieLensLatestSmall()

    usermvs =  ml.getUserMovies(float(testSubject))
    allmvs = niml.getAllMovies()
    allGenres = ml.getGenres()


    print('ven to see whether actual user is getting here', allmvs)
    print('ven to see whether actual user is getting here', usermvs)

    recommendedMovie = []
    
    for mvid in usermvs:
        if(mvid >= 0):
            for allmvid in allmvs:
                recommendedMovie.append(niml.computeGenreSimilarity( allmvid, mvid, allGenres))
                print('ven checks grec', ml.computeGenreSimilarity( allmvid, mvid, allGenres)) 

   

    pos = 0
    
    recommendations = []
    from operator import itemgetter
    isPositiveRec =  max(recommendedMovie,key=itemgetter(1))[1]
    positiveRec =  max(recommendedMovie,key=itemgetter(1))[0]

    if(isPositiveRec > 0.0):
        recommendations.append(positiveRec)




        
    return recommendations

    
