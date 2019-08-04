from tkinter import *
import math
root = Tk()
root.title('Calculator')
##  Produce the window.

commandList = []
output = ''
LabelInput = Label(root, text= '',bg='green',width=30,height=1)
LabelInput.grid(row=1,column=1,columnspan=5)
LabelOutput = Label(root, text = output,bg='yellow',width=30,height=1)
LabelOutput.grid(row=2,column=1,columnspan=5)
##  Use commandList to save the input, use str 'output' to respect output. 

def Press7():
    commandList.append('7')
    nowText = ''.join(commandList)
    LabelInput = Label(root, text=nowText,bg = 'green',width=30,height=1)
    LabelInput.grid(row=1,column=1,columnspan=5)
def Press8():
    commandList.append('8')
    nowText = ''.join(commandList)
    LabelInput = Label(root, text=nowText,bg = 'green',width=30,height=1)
    LabelInput.grid(row=1,column=1,columnspan=5)
def Press9():
    commandList.append('9')
    nowText = ''.join(commandList)
    LabelInput = Label(root, text=nowText,bg = 'green',width=30,height=1)
    LabelInput.grid(row=1,column=1,columnspan=5)
def PressAdd():
    commandList.append('+')
    nowText = ''.join(commandList)
    LabelInput = Label(root, text=nowText,bg = 'green',width=30,height=1)
    LabelInput.grid(row=1,column=1,columnspan=5)
def Press4():
    commandList.append('4')
    nowText = ''.join(commandList)
    LabelInput = Label(root, text=nowText,bg = 'green',width=30,height=1)
    LabelInput.grid(row=1,column=1,columnspan=5)
def Press5():
    commandList.append('5')
    nowText = ''.join(commandList)
    LabelInput = Label(root, text=nowText,bg = 'green',width=30,height=1)
    LabelInput.grid(row=1,column=1,columnspan=5)
def Press6():
    commandList.append('6')
    nowText = ''.join(commandList)
    LabelInput = Label(root, text=nowText,bg = 'green',width=30,height=1)
    LabelInput.grid(row=1,column=1,columnspan=5)
def PressMinus():
    commandList.append('-')
    nowText = ''.join(commandList)
    LabelInput = Label(root, text=nowText,bg = 'green',width=30,height=1)
    LabelInput.grid(row=1,column=1,columnspan=5)
def PressLS():
    commandList.append('(')
    nowText = ''.join(commandList)
    LabelInput = Label(root, text=nowText,bg = 'green',width=30,height=1)
    LabelInput.grid(row=1,column=1,columnspan=5)
def Press1():
    commandList.append('1')
    nowText = ''.join(commandList)
    LabelInput = Label(root, text=nowText,bg = 'green',width=30,height=1)
    LabelInput.grid(row=1,column=1,columnspan=5)
def Press2():
    commandList.append('2')
    nowText = ''.join(commandList)
    LabelInput = Label(root, text=nowText,bg = 'green',width=30,height=1)
    LabelInput.grid(row=1,column=1,columnspan=5)
def Press3():
    commandList.append('3')
    nowText = ''.join(commandList)
    LabelInput = Label(root, text=nowText,bg = 'green',width=30,height=1)
    LabelInput.grid(row=1,column=1,columnspan=5)
def PressMult():
    commandList.append('*')
    nowText = ''.join(commandList)
    LabelInput = Label(root, text=nowText,bg = 'green',width=30,height=1)
    LabelInput.grid(row=1,column=1,columnspan=5)
def PressRS():
    commandList.append(')')
    nowText = ''.join(commandList)
    LabelInput = Label(root, text=nowText,bg = 'green',width=30,height=1)
    LabelInput.grid(row=1,column=1,columnspan=5)
def Press0():
    commandList.append('0')
    nowText = ''.join(commandList)
    LabelInput = Label(root, text=nowText,bg = 'green',width=30,height=1)
    LabelInput.grid(row=1,column=1,columnspan=5)
def PressPoint():
    commandList.append('.')
    nowText = ''.join(commandList)
    LabelInput = Label(root, text=nowText,bg = 'green',width=30,height=1)
    LabelInput.grid(row=1,column=1,columnspan=5)
def PressDiv():
    commandList.append('/')
    nowText = ''.join(commandList)
    LabelInput = Label(root, text=nowText,bg = 'green',width=30,height=1)
    LabelInput.grid(row=1,column=1,columnspan=5)

##  The functions before are all containing a str into commandList.
##  Then make a Label on the goal location.

def PressEqual():
    global output
    nowText = ''.join(commandList)
    try:
        y = eval(nowText)
        LabelOutput = Label(root, text=y,bg = 'yellow',width=30,height=1)
        LabelOutput.grid(row=2,column=1,columnspan=5)
    except:
        LabelOutput = Label(root, text='Expression Error',bg = 'yellow',width=30,height=1)
        LabelOutput.grid(row=2,column=1,columnspan=5)
    output = y
##  eval() is used to calculate the thing joined by commandList.
##  If it can not be read, it will show 'Expression Error'.
def PressDel():
    length = len(commandList)
    commandList.pop(length-1)
    nowText = ''.join(commandList)
    LabelInput = Label(root, text=nowText,bg = 'green',width=30,height=1)
    LabelInput.grid(row=1,column=1,columnspan=5)
##  pop the last str in the commandList.
def PressClear():
    y = len(commandList)
    while y >= 0:
        try:
            commandList.pop(y-1)
            y = y-1
        except:
            break
    nowText = ''.join(commandList)
    LabelInput = Label(root, text=nowText,bg = 'green',width=30,height=1)
    LabelInput.grid(row=1,column=1,columnspan=5)
    LabelOutput = Label(root, text='',bg = 'yellow',width=30,height=1)
    LabelOutput.grid(row=2,column=1,columnspan=5)
