#Author : Joshua Wang. Date 10/24 2013
import sys
import tree
from Warehouse import Warehouse
from Inputhandler import Inputhandler
from BFS import BFS
from DFS import DFS
from UCS import UCS
from UCS import UCS
from GreedyBFS import GreedyBFS
from A_star import A_star
from tree import tree, node
from A_star import A_star
import os


def showmove(ori, move):  # show the move step by step
	temp=ori
	temp.show()
	for i in move: 
		temp=temp.move(i)[0]
		if type(temp)  == str:
			print temp
		else :
			temp.show()
	

if __name__=="__main__":

	MAP=[]
	if len(sys.argv)!=2: # Expect exactly one argument: the inputfile
		print("ERROR: Expect one input docuemnt")  
		sys.exit(2)

	else:
		try:
			inputhandler=Inputhandler()
			MAP=inputhandler.filetostr(sys.argv[1])
		except IOError:
			sys.stderr.write("ERROR: Cannot read inputfile\n")
			sys.exit(1)
	# this section of inputing files is referred from the codes provided in NLP course, Columbia University, COMS 4705 2013


	inputhandler=Inputhandler()
	
	warehouse=Warehouse(MAP)
	warehouse.setiniworkerposi()

	print ("The configuration of the input:") 
	warehouse.show()

	root=node(warehouse)  # load to the tree
			
	instr=""
	solution=""
	while(1):
		print("\nplease choose the searching method:\nb :BFS\nd :DFS\nu :UCS")
		print("g_1 :Greedy best first search (heuristic 1)") 
		print("g_2 :Greedy best first search (heuristic 2)")
		print("a_1 :A* search (heuristic 1)")
		print("a_2 :A* search (heuristic 2)")
		print("Others :quit")
     
		instr=raw_input(":")
		if instr=="b":
			bfs=BFS(root)
			solution=bfs.search()
		elif instr=="d":
			dfs=DFS(root)
			solution=dfs.search()
		elif instr=="u":
			ucs=UCS(root)
			solution=ucs.search()
		elif instr=="g_1":
			gbfs=GreedyBFS(root,1)  # initialize with heuristic 1
			solution=gbfs.search()
		elif instr=="g_2":
			gbfs=GreedyBFS(root,2)  # initialize with heuristic 2
			solution=gbfs.search(2)
		elif instr=="a_1":
			a_star=A_star(root,1)
			solution=a_star.search()
		elif instr=="a_2":
			a_star=A_star(root,2)
			solution=a_star.search(2)
		else:
			break  # break the loop, will not go down

		print("movement solution:")
		print(solution)

		showstep=raw_input("show solution step by step (y= yes) ?")	  # show whether print the output solution
		if showstep=="y":
			showmove(root.content, solution)
