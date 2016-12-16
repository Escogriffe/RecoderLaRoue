
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