##  Use a while loop to pop all the str one by one, and let the output to be ''. 
def Presssin():
    global output
    x = ''.join(commandList)
    LabelInput = Label(root, text='sin('+ str(output) +')',bg = 'green',width=30,height=1)
    LabelInput.grid(row=1,column=1,columnspan=5)
    LabelOutput = Label(root, text=math.sin(float(output)),bg = 'yellow',width=30,height=1)
    LabelOutput.grid(row=2,column=1,columnspan=5)
def Presscos():
    global output
    x = ''.join(commandList)
    LabelInput = Label(root, text='cos('+ str(output) +')',bg = 'green',width=30,height=1)
    LabelInput.grid(row=1,column=1,columnspan=5)
    LabelOutput = Label(root, text=math.cos(float(output)),bg = 'yellow',width=30,height=1)
    LabelOutput.grid(row=2,column=1,columnspan=5)
def Presstan():
    global output
    x = ''.join(commandList)
    LabelInput = Label(root, text='tan('+ str(output) +')',bg = 'green',width=30,height=1)
    LabelInput.grid(row=1,column=1,columnspan=5)
    LabelOutput = Label(root, text=math.tan(float(output)),bg = 'yellow',width=30,height=1)
    LabelOutput.grid(row=2,column=1,columnspan=5)
def Presssqrt():
    global output
    x = ''.join(commandList)
    LabelInput = Label(root, text='sqrt('+ str(output) +')',bg = 'green',width=30,height=1)
    LabelInput.grid(row=1,column=1,columnspan=5)
    LabelOutput = Label(root, text=math.sqrt(float(output)),bg = 'yellow',width=30,height=1)
    LabelOutput.grid(row=2,column=1,columnspan=5)
def Press1_x():
    global output
    x = ''.join(commandList)
    LabelInput = Label(root, text='1/'+ str(output),bg = 'green',width=30,height=1)
    LabelInput.grid(row=1,column=1,columnspan=5)
    LabelOutput = Label(root, text=1/float(output),bg = 'yellow',width=30,height=1)
    LabelOutput.grid(row=2,column=1,columnspan=5)
##  The functions before are all used to getting the output and then put the output
##  in the Input Label and show the result in the Output Label.

##  Create the buttons.
Button7 = Button(root, text='   7   ',width=5,height=1,command=Press7)
Button7.grid(row=3,column=1)
Button8 = Button(root, text='   8   ',width=5,height=1,command=Press8)
Button8.grid(row=3,column=2)
Button9 = Button(root, text='   9   ',width=5,height=1,command=Press9)
Button9.grid(row=3,column=3) 
ButtonAdd = Button(root, text='   +   ',width=5,height=1,command=PressAdd)
ButtonAdd.grid(row=3,column=4)
Button4 = Button(root, text='   4   ',width=5,height=1,command=Press4)
Button4.grid(row=4,column=1)
Button5 = Button(root, text='   5   ',width=5,height=1,command=Press5)
Button5.grid(row=4,column=2)
Button6 = Button(root, text='   6   ',width=5,height=1,command=Press6)
Button6.grid(row=4,column=3) 
ButtonMinus = Button(root, text='   -    ',width=5,height=1,command=PressMinus)
ButtonMinus.grid(row=4,column=4)
ButtonLeftSquare = Button(root, text='    (    ',width=5,height=1,command=PressLS)
ButtonLeftSquare.grid(row=4,column=5)
Button1 = Button(root, text='   1   ',width=5,height=1,command=Press1)
Button1.grid(row=5,column=1)
Button2 = Button(root, text='   2   ',width=5,height=1,command=Press2)
Button2.grid(row=5,column=2)
Button3 = Button(root, text='   3   ',width=5,height=1,command=Press3)
Button3.grid(row=5,column=3) 
ButtonMult = Button(root, text='   *    ',width=5,height=1,command=PressMult)
ButtonMult.grid(row=5,column=4)
ButtonRightSquare = Button(root, text='    )    ',width=5,height=1,command=PressRS)
ButtonRightSquare.grid(row=5,column=5)
Button0 = Button(root, text='   0   ',width=5,height=1,command=Press0)
Button0.grid(row=6,column=1)
ButtonPoint = Button(root, text='   .    ',width=5,height=1,command=PressPoint)
ButtonPoint.grid(row=6,column=2) 
ButtonDiv = Button(root, text='   /    ',width=5,height=1,command=PressDiv)
ButtonDiv.grid(row=6,column=4)
ButtonEqual = Button(root, text='    =   ',width=5,height=1,command=PressEqual)
ButtonEqual.grid(row=6,column=5)
Buttontan = Button(root, text='  tan  ',width=5,height=1,command=Presstan)
Buttontan.grid(row=7,column=1)
Buttoncos = Button(root, text='  cos  ',width=5,height=1,command=Presscos)
Buttoncos.grid(row=7,column=2)
Buttonsin = Button(root, text='  sin  ',width=5,height=1,command=Presssin)
Buttonsin.grid(row=7,column=3) 
Buttonsqrt = Button(root, text=' sqrt ',width=5,height=1,command=Presssqrt)
Buttonsqrt.grid(row=7,column=4)
Button1_x = Button(root, text='  1/x  ',width=5,height=1,command=Press1_x)
Button1_x.grid(row=7,column=5)
ButtonClear = Button(root, text=' Clear',width=5,height=1,command=PressClear)
ButtonClear.grid(row=3,column=5)
ButtonDel = Button(root, text=' del  ',width=5,height=1,command=PressDel)
ButtonDel.grid(row=6,column=3)
