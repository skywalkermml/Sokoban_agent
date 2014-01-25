#Author:Joshua Wang, date :10/24 2013 
#The data structure of the tree, 
import sys
from collections import defaultdict

#Amazing tree structure.  reference: https://gist.github.com/hrldcpr/2012250
def treestru(): return defaultdict(treestru)

class node(object):   # class of a node
	def __init__(self, state):
		self.path=""
		self.content=state
		self.cost=0
		self.expectcost=0
	



class tree(object):
	def __init__(self, root):  # must be a node class
		self.tree=treestru()
		root.path=''
		self.tree["root"]=root # the"root" key indicate the root of a subtree 
		

	def getroot(self, newtree):
		return newtree["root"]

	def getnode(self, path): # get the node of a path to it.
		tempstr=self.tree
		for i in xrange(len(path)):
			tempstr=tempstr[path[i]]
		return tempstr["root"]

	def addandreturnnode(self, parent, newnodecontent, branch):  # add a node to a tree, and return the node. useful in searches
		tempstr=self.tree                                    # strange property! self.tree does not change accordingly !
		for i in xrange(len(parent.path)):
			tempstr=tempstr[parent.path[i]]   
		newnode=node(newnodecontent) 
		newnode.path=parent.path+branch
		tempstr[branch]["root"]=newnode
		return newnode

	def addnode(self, parent, newnodecontent, branch):  # currently not used
		tempstr=self.tree
		for i in xrange(len(parent.path)):
			tempstr=tempstr[parent.path[i]]
		newnode=node(newnodecontent) 
		newnode.path=parent.path+branch
		tempstr[branch]["root"]=newnode
		

	def getnumofnodeinsubtree(self, subtree):
		numofnode=0
		if "root" in subtree:
			numofnode=1
			for i in subtree: 
				if i != "root":
					numofnode+=self.getnumofnodeinsubtree(subtree[i])
		return numofnode

	def getnumofnodes(self):	
		return self.getnumofnodeinsubtree(self.tree)



#previous test code
#
# testroot=node(1)
# testtree=tree(testroot)
# n1=testtree.addandreturnnode(testroot, 2, "r")
# n2=testtree.addandreturnnode(n1, 3, "r")
# n3=testtree.addandreturnnode(n1, 4, "l")

# print n3.path
# print testtree.tree["r"]["l"]["root"].content
# #print(testtree.tree["root"].content)
# #print(testtree.getnode("l").path)
# print(testtree.getnumofnodes())


