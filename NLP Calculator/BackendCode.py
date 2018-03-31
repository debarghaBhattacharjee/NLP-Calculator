from KeywordsList import *
from EvaluationCode import *
from word2number import w2n
from num2words import *
import spacy
nlp = spacy.load('en_core_web_sm')

operatorList = [[add,'+'], [sub1,'-'], [sub2, '--'], [mult,'*'], [div,'/']]

def inputQuery(query):
  if query == "":
    query = input("Enter your query: ")
  print("\n")
  print("--------------------------------------------QUERY-----------------------------------------------")
  print(query)
  print("------------------------------------------------------------------------------------------------")
  return query

def tokenizeQuery(query):
  doc = nlp(query)
  tokenizedQuery = []
  for token in doc:
    if token.text in markedVerbs:
      tokenizedQuery.append([markedVerbs[token.text], 'NN'])
      tokenizedQuery.append(['of', 'IN'])
    elif token.tag_ == 'LS':
      tokenizedQuery.append([token.text, 'CD'])
    elif token.text == 'point' or token.text == '.':
      tokenizedQuery.append(['point', 'CD'])	  
    else:	
      tokenizedQuery.append([token.text, token.tag_])
  print("\n")
  print("----------------------------------------TOKENIZED QUERY-----------------------------------------")
  print(tokenizedQuery)
  print("------------------------------------------------------------------------------------------------")
  return tokenizedQuery

def numberQuery(tokenizedQuery):
  numberedQuery = []
  currentNumber = str()
  countNumber = 0
  
  for i, token in enumerate(tokenizedQuery):
    if token[0] == 'point':
      if not set(numbers).isdisjoint(set(tokenizedQuery[i-1][0])):
        tokenizedQuery[i-1][0] = num2words(w2n.word_to_num(tokenizedQuery[i-1][0]))
		
      if not set(numbers).isdisjoint(set(tokenizedQuery[i+1][0])):	  
        tokenizedQuery[i+1][0] = num2words(w2n.word_to_num(tokenizedQuery[i+1][0]))		
		
  for token in tokenizedQuery:
    if not token[1] == 'CD':
      if currentNumber != "":
        numberedQuery.append([w2n.word_to_num(currentNumber), 'CD'])
        currentNumber = ""
        countNumber = 0
      numberedQuery.append(token)
    else:
      countNumber = countNumber + 1
      if '.' in token[0]:
        token[0] = num2words(token[0])
        print(token[0])
      if countNumber > 1:
        currentNumber = currentNumber + " " + token[0]
      else:
        currentNumber = currentNumber + token[0]
  if currentNumber != "":
    numberedQuery.append([w2n.word_to_num(currentNumber), 'CD'])
    currentNumber = ""	
  i = 0
  for i, token in enumerate(numberedQuery):
    if numberedQuery[i][1] == 'HYPH':
      numberedQuery[i+1] = [0 - numberedQuery[i+1][0], 'CD'] 
      del numberedQuery[i]
  print("\n")
  print("-----------------------------------------NUMBERED QUERY-----------------------------------------")
  print(numberedQuery)
  print("------------------------------------------------------------------------------------------------")
  return numberedQuery

def symbolizeQuery(numberedQuery):
  symbolizedQuery = []
  flag = 0
  for token in numberedQuery:
    for i in range(0,len(operatorList)):
      if token[0] in operatorList[i][0]:
        symbolizedQuery.append([operatorList[i][1],'SYM'])
        flag = 1
        break
    if flag == 0:
      symbolizedQuery.append(token)
    flag = 0
	
  for i, token in enumerate(symbolizedQuery):
    if token[0] in markedConjunctions:
      if symbolizedQuery[i-1][0] in markedSymbols:
        del symbolizedQuery[i]
  print("\n")
  print("-----------------------------------------SYMBOLIZED QUERY---------------------------------------")
  print(symbolizedQuery)
  print("------------------------------------------------------------------------------------------------")
  return symbolizedQuery

