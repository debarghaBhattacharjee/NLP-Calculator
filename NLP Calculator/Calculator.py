from tkinter import *
from tkinter import messagebox
from BackendCode import *
from DatasetCode import *
import getpass

def selectMode():
  mode = 0
  password = str()
  attempts = 3
  choice = input("Enter as Admin? (Y/N) ")
  if choice == 'yes' or choice == 'Y' or choice == 'y':
    while attempts > 0:
      #password = input("Enter password: ")
      password = getpass.getpass("Enter password: ")
      if password == "debargha":
        mode = 1
        print("Entering as Admin.")
        return mode
      else:
        attempts = attempts - 1
        print("No. of attempts left: ", attempts)
    print("No more attempts left.")
    print("Entering as Guest.")
    return mode
  print("Entering as Guest.")
  return mode

mode = selectMode()  

root = Tk()
root.title("NLP Calculator")
root.iconbitmap("calculator.ico")
root.configure(background="#cfcfcf")
root.resizable(0,0)

def showResult():
  userQuery = entryQuery.get().lower()
  try:
    finalResult = solveQuery(userQuery)
  except Exception as e:
    errorMessage = "ERROR: " + str(e.args[0])
    print(errorMessage)
    messagebox.showinfo("ERROR", "Invalid query. Resolve and try again.")
    resetCalculator()
  else:
    textResult.configure(state=NORMAL)
    textResult.delete("1.0", END)
    textResult.insert(INSERT,finalResult)
    textResult.configure(state=DISABLED)
    if mode == 1:
      testData = "\n" + userQuery + "    " + str(finalResult)
      addData(testData)
  
def resetCalculator():
  entryQuery.delete(0,END)
  textResult.configure(state=NORMAL)
  textResult.delete("1.0", END)
  textResult.insert(INSERT,"Result is displayed here...")
  textResult.configure(state=DISABLED)
  
def addData(testData):
  result = messagebox.askquestion("DATASET", "Was the result correct?")
  if result == 'yes':
    addCorrectData(testData)
  else:
    addIncorrectData(testData)
  
labelTitle = Label( root, bd=1, relief=SOLID, width=40, height=5, padx=10, pady=5, font=("", 24, "bold"), text="NLP Calculator", justify='center')
labelTitle.pack(padx=15, pady=15)

frame = Frame(root, bd=1, relief=SOLID, padx=10, pady=10)
frame.pack(padx=15, pady=15)

labelQuery = Label(frame, bd=10, font=20, text="Enter Query: ")
labelQuery.pack(padx=15, pady=15)

entryQuery = Entry(frame, bd=2, relief=RIDGE, width=70, font=12)
entryQuery.pack(padx=15, pady=15)

buttonOK = Button(frame, text="OK", font=10, width=20, height=2, command=showResult)
buttonOK.pack(padx=15, pady=15)

buttonReset = Button(frame, text="Reset", font=10, width=20, height=2, command=resetCalculator)
buttonReset.pack()

labelResult = Label(frame, bd=10, font=20, text="Result: ")
labelResult.pack(side=LEFT, padx=15, pady=15)

textResult = Text(frame, bd=2, relief=RIDGE, font=12, width=60, height=5)
textResult.insert(INSERT, "Result is displayed here...")
textResult.configure(state=DISABLED)
textResult.pack(padx=15, pady=15)

root.mainloop()