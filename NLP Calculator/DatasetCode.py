import os
dirPath = os.path.dirname(os.path.abspath(__file__))

def addCorrectData(data):
  path = dirPath + '/correct.txt'
  fo = open(path,'a')
  fo.write(data)
  fo.close()
	
def addIncorrectData(data):
  path = dirPath + '/incorrect.txt'
  fo = open(path,'a')
  fo.write(data)
  fo.close()   