def modifySymbolizedQuery(symbolizedQuery):
  flag = 0
  mark = 0
  LB = 0
  RB = 0
  loop = 0
  highOperator1 = '('
  highOperator2 = '('
  for i, token in enumerate(symbolizedQuery):
    if token[1] == 'IN':
      flag = 1
      if token[0] in swapConjunction:
        symbolizedQuery[i] = ['and', 'CC']
  if flag == 1:
    for i, token in enumerate(symbolizedQuery):
      if token[1] == '-RRB-':
        highOperator1 = '('
        LB = LB - 1
      if token[1] == '-LRB-':
        LB = LB + 1
      if symbolizedQuery[i][1] == 'SYM':
        mark = 0
        selectedOperator = symbolizedQuery[i][0]
        
        if (symbolizedQuery[i-1][1] == 'CD') and (symbolizedQuery[i+1][1] == 'CD'):
          loop = loop + 1
          if (highOperator2 =='(' and highOperator1== '(') or (selectedOperator != highOperator1):
            if precedence[selectedOperator] > precedence[highOperator1]:
              highOperator1 = selectedOperator
              mark = 1
            else:
              highOperator2 = selectedOperator
              if precedence[selectedOperator] < precedence[highOperator1]:
                mark = 0
              elif precedence[selectedOperator] == precedence[highOperator1]:
                highOperator1 = selectedOperator
                mark = 1
				
          if mark == 1:
            del symbolizedQuery[i]
            symbolizedQuery.insert(i-1, ['of', 'IN'])
            symbolizedQuery.insert(i-1, [selectedOperator,'SYM'])
            symbolizedQuery.insert(i+2, ['and','CC'])

          print("L" + str(loop) + ": " + str(symbolizedQuery)) 			
		  
        elif (symbolizedQuery[i-1][1] == 'CD') and (symbolizedQuery[i+1][1] == 'SYM'):
          if precedence[selectedOperator] > precedence[highOperator1]: 
            highOperator1 = selectedOperator
            del symbolizedQuery[i]
            symbolizedQuery.insert(i-1, ['of', 'IN'])
            symbolizedQuery.insert(i-1, [selectedOperator,'SYM'])
            symbolizedQuery.insert(i+2, ['and','CC'])
			
        elif (symbolizedQuery[i-1][1] == 'CD') and (symbolizedQuery[i+1][1] == '-LRB-'):
          if precedence[selectedOperator] > precedence[highOperator1]: 
            highOperator1 = selectedOperator
            del symbolizedQuery[i+1]
            del symbolizedQuery[i+1]
            symbolizedQuery.insert(i-1, ['of', 'IN'])
            symbolizedQuery.insert(i-1, [selectedOperator,'SYM'])
            symbolizedQuery.insert(i+2, ['and','CC'])
			
        elif (symbolizedQuery[i-1][1] == 'CD') and (symbolizedQuery[i+1][1] == 'CC'):
          if precedence[selectedOperator] > precedence[highOperator1]: 
            highOperator1 = selectedOperator
            del symbolizedQuery[i]
            symbolizedQuery.insert(i-1, ['of', 'IN'])
            symbolizedQuery.insert(i-1, [selectedOperator,'SYM'])
          else:
            del symbolizedQuery[i+1]
			
    while LB > 0:
      symbolizedQuery.append([')', '-RRB'])
      LB = LB - 1
	  
    i = 0	
    for i in range(len(symbolizedQuery)-1, 0, -1):
      if symbolizedQuery[i][1] == '-RRB-':
        RB = RB + 1
      elif symbolizedQuery[i][1] == '-LRB-':
        RB = RB - 1
      i = i + 2
    while RB > 0:
      symbolizedQuery.insert(0, ['(', '-LRB-'])
      RB = RB - 1
					
  print("\n")
  print("-----------------------------------MODIFIED SYMBOLIZED QUERY------------------------------------")
  print(symbolizedQuery)
  print("------------------------------------------------------------------------------------------------")
  return symbolizedQuery
 		
def filterQuery(symbolizedQuery):
  filteredQuery = []
  for token in symbolizedQuery:
    if token[0] in symbols:
      filteredQuery.append([token[0], 'SYM'])
    elif (not token[1] in stopWordsTags) and (not token[0] in stopWordsSymbols):
      filteredQuery.append(token)
  print("\n")
  print("-----------------------------------------FILTERED QUERY-----------------------------------------")
  print(filteredQuery)
  print("------------------------------------------------------------------------------------------------")
  return filteredQuery

def solveQuery(userQuery):
  print("\n\n                                     ~~~~~ TEST CASE ~~~~~                                      ")
  print("################################################################################################")
  query = inputQuery(userQuery)
  tokenizedQuery = tokenizeQuery(query)
  numberedQuery = numberQuery(tokenizedQuery)
  symbolizedQuery = symbolizeQuery(numberedQuery)
  symbolizedQuery = modifySymbolizedQuery(symbolizedQuery)
  filteredQuery = filterQuery(symbolizedQuery)
  result = evaluateQuery(filteredQuery)
  print("\n")
  print("-----------------------------------------FINAL RESULT-------------------------------------------")
  print(result)
  print("------------------------------------------------------------------------------------------------")
  return result

