# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Window.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5 import QtWidgets, Qt
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import numpy as np
from collections import deque
from graphviz import Digraph
import os
import shutil


def preprocessing(expression):
    expression = list(expression)
    i = 0
    while (i < len(expression) - 1):
        if (expression[i] in "+*)" or (expression[i] >= 'a' and expression[i] <= 'z')) and (
                (expression[i + 1] >= 'a' and expression[i + 1] <= 'z') or expression[i + 1] == '('):
            expression.insert(i + 1, '&')
        i += 1
    return ''.join(expression)


def middle2behind(expression):  
    dirt={'+':3,'*':3,'&':2,'|':1,'(':0}
    result = []             # 结果列表
    stack = []              # 栈
    for item in expression: 
        if item>='a' and item<='z':      # 如果当前字符为操作数那么直接放入结果列表
            result.append(item) 
        else:
            if len(stack)==0:
                stack.append(item)
            else:
                if item=='(':
                    stack.append(item)
                    continue
                if item==')':
                    while(stack[-1]!='('):
                        result.append(stack.pop())
                    stack.pop()
                elif len(stack)>0 and dirt[item]>dirt[stack[-1]]:
                    stack.append(item)
                else:
                    while(len(stack)>0 and dirt[item]<=dirt[stack[-1]]):
                            result.append(stack.pop())
                    
                    stack.append(item)
    while(len(stack)!=0):
        result.append(stack.pop())
    return ''.join(result)


class NFAstate:
    index = 0

    def __init__(self):
        # 当前节点编号
        self.index = NFAstate.index
        # 当前节点值
        self.value = '#'
        # 当前结点连接到的编号
        self.chTrans = -1
        # 当前节点通过ε转移到的状态号集合
        self.eps = set()
        NFAstate.index += 1






class NFA:    
    def __init__(self, num):
        if num == -1:
            self.head = -1
            self.tail = -1
        else:
            self.head = ns_list[num]
            self.tail = ns_list[num + 1]


def add(n1, n2, ch):
    n1.value = ch
    n1.chTrans = n2.index


def add1(n1, n2):
    n1.eps.add(n2.index)


def str2NFA(exp):
    print('nfa')
    stack=[]
    ch_set = set()
    num=0
    print(num)
    for ch in exp:
        if ch>='a' and ch<='z':
            n=NFA(num)
            num+=2
            add(n.head,n.tail,ch)
            ch_set.add(ch)
            stack.append(n)
        elif ch=='+':
            n=NFA(num)
            num+=2
            n1=stack.pop()
            add1(n1.tail,n.head)
            add1(n1.tail,n.tail)
            add1(n.head,n1.head)
            stack.append(n)
            
        elif ch=='*':
            n=NFA(num)
            num+=2
            n1=stack.pop()
            add1(n1.tail,n.head)
            add1(n1.tail,n.tail)
            add1(n.head,n1.head)
            add1(n.head,n.tail)
            stack.append(n)
        elif ch=='&':
            n=NFA(-1)
            n1=stack.pop()
            n2=stack.pop()
            add1(n2.tail,n1.head)
            n.head=n2.head
            n.tail=n1.tail
            stack.append(n)
        elif ch=='|':
            n=NFA(num)
            num+=2
            n1=stack.pop()
            n2=stack.pop()
            add1(n.head,n1.head)
            add1(n.head,n2.head)
            add1(n1.tail,n.tail)
            add1(n2.tail,n.tail)
            stack.append(n)
    nfa=stack.pop()
    print('nnnnffa')
    return nfa,num,ch_set

class DFAstate:
    index = 0

    def __init__(self):
        self.isEnd = False
        self.index = DFAstate.index
        self.closure = set()
        self.Edges = []
        DFAstate.index += 1


class DFA:
    def __init__(self):
        self.startState = 0  # 开始状态为0
        self.endStates = set()
        self.terminator = set()
        self.trans = np.array([[-1 for j in range(26)] for i in range(128)])


