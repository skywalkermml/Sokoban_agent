#Author : Joshua Wang. Date 10/24 2013

import sys


class Inputhandler(object):
	def filetostr(self, str):  # transfer the file name to a nest list of strings
		MAP=[]   # the result
		inputfile=open(str, "r")
		l=inputfile.readline() 
		while l:
			l=l.strip("\n")
			MAP.append(list(l))
			l=inputfile.readline()

		
		return(MAP)
		

#if __name__=="__main__":
