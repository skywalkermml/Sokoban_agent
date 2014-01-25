import sys
import tree
from collections import deque
from Warehouse import Warehouse
from Inputhandler import Inputhandler
from tree import tree, node
import time
import heapq
from heuristics import heuristic1,heuristic2

class GreedyBFS(object):  # similar to UCS
	def __init__(self, root, heuris=1):
		self.explored=set()
		self.frontier=[]

		if heuris==1:
			root.expectcost=heuristic1(root.content)
		else:
			root.expectcost=heuristic2(root.content)

		heapq.heappush(self.frontier, (root.expectcost, root) )
		self.searchtree=tree(root)
		self.numofnodegenbefore=0
		#self.numofnodeonfringe=1
		#print(heuristic1(root.content))



	def search(self, heuris=1):
		if heuris == 1:       #  separate different cases
			def heuristic(s): return heuristic1(s) 
		elif heuris ==2:
			def heuristic(s): return heuristic2(s) 

		start=time.time()
		while (1):
			if len(self.frontier)==0:
		 		finish=time.time()
				print("number of nodes generated: "+str(self.searchtree.getnumofnodes()))
				print("number of nodes containing generated states: "+str(self.numofnodegenbefore))
				print("number of nodes on the fringe: "+str(len(self.frontier)))
				print("number of nodes in the explored list: "+str(len(self.explored)))
				print("run time: "+str(finish-start))
			 	return "failure"
			
			parentnode=heapq.heappop(self.frontier)[1]

			if parentnode.content.allgoalremoved:
				finish=time.time()
				print("number of nodes generated: "+str(self.searchtree.getnumofnodes()))
				print("number of nodes containing states generated before: "+str(self.numofnodegenbefore))
				print("number of nodes on the fringe: "+str(len(self.frontier)))
				print("number of nodes in the explored list: "+str(len(self.explored)))
				print("run time: "+str(finish-start))
				return parentnode.path
			 

			self.explored.add(parentnode)

			for action in ["u", "d", "l", "r"]:
			 	newstate=parentnode.content.move(action)[0]


			 	if not newstate=="ILLEGAL_MOVE": #exclude illegal move:
			 		child=self.searchtree.addandreturnnode(parentnode, newstate, action)
			 		child.expectcost= heuristic(child.content)


			 		
			 		infrontierposi=self.infrontierposition(child)  #calculate only once
			 		if  not self.inexplored(child) and infrontierposi==-1:  # not in frontier nor expolred
				 		heapq.heappush(self.frontier,(child.expectcost,child))	
				 	elif not infrontierposi==-1:  # in frontier
				 		if child.expectcost<self.frontier[infrontierposi][0]: 
				 			self.frontier[infrontierposi]=(child.expectcost,child)  # reset value
				 			heapq.heapify(self.frontier) # re heapify
				 		self.numofnodegenbefore+=1  # assume update in frontier also count as gen before!!!
				 	else:  # in explored
				 		self.numofnodegenbefore+=1 
		
		


	def infrontierposition(self, thenode):
		for i in xrange(len(self.frontier)):
			if self.frontier[i][1].content==thenode.content:
				return i
		return -1

	def inexplored(self, thenode):
		for element in self.explored:
			if element.content==thenode.content:
				return 1
		return 0

# previous test case
# if __name__=="__main__":
# 	inputhandler=Inputhandler()
# 	MAP=inputhandler.filetostr("med.txt")
# 	warehouse=Warehouse(MAP)
# 	warehouse.setiniworkerposi()
# 	warehouse.show()

# 	root=node(warehouse)
# 	root.expectcost=0
# 	gbfs=GreedyBFS(root)
# 	print(gbfs.search())