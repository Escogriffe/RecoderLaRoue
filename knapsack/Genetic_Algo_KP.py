'''
Genetic algorithm for heuristic solution to knapsack problem
Written by Brice

List of possible constraints:
-List of objects should not be empty (Nb_Objects>0)
-Max object weight should not exceed the total weight constraint.
-Object weight should not be zero

List of effective constraints:
-An empty knapsack is not a solution. As a consequence, an individual cannot have a genotype of all 0's.

Parameters are passed to Object_set constructor: nb_objects, weight ranges, value ranges, knapsack weight constraint.
'''

from random import randint,uniform
import numpy,operator #Numpy only used for tests.

class Object_set(object):
	'''
	Generates objects with values and weights, stores data parameters
	'''
	def __init__(self,Nb_Objects,min_w,max_w,min_v,max_v,weight_constraint,mutation_rate):
		if max_w>weight_constraint:
			print("You gave a max weight superior to the weight constraint("+str(weight_constraint)+"), this can generate objects too heavy to put in knapsack.")
			print("Running with max weight="+str(weight_constraint)+" instead.")
			self.max_w=weight_constraint
		else:
			self.max_w=max_w
		self.weight_constraint=weight_constraint
		self.Nb_Objects=Nb_Objects
		self.min_w=min_w
		self.object_weights=[randint(min_w,max_w) for i in range(Nb_Objects)]
		#self.object_weights=[4, 10, 1, 5, 8, 6, 1, 1, 10, 4, 2, 5, 4, 8, 4, 10, 5, 4, 1, 10, 8, 6, 1, 1, 6, 9, 6, 6, 8, 3]
		self.object_values=[randint(min_v,max_v) for i in range(Nb_Objects)]
		#self.object_values=[7, 8, 9, 1, 3, 8, 4, 5, 4, 7, 1, 10, 7, 8, 6, 10, 10, 6, 5, 7, 1, 6, 2, 8, 6, 2, 5, 5, 3, 7]
		self.mutation_rate=mutation_rate


class Solution_Indiv(object):
	'''
	One individual, ie a genotype of bits representing object presence/absence, along with weight and value.
	The weight of a Solution_Indiv can never exceed that of the constraint (max authorised) weight
	'''
	def __init__(self,weight,genes,Object_set):
		'''
		genes is a list of genes (bits)
		'''
		self.weight=weight
		self.genes=genes
		self.value=Solution_Indiv.get_value(genes,Object_set.object_values,Object_set.Nb_Objects)
	@staticmethod
	def get_value(genes,object_values,Nb_Objects):
		return sum([object_values[i] for i in range(Nb_Objects) if genes[i]==1])

def weighted_choice(candidates,prob_distrib):

	'''
	Chooses an element in candidates list based on prob distribution of candidates (list of weights of each candidate)
	Inspired from http://stackoverflow.com/questions/3679694/a-weighted-version-of-random-choice?noredirect=1&lq=1
	Candidates and prob_distrib lists need to be in the same order.

	'''
	total = sum(w for w in prob_distrib)  #If sum of weights is not 1
	r = uniform(0, total)
	upto = 0
	for i in range(len(candidates)):
		c,w=candidates[i],prob_distrib[i]
		upto+=w
		if upto>=r:
			return c

def cross(ind_1,ind_2,O):
	'''
	Attempts to shuffle two genotypes (analogous to progeny generation)
	If a shuffled solution cannot be generated quickly, returns the two parent individuals
	'''
	breakpoint_list=[i for i in range(1,Nb_Objects-1)]  #"-1" to guarantee true crossover
	breakpoint=breakpoint_list[randint(0,len(breakpoint_list)-1)]
	breakpoint_list.remove(breakpoint) #Guarantee you don't try to crossover at same points
	genes1=ind_1.genes[:breakpoint]+ind_2.genes[breakpoint:]
	genes2=ind_2.genes[:breakpoint]+ind_1.genes[breakpoint:]
	weight1=sum([O.object_weights[i] for i in range(O.Nb_Objects) if genes1[i]==1])
	weight2=sum([O.object_weights[i] for i in range(O.Nb_Objects) if genes2[i]==1])
	trial=1
	while weight1>O.weight_constraint or weight2>O.weight_constraint:
		if trial<30 and breakpoint_list: #If breakpoint_list still has elements
			trial+=1
			breakpoint=breakpoint_list[randint(0,len(breakpoint_list)-1)]
			breakpoint_list.remove(breakpoint)			
			genes1=ind_1.genes[:breakpoint]+ind_2.genes[breakpoint:]
			genes2=ind_2.genes[:breakpoint]+ind_1.genes[breakpoint:]
			weight1=sum([O.object_weights[i] for i in range(O.Nb_Objects) if genes1[i]==1])
			weight2=sum([O.object_weights[i] for i in range(O.Nb_Objects) if genes2[i]==1])
		else:
			return [ind_1,ind_2]
	return [Solution_Indiv(weight1,genes1,O),Solution_Indiv(weight2,genes2,O)]

def sample(choice_density,O):
	sol_weight=float('inf')
	while sol_weight>O.weight_constraint:
		genes=[weighted_choice([0,1],choice_density) for i in range(O.Nb_Objects)] #Bitwise random insertion of objects into knapsack = one individual
		if sum(genes)==0:
			continue #Empty knapsack generated, not an acceptable solution.
		sol_weight=sum([O.object_weights[i] for i in range(O.Nb_Objects) if genes[i]==1])
	return Solution_Indiv(sol_weight,genes,O)


