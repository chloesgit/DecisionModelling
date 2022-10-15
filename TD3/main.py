from urllib.parse import DefragResult
import pandas as pd
import math
from scipy import stats
import random


def critiques(excelFile):
    df = pd.read_excel(excelFile, header=None)
    df.to_csv("file_to_csv.csv", index=None)
    dataframeObject = pd.DataFrame(pd.read_csv("file_to_csv.csv"))
    list = dataframeObject.values.tolist()
    dico = {}
    for i in range(1, len(list)):
        dico2 = {}
        for j in range(1, len(list[i])):
            if not math.isnan(float(list[i][j])):
                dico2[list[0][j]] = float(list[i][j])

        dico[list[i][0]] = dico2
    return dico


print("dictionnaire de critiques", critiques("critiques.xlsx"))
Critiques = critiques("critiques.xlsx")
Critiques["Anne"] = {'Lady': 1.5, "Luck": 4, "Dupree": 2.0}
ListMovies = ["Lady", "Snakes", "Luck", "Superman", "Dupree", "Night"]


def sim_distanceManhattan(pers1, pers2):
    dist = 0
    for movie in pers1.keys():
        if movie in pers2.keys():
            dist += abs(pers1[movie]-pers2[movie])
    return dist


def sim_distanceEuclidienne(pers1, pers2):
    dist = 0
    for movie in pers1.keys():
        if movie in pers2.keys():
            dist += (pers1[movie]-pers2[movie])**2
    return math.sqrt(dist)


def recommendNearestNeighbor(nouveauCritique, Critiques):
    closestNeighbor, dist = 0, False
    for user in Critiques.keys():
        if user != nouveauCritique:
            newDistance = sim_distanceEuclidienne(
                Critiques[nouveauCritique], Critiques[user])
            if dist == False or dist > newDistance:
                dist = newDistance
                closestNeighbor = user
    recommend = []
    for movie in Critiques[closestNeighbor]:
        if movie not in Critiques[nouveauCritique]:
            recommend.append((movie, Critiques[closestNeighbor][movie]))
    return recommend


print("Recommandation pour Anne avec Nearest Neighbor",
      recommendNearestNeighbor("Anne", Critiques))


def calculateGlobalScore(user, Critiques, ListMovies):
    Total, s, sprime = {}, {}, {}
    for movie in ListMovies:
        if movie not in Critiques[user]:
            sval = 0
            val = 0
            for critique in Critiques:
                if critique != user and critique != "Toby" and movie in Critiques[critique]:
                    sval += 1 / \
                        (1 +
                         sim_distanceManhattan(Critiques[critique], Critiques[user]))
                    val += Critiques[critique][movie] / \
                        (1 +
                         sim_distanceManhattan(Critiques[critique], Critiques[user]))
            Total[movie] = val
            s[movie] = sval
            sprime[movie] = val/sval
    return Total, s, sprime


def Bestrecommend(user, Critiques, ListMovies):
    _, _, sprime = calculateGlobalScore(user, Critiques, ListMovies)
    bestMovie, highScore = False, 0
    for movie in sprime:
        if bestMovie == False or sprime[movie] > highScore:
            highScore = sprime[movie]
            bestMovie = movie
    return bestMovie


print("Recommandation pour Anne avec Best",
      Bestrecommend("Anne", Critiques, ListMovies))


def calculateGlobalScoreExp(user, Critiques, ListMovies):
    Total, s, sprime = {}, {}, {}
    for movie in ListMovies:
        if movie not in Critiques[user]:
            sval = 0
            val = 0
            for critique in Critiques:
                if critique != user and critique != "Toby" and movie in Critiques[critique]:
                    sval += math.exp(-sim_distanceManhattan(
                        Critiques[critique], Critiques[user]))
                    val += Critiques[critique][movie] * \
                        math.exp(-sim_distanceManhattan(
                            Critiques[critique], Critiques[user]))
            Total[movie] = val
            s[movie] = sval
            sprime[movie] = val/sval
    return Total, s, sprime


def BestrecommendExp(user, Critiques, ListMovies):
    _, _, sprime = calculateGlobalScoreExp(user, Critiques, ListMovies)
    bestMovie, highScore = False, 0
    for movie in sprime:
        if bestMovie == False or sprime[movie] > highScore:
            highScore = sprime[movie]
            bestMovie = movie
    return bestMovie


