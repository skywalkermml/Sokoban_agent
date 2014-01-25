from Warehouse import Warehouse
from Inputhandler import Inputhandler
#from math import fabs


def heuristic1(inware):
	if not type(inware)==Warehouse:
		print "error in heuristic1, input is not a warehouse"
	newmap=inware.smap
	outboxposi=getoutboxposi(newmap)
	emptygoalposi=getemptygoalposi(newmap)
	return sumofshortestdist(outboxposi, emptygoalposi) # will destroy lists!

def heuristic2(inware):
	if not type(inware)==Warehouse:
		print "error in heuristic2, input is not a warehouse"
	newmap=inware.smap
	workerposi=inware.workerposi
	outboxposi=getoutboxposi(newmap)
	emptygoalposi=getemptygoalposi(newmap)
	return sumofshortestdist_w_worker(outboxposi, emptygoalposi, workerposi) # will destroy lists!


def getoutboxposi(inmap):
	result=[]
	for i in xrange(len(inmap)):
		for j in xrange(len(inmap[i])):
			if inmap[i][j]=="$":
				result.append((i,j))
	return result
	

def getemptygoalposi(inmap):
	result=[]
	for i in xrange(len(inmap)):
		for j in xrange(len(inmap[i])):
			if inmap[i][j]==".":
				result.append((i,j))
	return result

def sumofshortestdist(outboxposi, emptygoalposi):

	if len(outboxposi)!=0 and len(outboxposi)==len(emptygoalposi):
		boxposi=outboxposi.pop()
		
		(y,x) = emptygoalposi[0]
		st=abs(y-boxposi[0])+abs(x-boxposi[1])

		for (a,b) in emptygoalposi:
			if abs(a-boxposi[0])+abs(b-boxposi[1]) < st :
				st=abs(a-boxposi[0])+abs(b-boxposi[1])
				(y,x)=(a,b)
		emptygoalposi.remove((y,x))
		return st+sumofshortestdist(outboxposi, emptygoalposi)
	else:
		return 0



def sumofshortestdist_w_worker(outboxposi, emptygoalposi, workerposi):
	if outboxposi==[]:
		worker_boxdis=0
	else:
		worker_boxdis= sum ([ abs(a-workerposi[0])+abs(b-workerposi[1])-1 for (a,b) in outboxposi])  #must execute first
	return worker_boxdis+sumofshortestdist(outboxposi, emptygoalposi)


if __name__=="__main__":
	inputhandler=Inputhandler()
	MAP=inputhandler.filetostr("input.txt")
	warehouse=Warehouse(MAP)
	warehouse.setiniworkerposi()
	warehouse.show()
	print heuristic1(warehouse)
	print heuristic2(warehouse)