def cloure(s):
    # 求集合s的ε闭包
    ep_stack = []
    s_list = list(s)
    for item in s_list:
        ep_stack.append(item)
    while (len(ep_stack) > 0):
        temp = ep_stack.pop()
        for item in list(ns_list[temp].eps):
            if item not in s:
                s.add(item)
                ep_stack.append(item)
    return s


def move(s, ch):
    """
    Parameters
    ----------
    s : SET
        epsilon闭包.
    ch : CHAR
        匹配的操作数.

    Return 新的epsilon闭包
    -------
    """
    temp = set()
    for item in s:
        if ns_list[item].value == ch:
            temp.add(ns_list[item].chTrans)
    temp = cloure(temp)
    return temp


def isEnd(n, s):
    """
    Parameters
    ----------
    n : NFA
    s : SET
        闭包.
    Returns True or False
    -------
    """
    for item in s:
        if n.tail.index == item:
            return True
    return False




def nfa2dfa(nfa, exp):
    dfanum = 0
    d = DFA()
    q = deque()
    states = set()
    exp = list(exp)
    exp.sort()
    stateSet = set()
    # 找到终止符集
    for ch in exp:
        if ch >= 'a' and ch <= 'z':
            d.terminator.add(ch)

    tempSet = set()
    tempSet.add(nfa.head.index)
    ds_list[0].closure = cloure(tempSet)  # 得到初态的ε闭包
    ds_list[0].isEnd = isEnd(nfa, ds_list[0].closure)
    dfanum += 1

    q.append(d.startState)

    while len(q) > 0:
        num = q.popleft()
        dt = list(d.terminator)
        dt.sort()
        for ch in dt:
            temp = move(ds_list[num].closure, ch)  # 对每个终止符号进行move运算
            if len(temp) > 0 and tuple(temp) not in stateSet:  # 如果当前闭包未出现过，则进栈
                stateSet.add(tuple(temp))
                ds_list[dfanum].closure = temp
                ds_list[num].Edges.append([ch, dfanum])
                d.trans[num][ord(ch) - ord('a')] = dfanum
                ds_list[dfanum].isEnd = isEnd(nfa, ds_list[dfanum].closure)
                q.append(dfanum)

                dfanum += 1
            else:
                for i in range(dfanum):
                    if temp == ds_list[i].closure:
                        ds_list[num].Edges.append([ch, i])
                        d.trans[num][ord(ch) - ord('a')] = i
                        break
    for item in ds_list:
        if item.isEnd == True:
            d.endStates.add(item)

    return d, dfanum, len(dt)

class stateSet:
    def __init__(self):
        self.index = -1  # 能转换到的状态集标号
        self.s = set()  # 该状态集中的dfa状态号