print("Recommandation pour Anne avec Best exponentiel",
      BestrecommendExp("Anne", Critiques, ListMovies))


def sim_distanceCosine(pers1, pers2):
    num = 0  # compute the numerator
    sqx, sqy = 0, 0
    for movie in pers1.keys():
        if movie in pers2.keys():
            num += pers1[movie]*pers2[movie]
            sqx += pers1[movie]*pers1[movie]
            sqy += pers2[movie]*pers2[movie]
    if sqx == 0 and sqy == 0:
        return 0
    return num/(math.sqrt(sqx)+math.sqrt(sqy))


def PearsonRecommend(dico, user, ListMovies):
    saprime = {}
    for movie in ListMovies:
        if movie not in dico[user].keys():
            total = 0
            sa = 0
            for critique in dico.keys():
                if critique != user and critique != "Toby":
                    critique_score = []
                    for movie2 in dico[user].keys():
                        if movie2 in dico[critique].keys():
                            critique_score.append(dico[critique][movie2])
                        else:
                            critique_score.append(0)
                    pearson, _ = stats.pearsonr(
                        list(critique_score), list(dico[user].values()))
                    sa += math.exp(-pearson)
                    if movie in dico[critique].keys():
                        total += math.exp(-pearson)*dico[critique][movie]
            saprime[movie] = total/sa
    return (max(saprime, key=saprime.get))


print("Recommandation pour Anne avec Pearson",
      PearsonRecommend(Critiques, "Anne", ListMovies))


def calculateGlobalScoreCosine(user, Critiques, ListMovies):
    Total, s, sprime = {}, {}, {}
    for movie in ListMovies:
        if movie not in Critiques[user]:
            sval = 0
            val = 0
            for critique in Critiques:
                if critique != user and critique != "Toby" and movie in Critiques[critique]:
                    sval += math.exp(-sim_distanceCosine(
                        Critiques[critique], Critiques[user]))
                    val += Critiques[critique][movie] * \
                        math.exp(-sim_distanceCosine(
                            Critiques[critique], Critiques[user]))
            Total[movie] = val
            s[movie] = sval
            sprime[movie] = val/sval
    return Total, s, sprime


def CosineRecommend(user, Critiques, ListMovies):
    _, _, sprime = calculateGlobalScoreCosine(user, Critiques, ListMovies)
    bestMovie, highScore = False, 0
    for movie in sprime:
        if bestMovie == False or sprime[movie] > highScore:
            highScore = sprime[movie]
            bestMovie = movie
    return bestMovie


print("Recommandation pour Anne avec Cosine",
      CosineRecommend("Anne", Critiques, ListMovies))

Songs = {
    "Angelica": {"Blues Traveler": 3.5, "Broken Bell": 2, "Norah Jones": 4.5, "Phoenix": 5, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2},
    "Bill": {"Blues Traveler": 2, "Broken Bell": 3.5, "Deadmau5": 4, "Phoenix": 2, "Slightly Stoopid": 3.5, "Vampire Weekend": 3},
    "Chan": {"Blues Traveler": 5, "Broken Bell": 1, "Deadmau5": 1, "Norah Jones": 3, "Phoenix": 5, "Slightly Stoopid": 1},
    "Dan": {"Blues Traveler": 3, "Broken Bell": 4, "Deadmau5": 4.5, "Phoenix": 3, "Slightly Stoopid": 4.5, "The Strokes": 4, "Vampire Weekend": 2},
    "Hailey": {"Broken Bell": 4, "Deadmau5": 1, "Norah Jones": 4, "The Strokes": 4, "Vampire Weekend": 1},
    "Jordyn": {"Broken Bell": 4.5, "Norah Jones": 4, "Deadmau5": 5, "Phoenix": 5, "Slightly Stoopid": 4.5, "The Strokes": 4, "Vampire Weekend": 4},
    "Sam": {"Blues Traveler": 5, "Broken Bell": 2, "Norah Jones": 3, "Phoenix": 5, "Slightly Stoopid": 4, "The Strokes": 5},
    "Veronica": {"Blues Traveler": 3, "Norah Jones": 5, "Phoenix": 4, "Slightly Stoopid": 2.5, "The Strokes": 3}
}

ListSongs = ["Blues Traveler", "Broken Bell", "Norah Jones", "Deadmau5",
             "Phoenix", "Slightly Stoopid", "The Strokes", "Vampire Weekend"]


