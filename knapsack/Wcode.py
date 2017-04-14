

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

M = [0 for i in range(totalWeight +1)]

for i in range(1,totalWeight +1):

    ## we want to fix M[i]
    for j in range(numberOfItems):
        if itemWeight[j] > i:
            continue ## object too big for this value

        val = itemValue[j] + M[ i - itemWeight[j] ]
        if val > M[i]:
            M[i] = val

print "estimated weight of best knapsack with weight <= ",totalWeight," : " , max(M)