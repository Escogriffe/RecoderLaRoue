

from random import randint, shuffle

totalWeight = 100

numberOfItems = 500

minWeight=1
maxWeight= totalWeight


minValue = 1
maxValue = 10

def genData(numberOfItems, minWeight , maxWeight , minValue , maxValue):
    itemWeight = [randint(minWeight , maxWeight) for i in range(numberOfItems)]
    itemValue = [randint(minValue , maxValue) for i in range(numberOfItems)]
    return itemWeight , itemValue


## dynamic programing to compute best possible value of knapsack with weight = totalWeight


def dynamicProgSolution( itemWeight, itemValue, totalWeight ):
    
    MaxValuePerWeight = [0 for i in range(totalWeight +1)]
    BagContent = [ [] for i in range(totalWeight +1)]
    
    maxIdx = 0
    
    for i in range(1,totalWeight +1):
    
        ## we want to fix M[i]
        for j in range(numberOfItems):
            if itemWeight[j] > i:
                continue ## object too big for this value
    
            if j in BagContent[i - itemWeight[j] ]:
                continue ## item has already been used 
    
            val = itemValue[j] + MaxValuePerWeight[ i - itemWeight[j] ]
            if val > MaxValuePerWeight[i]:
                MaxValuePerWeight[i] = val
                BagContent[i] = [j] + BagContent[i - itemWeight[j] ]
    
        if MaxValuePerWeight[maxIdx] < MaxValuePerWeight[i]:
            maxIdx = i

    return MaxValuePerWeight[maxIdx] , BagContent[maxIdx]


def randomSolution(itemWeight, itemValue, totalWeight , maxtry=100):
    """ randomly choose items to fill the bag """

    maxContent = []
    maxValue = 0

    nbItems = len(itemValue)

    for i in range(maxtry):
        currentContent = []
        currentValue = 0
        Weight = 0

        order = range(nbItems)
        shuffle(order)

        for j in order:
            if (Weight + itemWeight[j]) > totalWeight:
                break
            Weight += itemWeight[j]
            currentValue += itemValue[j]
            currentContent.append(j)

        if currentValue > maxValue:
            maxValue = currentValue
            maxContent = currentContent[:]

    return maxValue,maxContent


def ratioHeuristic(itemWeight, itemValue, totalWeight):

    ratios = []

    #bestSingle = 0
    #bestValueSingle = 0

    for i in range(len(itemValue)):
        ratios.append( itemValue[i]*1.  / itemWeight[i] )

        #if itemValue[i] > bestSingle and itemWeight[i]

    import numpy as np ## triche ici parce que fonction super optimisee ...

    order = np.argsort(ratios)

    bag = []
    value = 0
    weight = 0

    for i in order[::-1]:

        if weight + itemWeight[i] > totalWeight:
            break



        bag.append(i)
        value += itemValue[i]
        weight += itemWeight[i]

    return value , bag



#print "item weights : " , itemWeight
#print "item values  : " , itemValue


from time import time

TIMESDYN = []
TIMESRD = []
TIMESH = []

MAXDYN = []
MAXRD = []
MAXH = []

nbTry = 20

for i in range(nbTry):
    
    itemWeight , itemValue = genData(numberOfItems, minWeight , maxWeight , minValue , maxValue)

    t0 = time()
    
    maxVal , maxContent = dynamicProgSolution( itemWeight, itemValue, totalWeight )
    
    t1 = time()
    
    maxValRd , maxContentRd = randomSolution(itemWeight, itemValue, totalWeight , 400)
    
    t2 = time()

    maxValH , maxContentH = ratioHeuristic(itemWeight, itemValue, totalWeight)

    t3 = time()

    MAXDYN.append(maxVal)
    MAXRD.append(maxValRd)
    MAXH.append(maxValH)

    TIMESDYN.append(t1 - t0)
    TIMESRD.append(t2 - t1)
    TIMESH.append(t3 - t2)

    
print "estimated value of best knapsack with weight <= ",totalWeight," and ",numberOfItems," possible items : " 
print 'average best over',nbTry,"instances."
print "dynamic prog : ", sum(MAXDYN)/(1. * nbTry )  , "\ttime (s) :" , sum(TIMESDYN) / (1.* nbTry)
print "random try   : ", sum(MAXRD)/ (1.* nbTry) , "\ttime (s) :" , sum(TIMESRD)/ (1.* nbTry)
print "ratio heuristic:", sum(MAXH)/ (1.* nbTry) , "\ttime (s) :" , sum(TIMESH)/ (1.* nbTry)




