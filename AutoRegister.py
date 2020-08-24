import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from view.main import Ui_MainWindow
import static.staticValues as staticValues
from data.CarriageData import Data, Register
from parsing.LozenParser import Parser
from view.PrograssDialog import Ui_Form
from threading import Thread
import re

class WindowClass(Ui_MainWindow) :

    lozenLoginData1 = ""
    lozenLoginData2 = ""
    
    is_progressing = False

    def __init__(self) :
        super(WindowClass, self).__init__()
        self.setupUi(self)
        
        # 조회 버튼 클릭 이벤트
        self.inquiryButton.clicked.connect(self.clickInquiryButton)
        self.registButton.clicked.connect(self.clickRegistrationButton)

    def progressing(self):
        print("startProgressing")
        self.is_progressing = True
        
        pgDialog = Ui_Form()
        pgDialog.setupUi()
        pgDialog.progLabel.setText("데이터 크롤링 중..")
        process = False
        
        print("stopProgressing")

    def reflash(self):
        print("reflash")
        #TODO: start progress
        pg = Thread(target=self.progressing)
        pg.start()
        #크롤링
        crawler = Parser(self.lozenLoginData1, self.lozenLoginData2, self.lozenLoginSession)
        
        ddate = str(self.fromDateEdit.date().toPyDate())
        fromDate = "".join(ddate.split("-"))

        ddate = str(self.toDateEdit.date().toPyDate())
        toDate = "".join(ddate.split("-"))
        dataList = crawler.parse(fromDate, toDate)

        self.spreadData(dataList)

        #TODO: STOP PROGRESS
        self.is_progressing = False

    def spreadData(self, datas):
        print("spreadData")
    
        self.model = QtGui.QStandardItemModel()
        self.model.setColumnCount(5)
        self.model.setHorizontalHeaderLabels(["","주문번호","운송장번호", "날짜", "상호", "전화번호", "상품", "수량", "주소"])
        
        self.tableView.clicked.connect(self.clickTable)
    
        #크롤링 된 데이터를 tableView에 뿌릴 model 생성
        
        rowSet = []
        for index, data in enumerate(datas):

            # 등록된 데이터 체크해서 Enabled 시키키
            items = []
            item = QtGui.QStandardItem()
            item.setCheckable(True)

            enable = True
            
            item.setCheckState(not enable)
            item.setEnabled(enable)

            items.append(item)

            #품목 개수에 따라 행 높이 조절
            for i,d in enumerate(data.toArray()):
                # print("data : ", d)
                if i == 5 and ('\n' in d):
                    # print("datas : ", d.count('\n'))
                    rowSet.append((index, d.count('\n')))
                item = QtGui.QStandardItem(d)
                item.setEnabled(enable)
                items.append(item)
                
            self.model.appendRow(items)

        self.tableView.setModel(self.model) 
        
        print("rowSet: " , rowSet)
        for row in rowSet:
            self.tableView.setRowHeight(row[0], 40+(row[1]*40))

        self.tableView.setColumnWidth(0, 10)
        self.tableView.setColumnWidth(1, 80)
        self.tableView.setColumnWidth(2, 80)
        self.tableView.setColumnWidth(3, 80)

        self.tableView.setColumnWidth(4, 150)
        self.tableView.setColumnWidth(5, 120)

        self.tableView.setColumnWidth(7, 40)
        self.tableView.setColumnWidth(8, 250)

    def clickTable(self):
        print("click table view")
        index = self.tableView.currentIndex()
        newIndex = self.tableView.model().index(index.row(), 1)
        print("newIndex", newIndex)
        print("index", self.tableView.model().data(newIndex))

    def clickInquiryButton(self): 
        print("pressed InquiryButton")
        self.reflash()

    def clickRegistrationButton(self): 
        print("pressed RegistryButton")
        register = Register(ZONE, SESSION_ID)

        
        


if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    myWindow.reflash()
    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()