

from random import randint

totalWeight = 10

numberOfItems = 3

minWeight=1
maxWeight= totalWeight


minValue = 1
maxValue = 10


itemWeight = [randint(minWeight , maxWeight) for i in range(numberOfItems)]
itemValue = [randint(minValue , maxValue) for i in range(numberOfItems)]

print "item weights : " , itemWeight
print "item values  : " , itemValue


## dynamic programing to compute best possible value of knapsack with weight = totalWeight

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



print "estimated weight of best knapsack with weight <= ",totalWeight," : " , MaxValuePerWeight[maxIdx] , BagContent[maxIdx]