import sys
from function.MainFunction import Calculator
from MainUI import MyMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from AnswerUI import MyAnswerUI
from function.MainFunction import Type

class LogInfoStruct:
    """
    保存写入log文件的参数
    """
    def __init__(self):
        self.LogFile = "" #log文件的路径
        self.expression = ""    #表达式
        self.result_str = ""    #正确结果
        self.UserResult_str = ""    #用户结果
        self.Status_str = ""    #答题是否正确

def main():
    app =  QtWidgets.QApplication(sys.argv)
    MyCalculator = Calculator()
    MyLog = LogInfoStruct()
    AnswerUI = MyAnswerUI(MyCalculator, MyLog)
    win = MyMainWindow(AnswerUI)
    win.show()
    sys.exit(app.exec_())
    
    
if __name__ == "__main__":
    main()