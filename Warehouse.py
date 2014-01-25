#Author:Joshua Wang, date :10/24 2013 

from Inputhandler import Inputhandler
import sys
import copy

class Warehouse(object):  # the object of the states of nodes
	def __init__(self, inMAP):
		self.smap=copy.deepcopy(inMAP) #self-map. represent the configuation of the warehouse
		self.workerposi=[None,None]  # locate workerposi outside the class
		#self.workerposi.append(self.iniworkerposi())
		self.allgoalremoved=0
		if not self.islegal():
			print("input format is incorrect")

	def islegal(self):  # current version: must have one worker
		#num of work er=1
		numofworker=0
		for i in self.smap:
			numofworker+=i.count("@")
			numofworker+=i.count("+")
		if not numofworker==1:
			return 0
		else: 
			return 1

	def setiniworkerposi(self): #automatically set worker's position. Must call when the warehouse is initializaed 
		for i in xrange(len(self.smap)):
			if self.smap[i].count("@")==1:
				self.workerposi=[i,self.smap[i].index("@")]
			elif self.smap[i].count("+")==1:
				self.workerposi=[i, self.smap[i].index("+")]
		#print(self.workerposi)
		
	def setworkerposi(self, posi):  # new position must be legal! used after move
		self.workerposi[0]=posi[0]
		self.workerposi[1]=posi[1]

	def isallgoalremoved(self):  # used after move to check whether the goal obtained
		numofemptygoal=0
		for i in self.smap:
			numofemptygoal+= i.count(".")
			numofemptygoal+= i.count("+")
		if numofemptygoal==0:
			return 1
		else: 
			return 0

	def show(self):  # show the configuation
		for i in self.smap:
			print("".join(i))

	def __eq__(self, y):  # overload ==, default as same map, or same str ("illegal move")
		if type(y) is Warehouse:
			if self.smap==y.smap:
				return 1
			else: 
				return 0
		elif type(y) is str:
			if self.smap==y:
				return 1
			else: 
				return 0
		else:
			print("error, unexpected situation in ==")
			return 0


	def __ne__(self, y):  # != is the opposite of ==
		return not __eq__(self, y)


	
	def move(self, direc,stype="NOT_UCS"):  # will determine whether the move is legal , if illegal, retrun "illegal"
		nextlist=copy.deepcopy(self.smap)
		wy=self.workerposi[0]
		wx=self.workerposi[1]
		if direc=="u":  # going up 
			if wy-1>=0 and not self.smap[wy-1][wx]=="#":  # can move up 
				if wy-2>=0 and any (x in self.smap[wy-1][wx] for x in ["$", "*"]):# a box on top
					if any (x in self.smap[wy-2][wx] for x in ["."," "]): # can move the box
						nextlist[wy][wx]=self.smap[wy][wx].replace("@"," ").replace("+",".") # worker moves
						nextlist[wy-1][wx]=self.smap[wy-1][wx].replace("$","@").replace("*","+") #box and worker
						nextlist[wy-2][wx]=self.smap[wy-2][wx].replace(" ","$").replace(".","*") # box moves						
						nexthouse=Warehouse(nextlist)
						nexthouse.setworkerposi([wy-1,wx])						
						if self.smap[wy-2][wx]=="." and nextlist[wy-2][wx]=="*": # double check if a box push to one goal
							nexthouse.allgoalremoved=nexthouse.isallgoalremoved()
						if stype=="UCS":   # when ucs is calling this function, at this branch the cost is 2
							return [nexthouse,2] # cost=2 
						else:
							return [nexthouse,1] # cost=1
					else:  # cannot move the box
						return ["ILLEGAL_MOVE",-10]


				elif any (x in self.smap[wy-1][wx] for x in [".", " "]): #can move  up, without bix
					nextlist[wy][wx]=self.smap[wy][wx].replace("@"," ").replace("+",".")
					nextlist[wy-1][wx]=self.smap[wy-1][wx].replace(" ","@").replace(".","+")
					nexthouse=Warehouse(nextlist)
					nexthouse.setworkerposi([wy-1,wx])
					return [nexthouse,1] #cost=1
				else:
					print("unexpected situation in move()!")
					return ["ILLEGAL_MOVE",-10]
			else:
				return ["ILLEGAL_MOVE",-10]

		if direc=="d":  # the opposite of "moving up"
			if wy+1<=len(self.smap)-1 and not self.smap[wy+1][wx]=="#":
				if wy+2<=len(self.smap)-1 and any (x in self.smap[wy+1][wx] for x in ["$", "*"]):# a box on bottom
					if any (x in self.smap[wy+2][wx] for x in ["."," "]): # can move the box
						nextlist[wy][wx]=self.smap[wy][wx].replace("@"," ").replace("+",".") # worker moves
						nextlist[wy+1][wx]=self.smap[wy+1][wx].replace("$","@").replace("*","+") #box and worker
						nextlist[wy+2][wx]=self.smap[wy+2][wx].replace(" ","$").replace(".","*") # box moves
						nexthouse=Warehouse(nextlist)
						nexthouse.setworkerposi([wy+1,wx])
						if self.smap[wy+2][wx]=="." and nextlist[wy+2][wx]=="*": # double check if a box push to one goal
							nexthouse.allgoalremoved=nexthouse.isallgoalremoved()
						if stype=="UCS":
							return [nexthouse,2] # cost=2 
						else:
							return [nexthouse,1] # cost=1
					else:
						return ["ILLEGAL_MOVE",-10] 


				elif any (x in self.smap[wy+1][wx] for x in [".", " "]): #can move , without box 
					nextlist[wy][wx]=self.smap[wy][wx].replace("@"," ").replace("+",".")
					nextlist[wy+1][wx]=self.smap[wy+1][wx].replace(" ","@").replace(".","+")
					nexthouse=Warehouse(nextlist)
					nexthouse.setworkerposi([wy+1,wx])
					return [nexthouse,1]
				else:
					print("unexpected situation in move()!")
					return ["ILLEGAL_MOVE",-10]
			else:
				return ["ILLEGAL_MOVE",-10]


		if direc=="l": # similar as up and down, with x, y interchanged
			if wx-1>=0 and not self.smap[wy][wx-1]=="#":
				if wx-2>=0 and any (x in self.smap[wy][wx-1] for x in ["$", "*"]):
					if any (x in self.smap[wy][wx-2] for x in ["."," "]): # can move the box
						nextlist[wy][wx]=self.smap[wy][wx].replace("@"," ").replace("+",".") # worker moves
						nextlist[wy][wx-1]=self.smap[wy][wx-1].replace("$","@").replace("*","+") #box and worker
						nextlist[wy][wx-2]=self.smap[wy][wx-2].replace(" ","$").replace(".","*") # box moves
						nexthouse=Warehouse(nextlist)
						nexthouse.setworkerposi([wy,wx-1])
						if self.smap[wy][wx-2]=="." and nextlist[wy][wx-2]=="*": # double check if a box push on one goal
							nexthouse.allgoalremoved=nexthouse.isallgoalremoved()
						if stype=="UCS":
							return [nexthouse,2] # cost=2 
						else:
							return [nexthouse,1] # cost=1					
					else:
						return ["ILLEGAL_MOVE",-10] 


				elif any (x in self.smap[wy][wx-1] for x in [".", " "]): #can move  
					nextlist[wy][wx]=self.smap[wy][wx].replace("@"," ").replace("+",".")
					nextlist[wy][wx-1]=self.smap[wy][wx-1].replace(" ","@").replace(".","+")
					nexthouse=Warehouse(nextlist)
					nexthouse.setworkerposi([wy,wx-1])
					return [nexthouse,1]
				else:
					print("unexpected situation in move()!")
					return ["ILLEGAL_MOVE",-10]
			else:
				return ["ILLEGAL_MOVE",-10]


		if direc=="r":  # opposite to moving left
			if wx+1<=len(self.smap[wy])-1 and not self.smap[wy][wx+1]=="#":
				if wx+2<=len(self.smap[wy])-1 and any (x in self.smap[wy][wx+1] for x in ["$", "*"]):# a box on top
					if any (x in self.smap[wy][wx+2] for x in ["."," "]): # can move the box
						nextlist[wy][wx]=self.smap[wy][wx].replace("@"," ").replace("+",".") # worker moves
						nextlist[wy][wx+1]=self.smap[wy][wx+1].replace("$","@").replace("*","+") #box and worker
						nextlist[wy][wx+2]=self.smap[wy][wx+2].replace(" ","$").replace(".","*") # box moves
						nexthouse=Warehouse(nextlist)
						nexthouse.setworkerposi([wy,wx+1])
						if self.smap[wy][wx+2]=="." and nextlist[wy][wx+2]=="*": # double check if a box push on one goal
							nexthouse.allgoalremoved=nexthouse.isallgoalremoved()
						if stype=="UCS":
							return [nexthouse,2] # cost=2 
						else:
							return [nexthouse,1] # cost=1
					else:
						return ["ILLEGAL_MOVE",-10] 


				elif any (x in self.smap[wy][wx+1] for x in [".", " "]): #can move  
					nextlist[wy][wx]=self.smap[wy][wx].replace("@"," ").replace("+",".")
					nextlist[wy][wx+1]=self.smap[wy][wx+1].replace(" ","@").replace(".","+")
					nexthouse=Warehouse(nextlist)
					nexthouse.setworkerposi([wy,wx+1])
					return [nexthouse,1]
				else:
					print("unexpected situation in move()!")
					return ["ILLEGAL_MOVE",-10]
			else:
				return ["ILLEGAL_MOVE",-10]
		else:
			print("input error")


                        

# previous testing programs:
#
#			
# if __name__=="__main__":
# 	inputhandler=Inputhandler()
# 	MAP=inputhandler.filetostr("input.txt")
# 	warehouse=Warehouse(MAP)
# 	warehouse.setiniworkerposi()
# 	warehouse.show()
# 	s=""
# 	while s!="quit":
# 		s=raw_input("move:")
# 		warehouse=warehouse.move(s)
# 		warehouse.show()
# 		print(warehouse.allgoalremoved)
	
# 	#newwarehouse=warehouse.show()
	
	
