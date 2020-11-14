import pandas as pd
import numpy as np
import warnings
import time

def getcolumn(x):
    if(x == 'ID'):
        return 8
    elif(x == '='):
        return 7
    elif (x == ')'):
        return 6
    elif (x == '('):
        return 5
    elif (x == '%'):
        return 4
    elif (x == '/'):
        return 3
    elif (x == '*'):
        return 2
    elif (x == '-'):
        return 1
    elif (x == '+'):
        return 0
    elif (x == 'int'):
        return 9
    elif (x == 'INT_NUM'):
        return 10
    elif (x == '$'):
        return 11
    elif (x == 'S'):
        return 12
    elif (x == 'A'):
        return 13
    elif (x == 'B'):
        return 14
    elif (x == 'C'):
        return 15
    elif (x == "S'"):
        return 16

actions = pd.read_csv('./data/actions.csv',header=None,dtype=np.object).values.tolist()
# goto = pd.read_csv('./data/goto.csv')

# print(goto)
tokenstr = open('./data/input_token.txt', 'r', encoding='utf-8-sig')
tokenlist = tokenstr.read().split(' ')  # 读取token串，将其分割成一个个单词，同时也是输入缓冲区
tokenlist.append('$') # 添加一个结束符

s_state = []  # 状态栈
s_token = []  # 单词栈
n = 0  # 缓冲区的读取头
cur_state = 0
s_state.append(0)  # 初始状态0入栈
action = []
action = actions[0][getcolumn(tokenlist[n])].split('?')  # 下一步的操作



while (actions[cur_state][getcolumn(tokenlist[n])] != "accept") :
    # time.sleep(0.5)
    if (action[0] == "shift"):
        # shift x:跳转到状态x，当前状态入栈，读头下的单词入栈，读头后移一位，根据读头下的内容更新下一步操作
        cur_state = int(action[1]) # 跳转到action所指状态
        s_state.append(cur_state) # 当前状态入栈
        s_token.append(tokenlist[n])  # 读头下的单词入栈
        n = n+1  # 读头向后移动一位
        action = actions[cur_state][getcolumn(tokenlist[n])]  # 更新下一步操作
        action = str(action).split('?')
        print(action)
        print(s_state)
        print(s_token)
        # print(type(action))
        # print(type())
    elif (action[0] == 'reduce'):
        # reduce A -> B - C:读头不动，将单词栈栈顶由B-C替换为A，状态栈也弹出对应的位数，当前状态跳转到栈顶状态，更新下一步操作由A决定
        # 跳转到A决定的状态，当前状态入栈
        # s_state.pop()
        # cur_state = s_state[len(s_state)-1]
        i = len(action)-1
        j = len(s_token)-1
        while(i > -1 and j > -1 and action[i] == s_token[j]):  # 将产生式右端的字符从栈顶弹出
            # print(action[i]+'   '+s_token[j])
            s_token.pop()
            s_state.pop()  # 状态也要对应的弹出
            i = i-1
            j = j-1
        cur_state = s_state[len(s_state) - 1]
        s_token.append(action[1])  # 单词栈栈顶替换为A
        action = actions[cur_state][getcolumn(action[1])]  # 更新下一步操作
        action = str(action).split('?')
        print(action)
        print(s_state)
        print(s_token)
        cur_state = int(action[0])
        s_state.append(cur_state)
        action = actions[cur_state][getcolumn(tokenlist[n])]  # 再次更新下一步操作
        action = str(action).split('?')
        print(action)
        print(s_state)
        print(s_token)
        # print("reduce")
    elif (action[0] == 'accept'):
        print("accept")
        break
    else :
        print("something wrong with your code!")
        exit(0)
    print("\n")
print("E' -> S'")
print("accept!")

