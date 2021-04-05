import sys
from UI.MainWindow import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from function.MainFunction import Calculator
from function.MainFunction import Type 
from PyQt5.QtCore import pyqtSlot
from AnswerUI import MyAnswerUI

#答题类型和范围的词典，用于用户输入和代码需要类型的转换
TypeDic = {'加减运算':Type.add_sub,'乘除运算':Type.mul_div,'混合运算':Type.mix}
RangDic = {'10以内':10,'100以内':100}

class MyMainWindow(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self,answerUI):
        super(MyMainWindow,self).__init__()
        self.setupUi(self)
        """self.CalClass = CalClass
        self.Log = Log"""
        self.answerUI = answerUI


    @pyqtSlot()
    def QuestionInit(self):
        """
        开始答题按钮的槽函数
        用于读入用户的参数，显示主界面
        """
        self.answerUI.CalClass.QestionNum = int(self.lineEdit.text())
        self.answerUI.CalClass.ElementNum = int(self.lineEdit_2.text())
        self.answerUI.CalClass.QuestionType = TypeDic[self.comboBox.currentText()] 
        self.answerUI.CalClass.NumRange = RangDic[self.comboBox_2.currentText()]
        self.answerUI.show()


        




