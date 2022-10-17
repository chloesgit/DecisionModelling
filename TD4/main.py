from re import S
import pandas as pd
import random


def convert_excel_to_list(file_name):
    excelFile = pd.read_excel(file_name, header=None)
    excelFile.to_csv("file_to_csv.csv", index=None)
    dataframeObject = pd.DataFrame(pd.read_csv("file_to_csv.csv"))
    list = dataframeObject.values.tolist()
    dico = {}
    for voter in list:
        dico[voter[0]] = voter[1:]
    return dico


votes = convert_excel_to_list("votes.xlsx")
print(votes)


candidateList = ["a", "b", "c", "d"]


def MajorityRule(votes):
    counts = {}
    for voter in votes.keys():
        vote = votes[voter]
        if vote[0] in counts.keys():
            counts[vote[0]] += 1
        else:
            counts[vote[0]] = 1
    return max(counts, key=counts.get)


print(MajorityRule(votes))


Votes = convert_excel_to_list("votes.xlsx")


def Plurality(Votes):
    candidatesScores = {}
    global_best_cand, global_best_score = False, 0
    for voter in Votes.keys():
        vote = Votes[voter]
        bestCandidate = vote[0]
        if bestCandidate in candidatesScores.keys():
            candidatesScores[bestCandidate] += 1
        else:
            candidatesScores[bestCandidate] = 1
        if candidatesScores[bestCandidate] > global_best_score:
            global_best_cand = bestCandidate
            global_best_score = candidatesScores[bestCandidate]
    return global_best_cand
    # if equality in score, the first candidate to obtain the score is elected


print("Best candidate according to Plurality: "+Plurality(Votes))


def PluralityRunoff(Votes):
    candidatesScores = {}
    for voter in Votes.keys():
        vote = Votes[voter]
        bestCandidate = vote[0]
        if bestCandidate in candidatesScores.keys():
            candidatesScores[bestCandidate] += 1
        else:
            candidatesScores[bestCandidate] = 1
    sortedCandidates = sorted(
        candidatesScores.items(), key=lambda x: x[1], reverse=True
    )
    finalists = [sortedCandidates[i][0] for i in range(2)]
    finalistsScores = {finalists[0]: 0, finalists[1]: 0}
    for voter in Votes.keys():
        vote = Votes[voter]
        for candidate in vote:
            if candidate in finalists:
                preferred = candidate
                break
        finalistsScores[preferred] += 1
    if finalistsScores[finalists[0]] > finalistsScores[finalists[1]]:
        return finalists[0]
    else:
        return finalists[1]


print("Best candidate according to Plurality Runoff: "+PluralityRunoff(Votes))


def CondorcetVoting(votes, candidateList):
    for candidate in candidateList:
        ispreferedto = {}
        count = 0
        for candidate2 in candidateList:
            if candidate != candidate2:
                for voter in votes.keys():
                    vote = votes[voter]
                    if vote.index(candidate) > vote.index(candidate2):
                        if candidate2 in ispreferedto.keys():
                            ispreferedto[candidate2] += 1
                        else:
                            ispreferedto[candidate2] = 1
                if ispreferedto[candidate2] < len(votes.keys())/2:
                    count += 1
        if count == len(candidateList)-1:
            return (candidate)
    return ("None")


print("Best candidate according to Condorcet",
      CondorcetVoting(votes, candidateList))


def BordaVoting(Votes):
    candidatesScores = {}
    for voter in Votes.keys():
        vote = Votes[voter]
        for i, candidate in enumerate(vote):
            if candidate in candidatesScores.keys():
                candidatesScores[candidate] += i+1
            else:
                candidatesScores[candidate] = i+1
    sortedCandidates = sorted(
        candidatesScores.items(), key=lambda x: x[1], reverse=False
    )
    return sortedCandidates[0][0]


print("Best candidate according to Borda: "+BordaVoting(Votes))

alphabet = ["a", "b", "c", "d", "e", 'f', "g", "h", "i", "j", "k", "l",
            "m", "n", "o", "p", "q", 'r', "s", "t", 'u', "v", "w", "x", "y", "z"]


def generateVotes(numberCandidates, numberVoters):
    candidateList = [alphabet[i] for i in range(numberCandidates)]
    votes = {}
    bestCandidate = {}
    for i in range(numberVoters):
        samePreferences = 0
        values = list(votes.values())
        preferences = [candidateList[j] for j in range(numberCandidates)]
        random.shuffle(preferences)
        if preferences in votes.values():
            samePreferences += 1
        if preferences[0] in bestCandidate.keys():
            bestCandidate[preferences[0]] += 1
        else:
            bestCandidate[preferences[0]] = 1
        while samePreferences > 0.9*numberVoters or bestCandidate[preferences[0]] > 0.7*numberVoters:
            bestCandidate[preferences[0]] -= 1
            samePreferences -= 1
            random.shuffle(preferences)
            if preferences in votes.values():
                samePreferences += 1
            if preferences[0] in bestCandidate.keys():
                bestCandidate[preferences[0]] += 1
            else:
                bestCandidate[preferences[0]] = 1

        votes["Voter " + str(i)] = preferences
    return (votes)


print(generateVotes(4, 10))


def allSameWinner():

    stop = False
    numberCandidates, numberVoters = random.randint(
        6, 12), random.randint(40, 50)
    candidateList = [alphabet[i] for i in range(numberCandidates)]
    while stop == False:
        all_same = True
        Votes = generateVotes(numberCandidates, numberVoters)
        Candidates = [Plurality(Votes), PluralityRunoff(
            Votes), CondorcetVoting(Votes, candidateList), BordaVoting(Votes)]
        if Candidates[2] == "None":
            all_same = False
        c = Candidates[0]
        for c2 in Candidates[1:]:
            if c2 != c:
                all_same = False
        if all_same == True:
            print("The winners are : ", Candidates)
            return Votes


print("Generation of a set of votes which has the same winner with the 4 different algorithms :", allSameWinner())


def differentWinners():
    stop = False
    numberCandidates, numberVoters = random.randint(
        2, 26), random.randint(40, 100)
    candidateList = [alphabet[i] for i in range(numberCandidates)]

    while stop == False:
        all_different = True
        Votes = generateVotes(numberCandidates, numberVoters)
        Candidates = [Plurality(Votes), PluralityRunoff(
            Votes), CondorcetVoting(Votes, candidateList), BordaVoting(Votes)]
        if Candidates[2] == "None":
            all_different = False
        for i, c in enumerate(Candidates[:-1]):
            if c in Candidates[i+1:]:
                all_different = False
        if all_different == True:
            print("The winners are : ", Candidates)
            return Votes


print("Generation of a set of votes which has different winners with the 4 different algorithms :", differentWinners())
