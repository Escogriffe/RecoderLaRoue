
import numpy as np

class SubMatrixLite:
	def __init__(self, states):
		self.stateList = states
		self.LBDA = 1.

	def getPsubstitution(self,n1,n2,t):
		"""JC69"""
		if n1 == n2:
			return 0.25 + 0.75 * np.exp(-4 * self.LBDA *t )
		
		return 0.25 - 0.25 * np.exp(-4 * self.LBDA *t )

	def getRootProba(self,n):
		return 0.25

class SubMatrixGaltierGouy1998:
	def __init__(self , j ):
		self.stateList = ["A","T","G","C"]

		self.ancestralGC = None ## omega
		## the tree will have to ask for this parameter. or does it estimate it himself...
		self.TsTv = None ## kappa

		self.GCeq = None ##defined here for modularity but should stay at None

	def getSubstitution(self, n1 ,n2 , t , localGCequilibrium = None):
		""" Tamura 1992 with potential branch specific GCequilibrium """

		GCeq = localGCequilibrium
		if GCeq is None: ## try to use global GC instead
			GCeq = self.GCeq
		if GCeq is None: ## no GCeq
			print "!!ERROR!! this model uses branch specific or global GCequilibrium, but none was defined."
			exit(1)

		if n1 == n2:
			E1 = 1. + np.exp(-t)
			E2 = np.exp( - (self.TsTv / 2.) * t)
			if n1 in ["A","T"]:
				return (1 - GCeq) * 0.5 * E1 + GCeq * E2
			else:
				return (GCeq) * 0.5 * E1 + ( 1 - GCeq ) * E2

		elif n2 in ["A","T"]:

			if ( n1 == "G" and n2 == "A" ) or ( n1 == "C" and n2 == "T" ):
				E1 = 1. + np.exp(-t)
				E2 = np.exp( - (self.TsTv / 2.) * t)
				return (1 - GCeq) * 0.5 * E1 - ( 1 - GCeq ) * E2
			else:
				return ( 1 - GCeq ) * 0.5 * ( 1. - np.exp(-t) )

		else:

			if ( n1 == "A" and n2 == "G" ) or ( n1 == "T" and n2 == "C" ):
				E1 = 1. + np.exp(-t)
				E2 = np.exp( - (self.TsTv / 2.) * t)
				return (GCeq) * 0.5 * E1 - ( GCeq ) * E2
			else:
				return ( GCeq ) * 0.5 * ( 1. - np.exp(-t) )

		print "!!ERROR!! invalid states" , n1 , n2
		exit(1)

class AlnLite:
	def __init__(self, spList, seqList):

		self.spDict  = {s:i for i,s in enumerate(spList)}
		self.seqList = seqList

	def getNbSp(self):
		return len(self.spDict)

	def getNbPos(self):
		if len(self.seqList) == 0:
			return 0
		return len(self.seqList[0])

	def getPos(self,i):
		res = {}
		for sp,ind in self.spDict.items():
			res[sp] = self.seqList[ind][i]
		return res

	def getPosInSp(self,i,s):
		return self.seqList[self.spDict[s]][i]

	def getSpseq(self,s):
		return self.seqList[self.spDict[s]]