def minDFA(dfa, dfanum):
    s = [set() for i in range(128)]
    minDFA = DFA()
    minDFA.terminator = dfa.terminator

    # 下面将DFA状态分为终态和非终态
    endFlag = 1  # 判断是否DFA状态全为终态，若为1则是，为0则否
    for i in range(dfanum):
        if ds_list[i].isEnd == True:
            s[0].add(ds_list[i].index)
        else:
            endFlag = 0
            s[1].add(ds_list[i].index)
            numstateSet = 2  # 初始的状态数
    if endFlag == 1:
        numstateSet = 1  # DFA状态全为终态，所以只有一个状态集合

    cutFlag = True  # 上一次是否产生新的划分的标志
    while (cutFlag):  # 若上一次产生新的划分则继续循环
        cutCount = 0
        for statenum in range(numstateSet):
            for ch in dfa.terminator:  # 对每个终结符做move
                setNum = 0  # 当前划分的个数
                temp = [stateSet() for i in range(20)]  # 初始化缓冲区用于存储当前move操作的划分集合

                for item in s[statenum]:
                    epFlag = True  # 判断该集合是否存在没有此终结符对应的边
                    for edge in ds_list[item].Edges:
                        if edge[0] == ch:
                            epFlag = False
                            transNum = -1
                            for i in range(numstateSet):
                                s_temp = list(s[i])
                                for j in range(len(s_temp)):
                                    if edge[1] == s_temp[j]:
                                        transNum = i
                                        break
                            curSetNum = 0
                            while temp[curSetNum].index != transNum and curSetNum < setNum:
                                curSetNum += 1
                            if curSetNum == setNum:
                                temp[setNum].index = transNum
                                temp[setNum].s.add(item)
                                setNum += 1
                            else:
                                temp[curSetNum].s.add(item)
                    if epFlag == True:
                        curSetNum = 0
                        while temp[curSetNum].index != -1 and curSetNum < setNum:
                            curSetNum += 1
                        if curSetNum == setNum:
                            temp[setNum].index = -1
                            temp[setNum].s.add(item)
                            setNum += 1
                        else:
                            temp[curSetNum].s.add(item)

                if setNum > 1:
                    cutCount += 1
                    for i in range(setNum):
                        differ = False
                        for item in temp[i].s:
                            if item in s[i]:
                                s[i].remove(item)
                                s[numstateSet].add(item)
                                differ = True
                        if differ == True:
                            numstateSet += 1

        if cutCount == 0:
            cutFlag = False
            # 遍历每个划分好的状态集
    for i in range(numstateSet):
        for item in s[i]:
            if item == dfa.startState:  # 如果当前状态为初态，则最小化DFA状态也为初态
                minDFA.startState = i
            endStates = [state.index for state in dfa.endStates]
            if item in endStates:  # 如果当前状态为终态，则最小化DFA状态也为终态
                mds_list[i].isEnd = True
                minDFA.endStates.add(i)

            for edge in ds_list[item].Edges:
                for t in range(numstateSet):
                    if edge[1] in s[t]:
                        haveEdge = False
                        for m_edge in mds_list[i].Edges:
                            if m_edge[0] == edge[0] and m_edge[1] == edge[1]:
                                haveEdge = True
                        if haveEdge == False:
                            if [edge[0], t] not in mds_list[i].Edges:
                                mds_list[i].Edges.append([edge[0], t])
                            minDFA.trans[i][ord(edge[0]) - ord('a')] = t

    return minDFA, numstateSet


def dfa2code(minDFA,numstateSet):
    state=minDFA.startState
    code=''
    code+='int startState = '+str(state)+';\n'
    code+='int state = startState;\n'
    code+='bool quit = false;\n'
    
    code+='while(quit == false)\n{\n'
    code+='    char ch = cin.get(); //ch属于[a-z] \n'
    code+='    switch(state)\n    {\n'
    for i in range(numstateSet):
        code+='    case '+str(mds_list[i].index-128)+':\n'
        if mds_list[i].isEnd==True:
            code+='        switch(ch)\n        {\n'
            for edge in mds_list[i].Edges:
                
                code+="            case '"+str(edge[0])+"':\n"
                code+='                state = '+str(edge[1])+';\n'
                code+='                break;\n'
            code+='            default:\n'
            code+='                quit = true;\n                cout<<"到达终止状态，正常结束。"<<endl;\n                break;\n'
            code+='        }\n'
            code+='        break;\n'
            
        else:    
            code+='        switch(ch)\n        {\n'
            for edge in mds_list[i].Edges:
                
                code+="            case '"+str(edge[0])+"':\n"
                code+='                state = '+str(edge[1])+';\n'
                code+='                break;\n'
            code+='            default:\n'
            code+='                cout<<"错误：出现意料外的字符！"<<endl;\n'
            code+='                cout<<"匹配提前终止."<<endl;\n'
            code+='                quit = true;\n'
            code+='                break;\n'
            code+='        }\n'
            code+='        break;\n'
    
    code+='    }\n'
    code+='}\n'
    return code

