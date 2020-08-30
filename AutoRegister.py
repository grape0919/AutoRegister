import sys
from PyQt5.QtWidgets import QCheckBox, QTableWidgetItem
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
from view.main import Ui_MainWindow
import static.staticValues as staticValue
from data.CarriageData import Data, Register
from parsing.LozenParser import Parser
from view.PrograssDialog import Ui_Form
from threading import Thread
import re

class WindowClass(Ui_MainWindow) :

    lozenLoginData1 = ""
    lozenLoginData2 = ""
    ZONE = ""
    SESSION_ID = ""

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
        # pg = Thread(target=self.progressing)
        # pg.start()
        #크롤링
        crawler = Parser(self.lozenLoginData1, self.lozenLoginData2, self.lozenLoginSession)
        
        ddate = str(self.fromDateEdit.date().toPyDate())
        fromDate = "".join(ddate.split("-"))

        ddate = str(self.toDateEdit.date().toPyDate())
        toDate = "".join(ddate.split("-"))
        dataList = crawler.parse(fromDate, toDate)

        self.spreadData(dataList)

        #TODO: STOP PROGRESS
        # self.is_progressing = False

    def spreadData(self, datas):
        print("spreadData")
    
        self.model = QStandardItemModel()
        self.model.setColumnCount(5)
        self.model.setHorizontalHeaderLabels(["","주문번호","운송장번호", "날짜", "상호", "전화번호", "상품", "수량", "주소"])
        
        self.tableView.clicked.connect(self.clickTable)
    
        #크롤링 된 데이터를 tableView에 뿌릴 model 생성
        
        rowSet = []
        for index, data in enumerate(datas):

            # 등록된 데이터 체크해서 Enabled 시키키
            items = []
            # item = QStandardItem()
            # item.setCheckable(True)
            # enable = True
            
            # item.setCheckState(not enable)
            # item.setEnabled(enable)

            item = self.MyQTableWidgetItemCheckBox()
            self.tableView.setItem(index, 0, item)
            chbox = self.MyCheckBox(item)
            # print(chbox.sizeHint())
            self.tableView.setCellWidget(index, 0, chbox)
            

            # items.append(item)

            #품목 개수에 따라 행 높이 조절
            for i,d in enumerate(data.toArray()):
                # print("data : ", d)
                if i == 5 and ('\n' in d):
                    # print("datas : ", d.count('\n'))
                    rowSet.append((index, d.count('\n')))
                # item = QS(tandardItem(d)
                print("d:",d)
                item = QTableWidgetItem(d)
                print("item:",item)
                self.tableView.setItem(index, i, item)
                # item.setEnabled(enable)
                # items.append(item)
                
            # self.model.appendRow(items)

        # self.tableView.setModel(self.model) 
        
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
        # index = self.tableView.currentIndex()
        # newIndex = self.tableView.model().index(index.row(), 1)
        # print("newIndex", newIndex)
        # print("index", self.tableView.model().data(newIndex))

    def clickInquiryButton(self): 
        print("pressed InquiryButton")
        self.reflash()

    def clickRegistrationButton(self): 
        print("pressed RegistryButton")
        register = Register(self.ZONE, self.SESSION_ID)
        model = self.tableView.model()
        print("model : ", model)
        data = []
        if model :
            if model.rowCount() > 0:
                for row in range(model.rowCount()):
                    checkBox = self.findChild(QCheckBox, "DataListCheckBox_1")
                    print("check box : " + checkBox.isChecked())

                for row in range(model.rowCount()):
                    data.append([])
                    for column in range(model.columnCount()):
                        index = model.index(row, column)
                        # We suppose data are strings
                        print("index : ", index)
                        print("index data : ", model.data(index))
                        data[row].append(str(model.data(index)))

        print("Datas : ", data)


    class MyCheckBox(QCheckBox): 
        def __init__(self, item): 
            """ :param item: QTableWidgetItem instance """ 
            super().__init__() 
            self.item = item 
            self.mycheckvalue = 0 
            # 0 --> unchecked, 2 --> checked 
            self.stateChanged.connect(self.__checkbox_change) 
            self.stateChanged.connect(self.item.my_setdata) 
            # checked 여부로 정렬을 하기위한 data 저장 

        def __checkbox_change(self, checkvalue): 
            # print("myclass...check change... ", checkvalue) 
            self.mycheckvalue = checkvalue 
            print("checkbox row= ", self.get_row()) 

        def get_row(self): 
            return self.item.row()

    class MyQTableWidgetItemCheckBox(QTableWidgetItem):
        """
        checkbox widget 과 같은 cell 에 item 으로 들어감. 
        checkbox 값 변화에 따라, 사용자정의 data를 기준으로 정렬 기능 구현함.
        """ 
        def __init__(self): 
            super().__init__() 
            self.setData(Qt.UserRole, 0)
        
        def __lt__(self, other): 
            # print(type(self.data(Qt.UserRole))) 
            return self.data(Qt.UserRole) < other.data(Qt.UserRole) 

        def my_setdata(self, value): 
            # print("my setdata ", value) 
            self.setData(Qt.UserRole, value)
            #print("row ", self.row())



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