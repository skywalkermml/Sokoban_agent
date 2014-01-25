# then print statistics
import sys
import tree
from collections import deque
from Warehouse import Warehouse
from Inputhandler import Inputhandler
from tree import tree, node
import time
import heapq

class UCS(object): # do UCS
	def __init__(self, root):
		self.explored=set()
		self.frontier=[]
		heapq.heappush(self.frontier, (0, root) )  # push the root to frontier. cost of root =0
		self.searchtree=tree(root)
		self.numofnodegenbefore=0
		#self.numofnodeonfringe=1



	def search(self):
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
			 	[newstate, pathcost]=parentnode.content.move(action,"UCS")

			 	if not newstate=="ILLEGAL_MOVE": #exclude illegal move:
			 		child=self.searchtree.addandreturnnode(parentnode, newstate, action)
			 		child.cost= parentnode.cost+pathcost
			 		
			 		infrontierposi=self.infrontierposition(child)  #calculate only once
			 		if  not self.inexplored(child) and infrontierposi==-1:  # not in frontier nor expolred
				 		heapq.heappush(self.frontier,(child.cost,child))	
				 	elif not infrontierposi==-1:
				 		if child.cost<self.frontier[infrontierposi][0]:
				 			self.frontier[infrontierposi]=(child.cost,child)
				 			heapq.heapify(self.frontier)
				 		self.numofnodegenbefore+=1  # assume update in frontier also count as gen before!!!
				 	else:  # in explored
				 		self.numofnodegenbefore+=1 
		
		


	def infrontierposition(self, thenode):  # return -1 if not in frontier
		for i in xrange(len(self.frontier)):
			if self.frontier[i][1].content==thenode.content:
				return i
		return -1

	def inexplored(self, thenode):
		for element in self.explored:
			if element.content==thenode.content:
				return 1
		return 0


if __name__=="__main__":
	inputhandler=Inputhandler()
	MAP=inputhandler.filetostr("30s.txt")
	warehouse=Warehouse(MAP)
	warehouse.setiniworkerposi()
	warehouse.show()

	root=node(warehouse)
	root.cost=0
	ucs=UCS(root)
	print(ucs.search())