def intervert_mutate(ind,O):
	'''
	1 object loss <=> 1 object with same or lesser weight added. 2 mutations at every call to function.
	Does not use parameter mutation rate.
	'''
	idx_list=[i for i in range(Nb_Objects)]
	ng=[i for i in ind.genes]
	pres=2
	while pres!=1:
		idx_p=idx_list[randint(0,len(idx_list)-1)]
		idx_list.remove(idx_p)
		pres=ng[idx_p]
	weight_p=O.object_weights[idx_p]
	abss=2;weight_a=weight_p+1
	idx_list=[i for i in range(Nb_Objects) if i!=idx_p] #Take all possible indices again, without the p index
	while abss!=0 or weight_a>weight_p: #Need both conditions to False to break out of loop
		if idx_list:
			idx_a=idx_list[randint(0,len(idx_list)-1)]
			idx_list.remove(idx_a)
			abss=ng[idx_a]
			weight_a=O.object_weights[idx_a]
		else:
			return ind #Could not mutate.
	ng[idx_p]=0;ng[idx_a]=1
	weight=sum([O.object_weights[i] for i in range(O.Nb_Objects) if ng[i]==1])
	return Solution_Indiv(weight,ng,O)

def frequency_mutate(ind,O):
	'''
	Not a good way to mutate; uses parameter mutation rate
	'''
	weight=float('inf')
	no=0
	while weight > O.weight_constraint:
		mut=0
		no+=1
		ng=[i for i in ind.genes]
		for i in range(O.Nb_Objects):
			if uniform(0,1)<=O.mutation_rate:
				ng[i]=1-ind.genes[i] #Mutate 0->1 and 1->0
				mut+=1
		if mut==0 and O.mutation_rate>0:
			continue
		weight=sum([O.object_weights[i] for i in range(O.Nb_Objects) if ng[i]==1])
	#print(ind.weight,weight,ng,ind.genes);exit(1)
	#print(no)
	return Solution_Indiv(weight,ind.genes,O)

def Evolve(O,nb_generations):

	###Create population of solutions (=genotypes compatible with weight constraint)
	solution_pop=[]
	weighting_factor=O.Nb_Objects*((O.max_w+O.min_w)//2)/O.weight_constraint
	choice_density=[weighting_factor,1] #Determine over or under-sampling of 1's relative to 0's for solution population generation.

	while len(solution_pop)!=O.Nb_Objects*(O.max_w-O.min_w) and len(solution_pop)!=1000: #Fix max pop size to 1000
		solution_pop.append(sample(choice_density,O))
	###

	iter=0
	while iter<nb_generations:
		iter+=1
		pr=solution_pop[0].value
		solution_pop.sort(key=operator.attrgetter('value'),reverse=True) #Sort individuals by descending value. Operator more low-level than lambda: http://stackoverflow.com/questions/403421/how-to-sort-a-list-of-objects-based-on-an-attribute-of-the-objects
		#print(solution_pop[-1].value);print(numpy.var([i.value for i in solution_pop])) #Test output logs
		#print(numpy.mean([i.value for i in solution_pop]))
		ma=solution_pop[0].value
		if iter>1:
			if ma>pr:
				ma=solution_pop[0].value
				pr=ma
				print("Better found, generation",str(iter),"value",ma) #Log solution quality increase
		elite_number=int(0.1*len(solution_pop))
		new_pop=solution_pop[:elite_number] #Keep ~50% best individuals at worst (cap pop_size list=100)
		s=sum([i.value for i in solution_pop])
		weights=[round(i.value/s,3) for i in solution_pop]
		#solution_pop=mutate(solution_pop,O)
		while len(new_pop)<len(solution_pop):
				ind_1=weighted_choice(solution_pop,weights) #Weighted choice: choose each individual proportionally to his genotype's value.
				#ind_1alt=solution_pop[randint(0,len(solution_pop)-1)] #Uniform sampling
				ind_2=weighted_choice(solution_pop,weights) #Can get the same individual twice at this point.
				#ind_1=mutate(ind_1,O)
				ind_2=intervert_mutate(ind_2,O)
				#ind_2alt=solution_pop[randint(0,len(solution_pop)-1)]
				new_pop+=cross(ind_1,ind_2,O) #Pass Object_set instance as parameter to cross function
		solution_pop=new_pop
	solution_pop.sort(key=operator.attrgetter('value'),reverse=True)
	return solution_pop[0]

	'''
	Test prints
	'''
	#print(numpy.mean([i.value for i in solution_pop]));print(numpy.mean([i.value for i in new_pop]));exit(1)
	#print(max([i.value for i in solution_pop]),max([i.value for i in new_pop]));exit(1)
Nb_Objects=100
nb_generations=100
O=Object_set(Nb_Objects=Nb_Objects,min_w=1,max_w=100,min_v=1,max_v=10,weight_constraint=2000,mutation_rate=0.15)
print("Object set weights:",O.object_weights)
print("Object set values:",O.object_values)
print("Weight constraint",str(O.weight_constraint),"\n")
best=Evolve(O,nb_generations)
print("Best object combination found: objects [",",".join([str(i) for i in range(O.Nb_Objects) if best.genes[i]==1]),"] (0-based index)","value",best.value,"weight",best.weight)
#print(len([i for i in range(O.Nb_Objects) if best.genes[i]==1]))
