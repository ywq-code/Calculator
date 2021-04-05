# -*- coding: UTF-8 -*-
import os
import math
import random
import re
from enum import Enum
import datetime

class Type(Enum):
    add_sub = 0  #加减法
    mul_div = 1  #乘除法
    mix = 2      #混合运算
    none = 3

class Signs(Enum):
    add = 0
    sub = 1
    mul = 2
    div = 3


class Calculator:
    def __init__(self):
        self.QestionNum = 0     #题目数量
        self.ElementNum = 0     #题目元素数量
        self.QuestionType = Type.none   #运算的类型
        self.NumRange = 0           #元素的数据范围
        self.LogFile = self.LogFileInit() #log文件路径初始化
        self.QuestionCounter = 0    #答题数量计数
        self.RightCounter = 0   #记录正确答题数
        self.Accuracy = 0   #保存准确率
        #print("calculator")
    
    def CheckRules(self, datas, symbols):
        """
        函数功能：
            检查随机生成的数字和符号组成是否符合计算规则，主要检查0前后的乘除符号
        入口参数:
            data:列表，随机生成的数据
            synbol:列表，随机生成的计算符号
        返回值：
            true/false
        """
        symbols_length = len(symbols)
        if datas[0] == 0 and (symbols[0] == 2  or symbols[0] == 3):
            return False
        if datas[symbols_length] == 0 and (symbols[symbols_length - 1] == 2 or symbols[symbols_length - 1] == 3):
            return False
        #遍历数据列表查找零元素，并查找零元素后面对应的计算符号是否是除法（3）并且零元素前面是乘除   
        for index in range(1, symbols_length):
            if datas[index] == 0 and ((symbols[index] == 2 or symbols[index] == 3) or (symbols[index - 1] == 2 or symbols[index - 1] == 3)):
                return False
        """for index, data in enumerate(datas, 1):
            if data == 0 and index < length and ((symbols[index - 1] == Signs.mul or symbols[index - 1] == Signs.div) or (symbols[index] == Signs.div or symbols[index] == Signs.mul)) : 
                return False"""
        return True

    def CheckFloat(self, Resultstr):
        """
        函数功能：
            检查计算结果是否是小数
        入口参数：
            结果字符串
        返回值：
            true/false
        """
        index = Resultstr.find('.')
        if index == -1:
            return False
        if ((index == len(Resultstr) - 2) and (Resultstr[index + 1] == '0')):
            return False
        else:
            return True
         

    def GetRandInfo(self):
        """
        函数功能：
            得到表达式信息
        入口参数：
            出题数量、出题类型、数据范围
        返回值：
            算式元素、算式计算符号
        """
        SignList = []   #存放符号
        DateList = []   #存放数据
        if int(self.ElementNum) < 2:
            print("算式元素个数应大于等于2")
            return
        #else: SignList.append(self.ElementNum)

        #随机生成计算符号
        if self.QuestionType == Type.add_sub:   #加减法
            SignList += [random.randint(0,1) for _ in range(self.ElementNum - 1)]
        elif self.QuestionType == Type.mul_div:   #乘除法
            SignList += [random.randint(2,3) for _ in range(self.ElementNum - 1)]
        elif self.QuestionType == Type.mix:  #混合运算
            SignList += [random.randint(0,3) for _ in range(self.ElementNum - 1)]
        else:
            print("算式类型错误")
            return
        #生成算式元素
        DataList = [random.randint(0, self.NumRange) for _ in range(self.ElementNum)]

        if self.CheckRules(DataList,SignList):
            return DataList,SignList
        else: 
            return self.GetRandInfo()

    def GetExprssion(self):
        """
        函数功能：
            表达式生成
        返回值
            表达式和结果
        """
        SymbolList = [r"+", r"-", r"*", r"/"]
        Datas,Signs = self.GetRandInfo()
        length = len(Signs)
        ExpressionList = []
        for i in range(length):
            ExpressionList.append(str(Datas[i]))
            ExpressionList.append(SymbolList[Signs[i]])
        ExpressionList.append(str(Datas[length]))
        ExpressionStr = "".join(ExpressionList) #得到表达式字符串
        result = eval(ExpressionStr) #计算结果
        result_str = str(result)
        #对结果进行检查，如果是小数，重新生成
        if self.CheckFloat(result_str) == True:
            #print("计算结果是小数")
            return self.GetExprssion()
        else :
            return ExpressionStr,result_str
    
    def LogFileInit(self):
        """
        函数功能：
            log文件初始化
        返回值
            log文件的路径
        """
        LogFileDir = './log/'
        #获取当前时间
        CurrTime = datetime.datetime.now()
        TimeStr = CurrTime.strftime(r"%Y-%m-%d-%H-%M")
        filename = TimeStr + ".txt"
        Logfile = os.path.join(LogFileDir, filename)
        f = open(Logfile, 'a+', encoding="utf-8")
        #写入基本信息
        f.writelines(["时间：",TimeStr,'\t',
                    "题目数量：",str(self.QestionNum),'\t',
                    "运算类型：",str(self.QuestionType),'\n'])
        f.close()
        return Logfile
    def WriteToLog(self,LogFile,Expression,Result,userResult,Status):
        """
        函数功能：
            向日志文件写入信息
        函数返回值：
            无
        """
        f = open(LogFile, 'a+', encoding="utf-8")
        f.writelines(["题目：",Expression,'\t',
                    "正确答案：",Result,'\t',
                    "用户答案：",userResult,'\t',
                    "答案状态：",str(Status), '\n'])
        f.close()


    def CheckResult(self,userResult_str,Result_str):
        """
        函数功能：
            检查计算结果是否正确,计算准确率
        返回值：
            true/false
        """
        #判断是否是空结果
        if userResult_str == "":
            return False
        userResult = float(userResult_str)
        Result = float(Result_str)
        #计算准确率
        if userResult == Result:
            self.RightCounter += 1
            self.Accuracy = self.RightCounter / self.QuestionCounter
            self.Accuracy = "%.2f%%" %(self.Accuracy*100) 
            #print(self.Accuracy)
            return True 
        else :
            self.Accuracy = self.RightCounter / self.QuestionCounter
            self.Accuracy = "%.2f%%" %(self.Accuracy*100)
            #print(self.Accuracy)
            return False






