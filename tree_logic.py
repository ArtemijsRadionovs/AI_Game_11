# from value_arrays import value_array_5


# A_B_scores = {"A":50,"B":50}
g_index = 0
nodes = {}

# Get the index of the child
def getInd():
    global g_index
    g_index += 1 
    return g_index

# Calculate the rating of the child
def calcRating(A_score, B_score, count_1, count_3):
    
    return A_score - B_score + count_1 - count_3

# Count the child's score
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
    

def growBranch(ind, selKey, value_array, A_score, B_score, lvl, depth = 3):
    # if depth < 1:
        # return
    global nodes
    children = []
    rating = 0
    A_or_B = lvl % 2
    if depth > 1:
        for key in value_array.keys():
            
            val = int(value_array[key])
            locA, locB = count_score(A_score, B_score, val, A_or_B)
            
            locIndex = getInd()
            children.append(locIndex)
            locArr = value_array.copy()
            locArr.pop(key)
                
            growBranch(locIndex, key, locArr, locA, locB, lvl+1, depth-1)
    # turn = A_or_B*2 -1
    # print("Rating: " + str(rating))
    # print("A: " + str(A_score), "B: " + str(B_score))
    count_1 = sum(1 for value in value_array.values() if value == 1)
    count_3 = sum(1 for value in value_array.values() if value == 3)
    rating = calcRating(A_score, B_score, count_1, count_3)

    nodes.update({ind: {'ind': ind, 'elem': selKey, 'A': A_score, 'B': B_score, 'lvl': lvl, 'rating': rating, 'childs': children}})
    
# Choose the best branch
# def selectBranch(curr):
#     global nodes
#     theNode = nodes[curr]
#     # print(">>>>> Enter with: " + str(curr))
#     # print()
#     # print(theNode)
#     locElem = 0
#     locIndex = 0
#     locRating = -1
#     if len(theNode['childs']) > 0:
#         firstChildFlag = True
#         for childInd in theNode['childs']:
#             childElem, childIndex, childRating = selectBranch(childInd)
#             if firstChildFlag or locRating < childRating:
#                 # print("    Inside " + str(theNode['ind']) + " from loc " + str(locRating)+ " to child " + str(childRating))
#                 firstChildFlag = False
#                 locElem = childElem
#                 locIndex = childInd
#                 locRating = childRating
#     else:
#         locElem = theNode['elem']
#         locIndex = theNode['ind']
#         locRating = theNode['rating']
#     # print("<<<<< Exit with: " + str(theNode['ind']) + " | " + str(locElem) + " | " + str(locRating))
    
#     return locElem, locIndex, locRating

def selectAlphaBeta(curr, alpha, beta, isMaxFlag = True):
    global nodes
    theNode = nodes[curr]
    # print(">>>>> Enter with: " + str(curr))
    # print()
    # print(theNode)
    locElem = 0
    locIndex = 0
    locRating = float('-inf')
    if len(theNode['childs']) > 0:
        firstChildFlag = True
        for childInd in theNode['childs']:
            childElem, childIndex, childRating = selectAlphaBeta(childInd, alpha, beta, not isMaxFlag)
            if firstChildFlag:
                # print("    Inside " + str(theNode['ind']) + " from loc " + str(locRating)+ " to child " + str(childRating))
                firstChildFlag = False
                locElem = childElem
                locIndex = childInd
                locRating = childRating
            else:
                if isMaxFlag:
                    if locRating < childRating: # Find max value. If yes, save.
                        locElem = childElem
                        locIndex = childInd
                        locRating = childRating
                    alpha = max(alpha, locRating)
                    if beta <= alpha:
                        # print("Pruning at: " + str(theNode['ind']))
                        # print("Alpha: " + str(alpha))
                        # print("Beta: " + str(beta))
                        break
                else:
                    if locRating > childRating: # Find min value. If yes, save.
                        locElem = childElem
                        locIndex = childInd
                        locRating = childRating
                    beta = min(beta, locRating)
                    if beta <= alpha:
                        # print("Pruning at: " + str(theNode['ind']))
                        # print("Alpha: " + str(alpha))
                        # print("Beta: " + str(beta))
                        break
    else:
        locElem = theNode['elem']
        locIndex = theNode['ind']
        locRating = theNode['rating']
    # print("<<<<< Exit with: " + str(theNode['ind']) + " | " + str(locElem) + " | " + str(locRating))
    theNode['ab_rating'] = locRating
    theNode['alpha'] = alpha
    theNode['beta'] = beta
    theNode['minF_maxT'] = isMaxFlag
    return locElem, locIndex, locRating

def selectMinMax(curr, isMaxFlag = True):
    global nodes
    theNode = nodes[curr]
    # print(">>>>> Enter with: " + str(curr))
    # print()
    # print(theNode)
    locElem = 0
    locIndex = 0
    locRating = float('-inf')
    if len(theNode['childs']) > 0:
        firstChildFlag = True
        for childInd in theNode['childs']:
            childElem, childIndex, childRating = selectMinMax(childInd, not isMaxFlag)

            if firstChildFlag:
                # print("    Inside " + str(theNode['ind']) + " from loc " + str(locRating)+ " to child " + str(childRating))
                firstChildFlag = False
                locElem = childElem
                locIndex = childInd
                locRating = childRating
            else:
                if isMaxFlag:
                    if locRating < childRating: # Find max value. If yes, save.
                        locElem = childElem
                        locIndex = childInd
                        locRating = childRating
                else:
                    if locRating > childRating: # Find min value. If yes, save.
                        locElem = childElem
                        locIndex = childInd
                        locRating = childRating
    else:
        locElem = theNode['elem']
        locIndex = theNode['ind']
        locRating = theNode['rating']
    # print("<<<<< Exit with: " + str(theNode['ind']) + " | " + str(locElem) + " | " + str(locRating))
    theNode['mm_rating'] = locRating
    theNode['minF_maxT'] = isMaxFlag
    return locElem, locIndex, locRating