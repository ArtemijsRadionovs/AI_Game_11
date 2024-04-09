# Globalie mainīgie g_index un nodes tiek izmantoti, lai uzglabātu informāciju par koku un tā zaru indeksiem.
g_index = 0
nodes = {}

# Funkcija getInd() tiek izmantota, lai dabūtu nākamo pēcteča indeksu.
def getInd():
    global g_index
    g_index += 1 
    return g_index

# Saskaitīt pēcteču heiristisku novērtējumu, izmantojot heiristisku funkciju.
# Heiristiskā funkcijai ir definēti parametri, kas tiek izmantoti, lai aprēķinātu pēcteču vērtējumu.
# Tie ir A_score - spēlētāja A punkti, B_score - spēlētāja B punkti, count_1 - vieninieku skaits un count_3 - trijnieku skaits.
def calcRating(A_score, B_score, count_1, count_3):
    
    return A_score - B_score + count_1 - count_3

# Funkcija, kas saskaitā pēcteču rezultātu.
# Attiecīgi spēles noteikumiem: 
# Ja tiek izvēlēts 1, tad punkti tiek atņemti no tā spēlētāja, kurš izvēlējās šo skaitli.
# Ja tiek izvēlēts 2, tad 1 punkts tiek atņemts no abiem spēlētājiem.
# Ja tiek izvēlēts 3, tad 1 punkts tiek atņemts no pretējā spēlētāja.
def count_score(A_score, B_score, val, A_or_B):
    locA = A_score
    locB = B_score
    match val:
        case 1:
            if A_or_B == 0:
                locA -= 1
            else:
                locB -= 1
        case 2:
            locA -= 1
            locB -= 1
        case 3:
            if A_or_B == 0:
                locB -= 1
            else:
                locA -= 1
    return locA, locB
    
# Funkcija, kas uzcel koku ar visiem iespējamajiem gājieniem līdz noteiktam dziļumam -> depth = 3
# Funkcija izmanto rekursiju, lai izveidotu koku ar visiem iespējamajiem gājieniem.
def growBranch(ind, selKey, value_array, A_score, B_score, lvl, depth = 3):

    global nodes
    children = [] # Pēcteču masīvs
    rating = 0 
    A_or_B = lvl % 2
    if depth > 1:
        for key in value_array.keys():
            
            val = int(value_array[key])
            locA, locB = count_score(A_score, B_score, val, A_or_B) # Saskaitīt spēlētāju teoretisko rezultātu koka virsotnē
            
            locIndex = getInd() # Dabūt nākamo pēcteča indeksu
            children.append(locIndex) # Saglabāt pēcteča indeksu
            locArr = value_array.copy() # Kopēt vērtību masīvu, lai izvairītos no datu zuduma
            locArr.pop(key) # Izņemt izvēlēto elementu no kopētā masīva
            # Rekursīvi izsauc funkciju, lai tiktu līdz dziļumam depth = 3 
            growBranch(locIndex, key, locArr, locA, locB, lvl+1, depth-1)

    # Tiek skaitīti vieninieku un trijnieku skaits
    count_1 = sum(1 for value in value_array.values() if value == 1)
    count_3 = sum(1 for value in value_array.values() if value == 3)

    # Tiek aprēķināts zara vērtējums
    rating = calcRating(A_score, B_score, count_1, count_3)

    # Tiek izveidots koka elements, kurš satur informāciju par šo zaru.
    nodes.update({ind: {'ind': ind, 'elem': selKey, 'A': A_score, 'B': B_score, 'lvl': lvl, 'rating': rating, 'childs': children}})

