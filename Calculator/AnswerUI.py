import sys
from UI.AnswerUI import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from function.MainFunction import Calculator 
from PyQt5.QtCore import pyqtSlot




class MyAnswerUI(QtWidgets.QMainWindow, Ui_MainWindow):
    
    def __init__(self, CalClass,LogInfoStruct):
        super(MyAnswerUI,self).__init__()
        self.setupUi(self)
        #self.initUI()
        self.CalClass = CalClass  #Calculator的对象
        self.log = LogInfoStruct  #导入日志信息对象
        self.StartFlag = False  #答题开始标志位
        self.AnswerFlag = False #是否提交答案标志位
        self.EndFlag = False    #答题结束标志位
        #print("myanswer")
    

    @pyqtSlot()
    def NexQuestion(self):
        """
        下一题按钮的槽函数
        """
        if self.CalClass.QuestionCounter <= self.CalClass.QestionNum: #判断答题是否结束
            self.textBrowser_2.clear()  #清空之前的显示内容
            if  self.StartFlag == True:     #判断答题是否开始
                if self.AnswerFlag == True: #判断用户是否提交答案，防止直接跳转下一题
                    self.AnswerFlag = False
                    self.lineEdit.clear()
                    self.log.expression , self.log.result_str = self.CalClass.GetExprssion()  #生成下一题的表达式
                    #显示表达式
                    self.textBrowser.setText(self.log.expression)
                    #更新进度条
                    self.progressBar.setValue(self.CalClass.QuestionCounter)
                else :
                    self.textBrowser_2.setText("请先提交当前答案！") 
                    pass
            else:
                self.textBrowser_2.setText("请点击开始按钮！")
        else: 
            #答题结束显示准确率和提示信息
            self.textBrowser_2.setText("答题结束！" + '\n' + "答题准确率：" + str(self.CalClass.Accuracy))
            self.EndFlag = True #将答题结束标志位，改为true

    @pyqtSlot()
    def Start(self):
        """
        开始答题按钮的槽函数
        """
        self.textBrowser_2.clear()#清楚之前显示的内容
        if self.EndFlag == False:#判断是否结束答题
            if self.StartFlag == False: #开始答题标志，防止误触其他按钮
                self.StartFlag = True
                self.CalClass.QuestionCounter += 1 #答题计数
                #进度条初始化
                self.progressBar.setMaximum(int(self.CalClass.QestionNum))
                self.progressBar.setValue(self.CalClass.QuestionCounter)
                #print(self.CalClass.QuestionCounter)
                self.lineEdit.clear()
                self.log.expression , self.log.result_str = self.CalClass.GetExprssion()
                self.textBrowser.setText(self.log.expression)
            else: 
                self.textBrowser_2.setText("答题已经开始！")
                pass
        else:
            self.textBrowser_2.setText("答题已结束！" + '\n' + "点击结束按钮返回主界面" + '\n' + "答题准确率：" + str(self.CalClass.Accuracy))


    @pyqtSlot()
    def WriteLog(self):
        """
        提交按钮的槽函数
        主要用作写入日志文件
        """
        self.textBrowser_2.clear()#q清除之前的显示信息
        if self.EndFlag == False: #判断是否结束答题
            if self.StartFlag == True and self.AnswerFlag == False :
                if self.lineEdit.text() == "": #判断用户输入结果是否为空
                    self.textBrowser_2.setText("请不要提交空白答案！")
                    pass
                else:
                    self.AnswerFlag = True
                    #print(self.CalClass.QuestionCounter)
                    #日志文件的结构体保存日志信息
                    self.log.UserResult_str = self.lineEdit.text()
                    self.log.LogFile = self.CalClass.LogFile
                    self.log.Status_str = str(self.CalClass.CheckResult(self.log.UserResult_str,self.log.result_str))
                    #写入日志文件              
                    self.CalClass.WriteToLog(
                        self.log.LogFile,
                        self.log.expression,
                        self.log.result_str,
                        self.log.UserResult_str,
                        self.log.Status_str)
                        #显示答题信息和实时准确率
                    Promptmessage = "第" + str(self.CalClass.QuestionCounter) + "题提交成功"
                    self.textBrowser_2.setText(Promptmessage + '\n' +
                                                "当前准确率：" + str(self.CalClass.Accuracy))
                    self.CalClass.QuestionCounter += 1
        else:
            self.textBrowser_2.setText("答题已结束！" + '\n' + "点击结束按钮返回主界面" + '\n' + "答题准确率：" + str(self.CalClass.Accuracy))

       
    @pyqtSlot()
    def End(self):
        """
        写入最终的准确率
        关闭答题界面
        """
        f = open(self.CalClass.LogFile, 'a+', encoding="utf-8")
        f.writelines(["答题准确率：" + '\t' + str(self.CalClass.Accuracy)])
        self.hide()
        


