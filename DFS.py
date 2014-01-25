#Author : Joshua Wang. Date 10/24 2013
import sys
import tree
from collections import deque
from Warehouse import Warehouse
from Inputhandler import Inputhandler
from tree import tree, node
import time
import copy

class DFS(object): # do DFS
	def __init__(self, root):
		self.explored=set()
		self.frontier=deque()  # use deque to implement stack
		self.frontier.append(root)
		self.searchtree=tree(root)
		self.numofnodegenbefore=0
		self.numofnodeonfringe=1



	def search(self):
		start=time.time()
		while (1):
		 if len(self.frontier)==0:
		 	finish=time.time()  # then print statistics 
			print("number of nodes generated: "+str(self.searchtree.getnumofnodes()))
			print("number of nodes containing generated states: "+str(self.numofnodegenbefore))
			print("number of nodes on the fringe: "+str(len(self.frontier)))
			print("number of nodes in the explored list: "+str(len(self.explored)))
			print("run time: "+str(finish-start))
		 	return "failure"
		 parentnode= self.frontier.pop()
		 self.explored.add(parentnode)

		 for action in ["u", "l", "d", "r"]:  # scrumble actions to prevent loops (actually no need in graph search)
		 	newstate=parentnode.content.move(action)[0]
		 	if not newstate=="ILLEGAL_MOVE": #exclude illegal move:
		 		child=self.searchtree.addandreturnnode(parentnode, newstate, action)
		 		if  not self.inexplored(child) and not self.infrontier(child): # use graph search
			 		if newstate.allgoalremoved:
			 			finish=time.time() # then print statistics
			 			print("number of nodes generated: "+str(self.searchtree.getnumofnodes()))
						print("number of nodes containing states generated before: "+str(self.numofnodegenbefore))
						print("number of nodes on the fringe: "+str(len(self.frontier)))
						print("number of nodes in the explored list: "+str(len(self.explored)))
						print("run time: "+str(finish-start))
			 			return child.path
			 		self.frontier.append(child) 
			 	else:  # in explored ot frontier
			 		self.numofnodegenbefore+=1 
		
		


	def infrontier(self, thenode):
		for element in self.frontier:
			if element.content==thenode.content:
				return 1
		return 0

	def inexplored(self, thenode):
		for element in self.explored:
			if element.content==thenode.content:
				return 1
		return 0


# if __name__=="__main__":
# 	inputhandler=Inputhandler()
# 	MAP=inputhandler.filetostr("big.txt")
# 	warehouse=Warehouse(MAP)
# 	warehouse.setiniworkerposi()
# 	warehouse.show()

# 	root=node(warehouse)
# 	dfs=DFS(root)
# 	print(dfs.search())