
import ete3

from LiteClasses import SubMatrixLite, AlnLite

import random


def simSeq(seq, Model, t):
	""" simulates the evolution of sequence <seq> over time <t> according to model <Model> """
	SubProbas = {}
	for ParentState in Model.stateList:
		SubProbas[ParentState] = []
		for ChildState in Model.stateList:
			SubProbas[ParentState].append( Model.getPsubstitution(ParentState,ChildState,t) )

	newSeq = ""
	for n in seq:
		r = random.random()
		for i,p in enumerate(SubProbas[n]):
			if r <= p :
				newSeq += Model.stateList[i]
				break
			else:
				r -= p
	return newSeq

	


def simSeqOverTree(rootSeq, Tree, Model):
	Tree.add_features(seq=rootSeq)
	
	for N in Tree.traverse("preorder"):
		if N.is_root():
			continue
		N.add_features(seq=simSeq( N.up.seq , Model , N.dist))

	dseq = {}
	for L in Tree.iter_leaves():
		dseq[L.name] = L.seq
	return dseq

if __name__ == "__main__":
	states = ["A","T","G","C"]
	SP = ["A","B","C","D"]
	T = ete3.Tree("(A:0.2,(B:0.1,(C:0.05,D:0.05):0.05):0.1);")
	M = SubMatrixLite(states)
	
	RootSeq= "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
	print simSeqOverTree(RootSeq , T,M)