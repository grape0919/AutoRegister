
import sys
from PyQt5.QtWidgets import QCheckBox, QTableWidgetItem
from PyQt5.QtCore import Qt

from view.main import Ui_MainWindow
from data.CarriageData import Register
from parsing.LozenParser import Parser
from view.PrograssDialog import Ui_Form
from log.Logger import Logger
class WindowClass(Ui_MainWindow) :

    lozenLoginData1 = ""
    lozenLoginData2 = ""
    ZONE = ""
    SESSION_ID = ""

    is_progressing = False

    prodCodeData = None
    customCodeData = None
    prodSearchData = None
    prodSearchDict = None

    def __init__(self) :
        super(WindowClass, self).__init__()
        self.setupUi(self)
        
        # 조회 버튼 클릭 이벤트
        self.inquiryButton.clicked.connect(self.clickInquiryButton)
        self.registButton.clicked.connect(self.clickRegistrationButton)

    def progressing(self):
        Logger.info("startProgressing")
        self.is_progressing = True
        
        pgDialog = Ui_Form()
        pgDialog.setupUi()
        pgDialog.progLabel.setText("데이터 크롤링 중..")
        # process = False
        
        Logger.info("stopProgressing")

    def reflash(self):
        Logger.info("reflash")
        #TODO: start progress
        # pg = Thread(target=self.progressing)
        # pg.start()
        #크롤링
        crawler = Parser(self.lozenLoginData1, self.lozenLoginData2, self.lozenLoginSession)
        
        ddate = str(self.fromDateEdit.date().toPyDate())
        fromDate = "".join(ddate.split("-"))

        ddate = str(self.toDateEdit.date().toPyDate())
        toDate = "".join(ddate.split("-"))
        self.dataList = crawler.parse(fromDate, toDate)

        self.spreadData(self.dataList)

        #TODO: STOP PROGRESS
        # self.is_progressing = False

    def spreadData(self, datas):
        Logger.info("spreadData")
    
        # self.model = QStandardItemModel()
        # self.model.setColumnCount(5)
        # self.model.setHorizontalHeaderLabels(["","주문번호","운송장번호", "날짜", "상호", "전화번호", "상품", "수량", "주소"])
        
        self.tableView.setColumnCount(9)
        self.tableView.setRowCount(len(datas))
        self.tableView.clicked.connect(self.clickTable)
    
        #크롤링 된 데이터를 tableView에 뿌릴 model 생성
        
        rowSet = []
        
        tempDate = ""
        upload_count = 0

        for index, data in enumerate(datas):

            # 등록된 데이터 체크해서 Enabled 시키키
            item = self.MyQTableWidgetItemCheckBox()
            self.tableView.setItem(index, 0, item)
            chbox = self.MyCheckBox(item)
            self.tableView.setCellWidget(index, 0, chbox)
            

            for i,d in enumerate(data.toArray()):
                # if(i == 0):
                #     if tempDate != data.IO_DATE:
                #         tempDate = data.IO_DATE
                #         upload_count=1
                #     else :
                #         upload_count+=1

                #     data.UPLOAD_SER_NO = tempDate+"_"+str(upload_count)
                #     d = data.UPLOAD_SER_NO
                if(i == 2):
                    try:
                        code = self.customCodeData[d]
                    except KeyError:
                        code = "TRA2008008" #택배
                        
                    
                    data.CUST = code
                elif(i == 4):
                    rowSet.append((index, d.count('\n')))
                    data.PROD_DES = data.PROD_DES.split('\n')
                    code = []
                    for idx, prodNm in enumerate(data.PROD_DES):
                        try:
                            code.append(self.prodCodeData[prodNm])
                        except KeyError:
                            try:
                                code.append(self.prodSearchData[prodNm])
                                data.PROD_DES[idx] = self.prodSearchDict[prodNm]
                            except:
                                code.append("ECO14_05_04")
                    
                    data.PROD_CD = code
                    data.QTY = data.QTY.split('\n')

                item = QTableWidgetItem(d)
                self.tableView.setItem(index, i+1, item)
        
        #품목 개수에 따라 행 높이 조절
        for row in rowSet:
            self.tableView.setRowHeight(row[0], 40+(row[1]*20))

    def clickTable(self):
        Logger.info("click table view")

    def clickInquiryButton(self): 
        Logger.info("pressed InquiryButton")
        self.reflash()

    def clickRegistrationButton(self): 
        Logger.info("pressed RegistryButton")
        register = Register(self.ZONE, self.SESSION_ID)
        # model = self.tableView.model()
        # print("model : ", model)
        data = []
        if self.tableView.rowCount() > 0:
            for row in range(self.tableView.rowCount()):
                if(self.tableView.item(row, 0).text() == "0"):
                    continue
                else :
                    self.dataList[row].checkValue = "2"
                    data.append(self.dataList[row])
        
        register.registrationList(data)


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
            Logger.debug("checkbox row= " + str(self.get_row()))
            Logger.debug("checkValue : " + str(self.mycheckvalue))
            Logger.debug("self " + str(self.objectName))

            # item = QTableWidgetItem("True")
            # self.item.setItem(self.get_row(), "True")
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
            Logger.debug("my setdata " + str(value)) 
            self.setData(Qt.UserRole, value)
            Logger.debug("row " + str(self.row()))
            Logger.debug("self.data : " + str(self.data(Qt.UserRole)))

        def text(self):
            return str(self.data(Qt.UserRole))

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