# Izvēlēties labāko gājienu, izmantojot alfa-beta algoritmu
# Alfa-beta algoritms ir minimax algoritma uzlabota versija, kas ļauj veikt zaru apgriešanu, ja zināms, ka tā vērtība neietekmē galīgo rezultātu.
def selectAlphaBeta(curr, alpha, beta, isMaxFlag = True):
    global nodes
    theNode = nodes[curr]
    # print(">>>>> Enter with: " + str(curr))
    # print()
    # print(theNode)
    locElem = 0 # Lokālais elements
    locIndex = 0 # Lokālais indekss
    locRating = float('-inf')  # Lokālais heiristisks novērtējums
    if len(theNode['childs']) > 0:
        firstChildFlag = True
        for childInd in theNode['childs']:
            childElem, childIndex, childRating = selectAlphaBeta(childInd, alpha, beta, not isMaxFlag) # Rekursīvi izsauc funkciju, lai atrastu labāko gājienu
            if firstChildFlag:
                # print("    Inside " + str(theNode['ind']) + " from loc " + str(locRating)+ " to child " + str(childRating))
                firstChildFlag = False
                # Tiek saglabāts pirmais pēcteča elements, indekss un novērtējums
                locElem = childElem 
                locIndex = childInd
                locRating = childRating
            else:
                if isMaxFlag:
                    if locRating < childRating: # Atrast max vertibu. Ja ir, saglabāt.
                        locElem = childElem 
                        locIndex = childInd
                        locRating = childRating
                    alpha = max(alpha, locRating) # Saglabāt lielāko alfa vērtību
                    if beta <= alpha: # Ja beta ir mazāks vai vienāds ar alfa, tad pārtraukt rekursiju jeb apgriezt zaru
                        # print("Pruning at: " + str(theNode['ind']))
                        # print("Alpha: " + str(alpha))
                        # print("Beta: " + str(beta))
                        break
                else:
                    if locRating > childRating: # Atrast min vertibu. Ja ir, saglabāt.
                        locElem = childElem
                        locIndex = childInd
                        locRating = childRating
                    beta = min(beta, locRating) # Saglabāt mazāko beta vērtību
                    if beta <= alpha: # Ja beta ir mazāks vai vienāds ar alfa, tad pārtraukt rekursiju jeb apgriezt zaru
                        # print("Pruning at: " + str(theNode['ind']))
                        # print("Alpha: " + str(alpha))
                        # print("Beta: " + str(beta))
                        break
    else:
        locElem = theNode['elem'] # Ja nav pēcteču, tad saglabāt pašreizējo elementu
        locIndex = theNode['ind'] # Saglabāt pašreizējo indeksu
        locRating = theNode['rating'] # Saglabāt pašreizējo novērtējumu
    # print("<<<<< Exit with: " + str(theNode['ind']) + " | " + str(locElem) + " | " + str(locRating))
    theNode['ab_rating'] = locRating # Saglabāt alfa-beta novērtējumu
    theNode['alpha'] = alpha # Saglabāt alfa vērtību
    theNode['beta'] = beta # Saglabāt beta vērtību
    theNode['minF_maxT'] = isMaxFlag # Saglabāt minimizētāja vai maksimizētāja flagu
    return locElem, locIndex, locRating

# Izvēlēties labāko gājienu, izmantojot minimax algoritmu
# Minimax algoritms ir algoritms, kas izmanto rekursīvu pieeju, lai izvēlētos labāko gājienu katrā spēles stāvoklī.
# Algoritms darbojas, izmantojot divus galvenos principus: maksimizētājs maksimizē cenšās atrast maksimālo vērtību un minimizētājs cenšās atrast minimālo vērtību.
def selectMinMax(curr, isMaxFlag = True):
    global nodes
    theNode = nodes[curr] # Koku elementa izvēle
    # print(">>>>> Enter with: " + str(curr))
    # print()
    # print(theNode)
    locElem = 0 # Lokālais elements
    locIndex = 0 # Lokālais indekss
    locRating = float('-inf')  # Lokālais heiristisks novērtējums
    if len(theNode['childs']) > 0:
        firstChildFlag = True 
        for childInd in theNode['childs']:
            childElem, childIndex, childRating = selectMinMax(childInd, not isMaxFlag) # Rekursīvi izsauc funkciju, lai atrastu labāko gājienu
            
            # Tiek saglabāts pirmais pēcteča elements, indekss un novērtējums
            if firstChildFlag: 
                # print("    Inside " + str(theNode['ind']) + " from loc " + str(locRating)+ " to child " + str(childRating))
                firstChildFlag = False
                locElem = childElem
                locIndex = childInd
                locRating = childRating
            else:
                if isMaxFlag:
                    if locRating < childRating: # Atrast max vertibu. Ja ir, saglabāt.
                        locElem = childElem
                        locIndex = childInd
                        locRating = childRating
                else:
                    if locRating > childRating: # Atrast min vertibu. Ja ir, saglabāt.
                        locElem = childElem
                        locIndex = childInd
                        locRating = childRating
    else:
        locElem = theNode['elem'] # Ja nav pēcteču, tad saglabāt pašreizējo elementu
        locIndex = theNode['ind'] # Saglabāt pašreizējo indeksu
        locRating = theNode['rating'] # Saglabāt pašreizējo novērtējumu
    # print("<<<<< Exit with: " + str(theNode['ind']) + " | " + str(locElem) + " | " + str(locRating))
    theNode['mm_rating'] = locRating # Saglabāt minimax novērtējumu
    theNode['minF_maxT'] = isMaxFlag # Saglabāt minimizētāja vai maksimizētāja flagu
    return locElem, locIndex, locRating
