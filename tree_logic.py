from value_arrays import value_array_5


# A_B_scores = {"A":50,"B":50}
g_index = 0
nodes = {}

# Get the index of the child
def getInd():
    global g_index
    g_index += 1 
    return g_index

# Calculate the rating of the child
def calcRating(A_score, B_score, count_1, count_3, lvl):
    turn = (lvl % 2)*2 -1
    return (A_score - B_score)*turn + count_1 - count_3

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
    rating = calcRating(A_score, B_score, count_1, count_3, lvl)

    nodes.update({ind: {'ind': ind, 'elem': selKey, 'A': A_score, 'B': B_score, 'lvl': lvl, 'rating': rating, 'childs': children}})

# Choose the best branch
def selectBranch(curr):
    global nodes
    theNode = nodes[curr]
    # print(">>>>> Enter with: " + str(curr))
    print(theNode)
    locElem = 0
    locIndex = 0
    locRating = -1
    if len(theNode['childs']) > 0:
        firstChildFlag = True
        for childInd in theNode['childs']:
            childElem, childIndex, childRating = selectBranch(childInd)
            if firstChildFlag or locRating < childRating:
                # print("    Inside " + str(theNode['ind']) + " from loc " + str(locRating)+ " to child " + str(childRating))
                firstChildFlag = False
                locElem = childElem
                locIndex = childInd
                locRating = childRating
    else:
        locElem = theNode['elem']
        locIndex = theNode['ind']
        locRating = theNode['rating']
    # print("<<<<< Exit with: " + str(theNode['ind']) + " | " + str(locElem) + " | " + str(locRating))
    return locElem, locIndex, locRating

A_score = B_score = 50


ind = getInd()

growBranch(ind, 0, value_array_5, A_score, B_score, 0)

for i in nodes:
    print(nodes[i])

print(selectBranch(1))
# print(selectBranch(2))
# print(selectBranch(3))
# print(selectBranch(4))
# print(selectBranch(262))
# print(selectBranch(311))
# print(calcRating(50, 50, 1, 2, 0))
# print(calcRating(49, 50, 0, 2, 1))
# print(calcRating(49, 49, 1, 2, 1))
# print(calcRating(50, 49, 1, 1, 1))
# 
# print(calcRating(48, 49, 0, 2, 2))
# 
# print(calcRating(47, 48, 0, 2, 3))
# print(calcRating(47, 49, 0, 1, 3))
# print(calcRating(48, 47, 0, 2, 3))
# print(calcRating(49, 47, 0, 1, 3))
# print(calcRating(48, 48, 1, 0, 3))