def compare(user, List, ListObject):
    # ex: Anne, Critique, ListMovies
    print("Recommendations to "+user)
    print("Recommend nearest neighbor:")
    print(recommendNearestNeighbor(user, List))
    print("Recommend based on best Global Score (distance Manhattan)")
    print(Bestrecommend(user, List, ListObject))
    print("Recommend based on best Global Score (distance Exp)")
    print(BestrecommendExp(user, List, ListObject))
    print("Recommend based on best Global Score (distance Pearson)")
    print(PearsonRecommend(List, user, ListObject))

    print("Recommend based on best Global Score (distance Cosine)")
    print(CosineRecommend(user, List, ListObject))
    print("")


compare('Veronica', Songs, ListSongs)
compare('Anne', Critiques, ListMovies)


# def createCritics(Users, Movies):
#     res = {}
#     empty_cells = 0
#     M, N = len(Movies), len(Users)
#     for user in Users:
#         nbVotes = random.randint(1, M)
#         empty_cells += M-nbVotes
#         unvotedMovies = list(Movies)
#         votes = {}
#         for i in range(nbVotes):
#             index_movie_to_vote = random.randint(0, len(unvotedMovies)-1)
#             votes[unvotedMovies[index_movie_to_vote]] = random.randint(1, 5)
#             unvotedMovies.pop(index_movie_to_vote)
#         res[user] = votes
#     return res, empty_cells/(M*N)


def createCritics(nbCritiques, nbMovies):
    critiques = {}
    size = nbCritiques*nbMovies
    coeff = random.randint(30, 50)/100
    nbZero = 0
    for i in range(nbCritiques):
        critiques["critique "+str(i)] = {}
        for j in range(nbMovies):
            critiques["critique "+str(i)]["movie " +
                                          str(j)] = random.randint(1, 10)/2
    while nbZero <= size*coeff:
        i = random.randint(0, nbMovies-1)
        j = random.randint(0, nbCritiques-1)
        key1 = "critique "+str(j)
        key2 = "movie "+str(i)
        if key1 in critiques.keys():
            if key2 in critiques[key1].keys() and len(critiques[key1].keys()) > 2:
                del critiques[key1][key2]
                nbZero += 1
    return critiques


def recommandationNearestNeighbor(user, critiques):
    recommandation = recommendNearestNeighbor(user, critiques)
    max = 0
    movieRecommended = ""
    for movie in recommandation:
        if movie[1] > max:
            max = movie[1]
            movieRecommended = movie[0]
    return movieRecommended


def allRatingsDifferent():
    nbCritiques = random.randint(10, 20)
    nbMovies = random.randint(10, 20)
    while True:
        critiques = createCritics(nbCritiques, nbMovies)
        user = "critique " + str(random.randint(0, len(critiques)-1))
        ListMovies = ["movie "+str(i) for i in range(nbMovies)]
        recommendation = []
        while len(critiques[user].keys()) > nbMovies/2:
            i = random.randint(0, len(critiques[user])-1)
            if "movie "+str(i) in critiques[user].keys():
                del critiques[user]["movie "+str(i)]
        cosine = CosineRecommend(user, critiques, ListMovies)
        recommendation.append(cosine)
        pearson = PearsonRecommend(critiques, user, ListMovies)
        recommendation.append(pearson)
        if recommendation[0] == recommendation[1]:
            continue
        bestrecommendexp = BestrecommendExp(user, critiques, ListMovies)
        recommendation.append(bestrecommendexp)
        if recommendation[0] == recommendation[2] or recommendation[1] == recommendation[2]:
            continue
        bestrecommend = Bestrecommend(user, critiques, ListMovies)
        recommendation.append(bestrecommend)
        if recommendation[0] == recommendation[3] or recommendation[1] == recommendation[3] or recommendation[2] == recommendation[3]:
            continue
        nearestneighbor = recommandationNearestNeighbor(user, critiques)
        recommendation.append(nearestneighbor)
        if recommendation[0] == recommendation[4] or recommendation[1] == recommendation[4] or recommendation[2] == recommendation[4] or recommendation[3] == recommendation[4]:
            continue
        print("Pearson : ", pearson)
        print("Cosine : ", cosine)
        print("Bestrecommendexp : ", bestrecommendexp)
        print("Bestrecommend : ", bestrecommend)
        print("Nearestneighbor : ", nearestneighbor)
        break
    return (critiques)


print("Liste vérifiant les différentes conditions imposées à la question 4",
      allRatingsDifferent())
