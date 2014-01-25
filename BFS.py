#Author : Joshua Wang. Date 10/24 2013
import sys
import tree
from collections import deque
from Warehouse import Warehouse
from Inputhandler import Inputhandler
from tree import tree, node
import time
import copy

class BFS(object):  # do BFS
	def __init__(self, root):
		self.explored=set()  # explored set
		self.frontier=deque()  # use deque for fast poping and checking there is same value
		
		self.frontier.append(root)
		self.searchtree=tree(root)
		
		self.numofnodegenbefore=0  # record the the num of nodes seen before
		self.numofnodeonfringe=1 # currently not used



	def search(self):
		start=time.time() # set start time
		while (1):
		 if len(self.frontier)==0:
		 	finish=time.time() # print statistics results
			print("number of nodes generated: "+str(self.searchtree.getnumofnodes())) 
			print("number of nodes containing generated states: "+str(self.numofnodegenbefore))
			print("number of nodes on the fringe: "+str(len(self.frontier)))
			print("number of nodes in the explored list: "+str(len(self.explored)))
			print("run time: "+str(finish-start))
		 	return "failure"
		 parentnode= self.frontier.popleft()  # so ti will be FILO
		 self.explored.add(parentnode)

		 for action in ["u", "d", "l", "r"]:
		 	newstate=parentnode.content.move(action)[0]  #only thr state is required
		 	if not newstate=="ILLEGAL_MOVE": #exclude illegal move:
		 		child=self.searchtree.addandreturnnode(parentnode, newstate, action)
		 		if  not self.inexplored(child) and not self.infrontier(child): # check if it is in frontier and explored
			 		if newstate.allgoalremoved:
			 			finish=time.time()
			 			print("number of nodes generated: "+str(self.searchtree.getnumofnodes()))
						print("number of nodes containing states generated before: "+str(self.numofnodegenbefore))
						print("number of nodes on the fringe: "+str(len(self.frontier)))
						print("number of nodes in the explored list: "+str(len(self.explored)))
						print("run time: "+str(finish-start))
			 			return child.path
			 		self.frontier.append(child) 
			 	else:  # in explored ot frontier
			 		self.numofnodegenbefore+=1 
		
		


	def infrontier(self, thenode):  # check if is in frontier
		for element in self.frontier:
			if element.content==thenode.content:
				return 1
		return 0

	def inexplored(self, thenode):  # check if is in explored
		for element in self.explored:
			if element.content==thenode.content:
				return 1
		return 0

# previous test case
# if __name__=="__main__":
# 	inputhandler=Inputhandler()
# 	MAP=inputhandler.filetostr("3s.txt")
# 	warehouse=Warehouse(MAP)
# 	warehouse.setiniworkerposi()
# 	warehouse.show()

# 	root=node(warehouse)
# 	bfs=BFS(root)
# 	print(bfs.search())