class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self,item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)

def matchBoth(item1,item2):
    leftbrac = "{[("
    rightbrac = "}])"
    return leftbrac.index(item1) == rightbrac.index(item2)

def bracMatch(bracketItem):
    bracketList = list(bracketItem)
    braStack = Stack()
    leftbrac = "{[("
    rightbrac = "}])"
    result = True
    for item in bracketList:
        if item in leftbrac:
            braStack.push(item)
        elif item in rightbrac:
            if braStack.isEmpty():
                result = False
            else:
                if matchBoth(braStack.peek(),item):
                    braStack.pop()
                else:
                    result = False

    if braStack.isEmpty() and result:
        result = True
    else:
        result = False
    return result

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1242, 825)
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 0, 1131, 811))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(50, -1, 50, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setMinimumSize(QtCore.QSize(100, 50))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(22)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit.setMinimumSize(QtCore.QSize(50, 30))
        self.lineEdit.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_3.addWidget(self.lineEdit)
        self.pushButton_5 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout_3.addWidget(self.pushButton_5)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        spacerItem2 = QtWidgets.QSpacerItem(30, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(50, -1, 50, -1)
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.pushButton_2 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.pushButton_3 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem5)
        self.pushButton_4 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout.addWidget(self.pushButton_4)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        spacerItem6 = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem6)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QTextEdit(self.layoutWidget)
        self.label_2.setMinimumSize(QtCore.QSize(500, 500))
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_2.setPlaceholderText("代码区域")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.tableView = QtWidgets.QTableView(self.layoutWidget)
        self.tableView.setMinimumSize(QtCore.QSize(300, 300))
        self.tableView.setObjectName("tableView")
        self.horizontalLayout_2.addWidget(self.tableView)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.layoutWidget.raise_()
        self.lineEdit.raise_()
        self.pushButton_5.raise_()
        self.lineEdit.raise_()
        self.pushButton_5.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.pushButton_5.clicked.connect(self.analysis) #分析
        self.pushButton.clicked.connect(self.printNFA) #NFA
        self.pushButton_2.clicked.connect(self.dfa_table) #DFA
        self.pushButton_3.clicked.connect(self.mindfa_table) #最小化DFA
        self.pushButton_4.clicked.connect(self.code) #生成代码

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ELEX"))
        self.label.setText(_translate("MainWindow", "ELEX词法分析器"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "请输入正则表达式(支持运算符()+*&|)"))
        self.pushButton_5.setText(_translate("MainWindow", "分析"))
        self.pushButton.setText(_translate("MainWindow", "生成NFA"))
        self.pushButton_2.setText(_translate("MainWindow", "生成DFA"))
        self.pushButton_3.setText(_translate("MainWindow", "最小化DFA"))
        self.pushButton_4.setText(_translate("MainWindow", "生成代码"))




    def analysis(self):
        filepath='temp'
        if not os.path.exists(filepath):
            os.mkdir(filepath)
        else:
            shutil.rmtree(filepath)
            os.mkdir(filepath)
        
        expression = self.lineEdit.text()
        print(expression)
        if len(expression)==0:
            QtWidgets.QMessageBox.critical(self, "错误",'正则表达式不合法',QtWidgets.QMessageBox.Ok)
            print("不合法")
            return
        ops=['&','(',')']
        legel=True
        for i in range(len(expression)):
            if (expression[i]>='a' and expression[i]<='z') or expression[i] in ops:
                continue
            if expression[i]=='|':
                if i!=0 and (i!=len(expression)-1 and expression[i-1]<='z' and expression[i-1]>='a' and expression[i+1]<='z' and expression[i+1]>='a') or expression[i-1]==')':
                    continue
                if expression[i-1]=='*':
                    if i-1!=0 and ((expression[i-2]<='z' and expression[i-2]>='a') or expression[i-2]==')'):
                        continue
                    else:
                        legel=False
                        break
                if expression[i-1]=='+':
                    if i-1!=0 and ((expression[i-2]<='z' and expression[i-2]>='a') or expression[i-2]==')'):
                        continue
                    else:
                        legel=False
                        break
                else:
                    legel=False
                    break
            elif expression[i]=='*':
                if i!=0 and ((expression[i-1]<='z' and expression[i-1]>='a') or expression[i-1]==')'):
                    continue
                else:
                    legel=False
                    break
            elif expression[i]=='+':
                if i!=0 and ((expression[i-1]<='z' and expression[i-1]>='a') or expression[i-1]==')'):
                    continue
                else:
                    legel=False
                    break
            else:
                legel=False
                break
        if legel==False:
            QtWidgets.QMessageBox.critical(self, "错误",'正则表达式不合法',QtWidgets.QMessageBox.Ok)
            print("不合法")
            return
        legel=bracMatch(expression)
        if legel==False:
            QtWidgets.QMessageBox.critical(self, "错误",'正则表达式不合法',QtWidgets.QMessageBox.Ok)
            print("不合法")
            return
        else:
            global ch_set
            global ns_list
            global ds_list
            global mds_list
            NFAstate.index=0
            DFAstate.index=0
            ns_list = [NFAstate() for i in range(128)]
            print(ns_list[0].index)
            ds_list = [DFAstate() for i in range(128)]
            print(ds_list[0].index)
            mds_list = [DFAstate() for i in range(128)]
            ch_set=set()
            expression = preprocessing(expression)
            print(expression)
            expression = middle2behind(expression)
            print(expression)
            global nfanum
            nfa, nfanum,ch_set = str2NFA(expression)
            global dfanum
            global terminator_num
            dfa, dfanum, terminater_num = nfa2dfa(nfa, expression)
            global numstate
            mindfa, numstate = minDFA(dfa, dfanum)
            code=dfa2code(mindfa, numstate)
            print(code)
            QMessageBox.information(self,'信息','分析完成，请点击下方按钮查看详细信息',QMessageBox.Yes)
        global nfa1
        nfa1=nfa
        global dfa1
        dfa1=dfa
        global mindfa1
        mindfa1=mindfa
        global code1
        code1=code
    
    def code(self):
        self.label_2.setText(code1)
        
    def mindfa_table(self):
        self.model=QStandardItemModel(numstate,len(mindfa1.terminator))
        self.model.setVerticalHeaderLabels(['' for i in range(numstate)])
        
        tmp=list(dfa1.terminator)
        tmp.sort()
        tmp.insert(0,'DFA状态')
        self.model.setHorizontalHeaderLabels(list(tmp))
        print(str(mindfa1.trans))
        print(numstate,len(mindfa1.terminator))
        for row in range(numstate):
            i=QStandardItem(str(row))
            self.model.setItem(row,0,i)
            for col in range(len(mindfa1.terminator)):
                i=QStandardItem(str(mindfa1.trans[row][col]))
                print(i)
                self.model.setItem(row,col+1,i)
        self.tableView.setModel(self.model)
        self.label_2.setPlaceholderText("右为最小化DFA状态表\n最小化DFA图蓝色结点为初态，红色结点为终态")
        #绘图
        g=Digraph('mindfa',graph_attr={'rankdir':'LR'},format='png')
        for i in range(numstate):
            if i==mindfa1.startState:
                g.node(name=str(i),color='blue')
            elif mds_list[i].isEnd==True:
                g.node(name=str(i),color='red')
            elif i==mindfa1.startState and mds_list[i].isEnd==True:
                g.node(name=str(i),color='purple')
            else:g.node(name=str(i))
        for i in range(numstate):
            for edge in mds_list[i].Edges:
                g.edge(str(mds_list[i].index-128),str(edge[1]),label=str(edge[0]))
        g.view(filename='temp/mindfa.png')
    
    def dfa_table(self):
        self.model=QStandardItemModel(dfanum,len(dfa1.terminator))
        self.model.setVerticalHeaderLabels(['' for i in range(numstate+1)])
        
        #设置水平方向四个头标签文本内容
        tmp=list(dfa1.terminator)
        tmp.sort()
        tmp.insert(0,'DFA状态')
        self.model.setHorizontalHeaderLabels(list(tmp))
        print(str(dfa1.trans))
        print(dfanum,len(dfa1.terminator))
        for row in range(dfanum):
            print(row)
            i=QStandardItem(str(row))
            self.model.setItem(row,0,i)
            for col in range(len(dfa1.terminator)):
                print(str(dfa1.trans[row][col]))
                i=QStandardItem(str(dfa1.trans[row][col]))
                print(i)
                self.model.setItem(row,col+1,i)
        self.tableView.setModel(self.model)
        self.label_2.setPlaceholderText("右为DFA状态表\nDFA图蓝色结点为初态，红色结点为终态")
        #绘图
        g=Digraph('dfa',graph_attr={'rankdir':'LR'},format='png')
        for i in range(dfanum):
            if i==dfa1.startState:
                g.node(name=str(i),color='blue')
            elif ds_list[i].isEnd==True:
                g.node(name=str(i),color='red')
            elif i==dfa1.startState and ds_list[i].isEnd==True:
                g.node(name=str(i),color='purple')
            else:g.node(name=str(i))
        for i in range(dfanum):
            for edge in ds_list[i].Edges:
                g.edge(str(ds_list[i].index),str(edge[1]),label=str(edge[0]))
        g.view(filename='temp/dfa.png')
    
    def printNFA(self):
    #输出状态转换表
        ch_set.add('ε')
        ch_list=list(ch_set)
        ch_list.sort()
        self.model=QStandardItemModel(nfanum,len(ch_list))
        self.model.setVerticalHeaderLabels([str(i) for i in range(nfanum)])
        self.model.setHorizontalHeaderLabels(ch_list)
        
        ch_dirt={}
        for i in range(len(ch_list)):
            ch_dirt[ch_list[i]]=i
        
        for k in range(len(ns_list)):
            if len(ns_list[k].eps)!=0:
                v=''
                for item in ns_list[k].eps:
                    v+=str(item )+' '
                i=QStandardItem(v)

                self.model.setItem(ns_list[k].index,len(ch_list)-1,i)
            
            if ns_list[k].value in ch_list:
                i=QStandardItem(str(ns_list[k].chTrans))
                print(i)
                self.model.setItem(ns_list[k].index,ch_dirt[ns_list[k].value],i)
        self.tableView.setModel(self.model)
        self.label_2.setPlaceholderText("右为NFA状态表\nNFA图蓝色结点为初态，红色结点为终态")
        #画图
        g=Digraph('nfa',graph_attr={'rankdir':'LR'},format='png')
        for i in range(nfanum):
            if i==nfa1.head.index:
                g.node(str(i),color='blue')
            if i==nfa1.tail.index:
                g.node(str(i),color='red')
        for k in range(len(ns_list)):
            if len(ns_list[k].eps)!=0:
                for item in ns_list[k].eps:
                    g.edge(str(ns_list[k].index),str(item),label='ε')
            
            if ns_list[k].value in ch_list:
                g.edge(str(ns_list[k].index),str(ns_list[k].chTrans),label=ns_list[k].value)
                
        g.view(filename='temp/nfa.png')

import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow


class UsingTest(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(UsingTest, self).__init__(*args, **kwargs)
        self.setupUi(self)  # 初始化ui




if __name__ == '__main__':  # 程序的入口
    app = QApplication(sys.argv)
    win = UsingTest()
    win.show()
    sys.exit(app.exec_())