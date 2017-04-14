
import ete3

from LiteClasses import SubMatrixLite, AlnLite
from LiteSimul import simSeqOverTree


def setupLslowLeaves( N, mat, aln ):
	
	N.add_features(Lslow= [{s: int(c == s) for s in mat.stateList } for c in aln.getSpseq(N.name)] )

def setupLslowInternal( N, mat, aln ):
	#print "setupLslowInternal",N.get_leaf_names()
	resList = []
	for i in range(aln.getNbPos()):
		resList.append( {} )
		for ParentState in mat.stateList:
			#print "  ",ParentState
			resList[-1][ParentState] = 1.
			for C in N.get_children():
				#print "\t",C.get_leaf_names() , ", dist:", C.dist
				t = C.dist
				tmpRes = 0.
				for Cstate in mat.stateList:
					#print "\t\t",ParentState,"->",Cstate,":", mat.getPsubstitution(ParentState,Cstate,t),"*",C.Lslow[i][Cstate]
					tmpRes += mat.getPsubstitution(ParentState,Cstate,t) * C.Lslow[i][Cstate]
				#print "\t->",tmpRes
				resList[-1][ParentState] *= tmpRes
	N.add_features(Lslow=resList)


def setupLslowWholeTree(T,M,A):
	for N in T.traverse("postorder"):
		if N.is_leaf():
			setupLslowLeaves( N, M, A )
		else:
			setupLslowInternal( N, M, A )


def getLsRoot( R, mat ):
	Ls = 0
	for ls in R.Lslow:
		for RootState in mat.stateList:
			Ls += mat.getRootProba(RootState) * ls[RootState]
	return Ls



states = ["A","T","G","C"]
M = SubMatrixLite(states)

realT = ete3.Tree("(A:0.10,(B:0.15,(C:0.1,D:0.1):0.05):0.05);")

RootSeq= "A"*1000
SimulatedSeq = simSeqOverTree(RootSeq , realT, M)

Sp = []
Seqs = []
for k in SimulatedSeq.keys():
	print k,SimulatedSeq[k]
	Sp.append(k)
	Seqs.append(SimulatedSeq[k])

T = ete3.Tree("(A:0.1,(B:0.1,(C:0.1,D:0.1):0.1):0.1);")

#A = AlnLite(["A","B","C","D"],["A","G","G","G"])
A = AlnLite(Sp,Seqs)


#setupLslowWholeTree(realT,M,A)
#realTLkh = getLsRoot( realT, M )
#print "on real tree: ",realTLkh
#print realT.write()


print T.write()

setupLslowWholeTree(T,M,A)
currentLkh = getLsRoot( T, M )




def setupLsUp( N , M , A ):
	resList = []
	if N.is_root():
		return
	if N.up.is_root():
		for i in range(A.getNbPos()):
			resList.append( {} )
			for RootState in M.stateList:
				resList[-1][RootState] = M.getRootProba(RootState) 
				sisterNode = N.get_sisters()
				for S in sisterNode:
					tmpRes = 0.
					for SisterState in M.stateList:
						tmpRes +=  S.Lslow[i][SisterState] * M.getPsubstitution(RootState,SisterState,S.dist)
					resList[-1][RootState] *= tmpRes
					

	else:

		parentNode = N.up
		sisterNode = N.get_sisters()

		for i in range(A.getNbPos()):
			resList.append( {} )
			for state in M.stateList:
				resList[-1][state] = 1.
				tmpRes = 0.
				for ParentState in M.stateList:
					tmpRes +=  parentNode.Lsup[i][ParentState] * M.getPsubstitution(ParentState,state,parentNode.dist)
				resList[-1][state] *= tmpRes
				tmpRes = 0.
				for S in sisterNode:
					for SisterState in M.stateList:
						tmpRes +=  S.Lslow[i][SisterState] * M.getPsubstitution(state,SisterState,S.dist)
					resList[-1][state] *= tmpRes
					tmpRes = 0.
				

	N.add_features(Lsup=resList)
	return


def setupLsUpWholeTree(T,M,A):
	for N in T.traverse("preorder"):
		setupLsUp( N , M , A )


def getLsFrowAnyNode( N, mat ):

	if N.is_root():
		return getLsRoot(N,mat)

	Ls = 0
	for i in range(len(N.Lslow)):
		for State in mat.stateList:
			tmpRes = 0.
			for newState in mat.stateList:
				tmpRes += mat.getPsubstitution(State,newState, N.dist) * N.Lslow[i][newState]
			tmpRes *=N.Lsup[i][State]
			Ls += tmpRes

	return Ls



setupLsUpWholeTree(T,M,A)

print "Lkh",currentLkh

#for N in T.traverse("postorder"):
#	print N.get_leaf_names(),"\t->\t",getLsFrowAnyNode( N, M )


###L = T.get_leaves()[0]
###print L.name
###L.dist = 0.25
###
###
###print "new LS?", getLsFrowAnyNode( L, M )
###
###for n in L.iter_ancestors():
###	setupLslowInternal( n ,M,A)
###
###setupLsUpWholeTree(T,M,A)
###
###print "new LS ", getLsRoot( T, M )
###for N in T.traverse("postorder"):
###	print N.get_leaf_names(),"\t->\t",getLsFrowAnyNode( N, M )
###### shows that we need to recompute some Lslow and some Lsup as well...


Bspace = [0.0,0.01,0.05,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.99,0.999,1.0]

for N in T.traverse("postorder"):
	if not N.is_root():
		
		maxLkh = currentLkh
		maxLkhD = N.dist

		print N.get_leaf_names()

		for d in Bspace:
			N.dist = d

			newlkh = getLsFrowAnyNode( N, M )
			print " ",d, newlkh
			if newlkh > maxLkh:
				maxLkh = newlkh
				maxLkhD = d


		N.dist = maxLkhD
		## update lkh
		for n in N.iter_ancestors():
			setupLslowInternal( n ,M,A)
		
		setupLsUpWholeTree(T,M,A)

		currentLkh = maxLkh
		#print "optimized 1 branch: " , maxLkhD, "->",maxLkh

print T.write()


## compare with the result of : phyml -i test/test.aln.phi -q -m JC69 -c 1 -u test/startTree.txt -o l