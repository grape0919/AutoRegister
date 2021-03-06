import sys
from log.Logger import Logger

from AutoRegister import WindowClass

from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt
from view.PrograssDialog import Ui_Form

from login.AutoLogin import AutoLogin
from parsing.ProdCrawler import Crawler


if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)
    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    ## 로그인
    
    Logger.info("login start")
    
    pgDialog = Ui_Form()
    pgDialog.setupUi()
    pgDialog.progLabel.setText("로그인 및 거래처/품목데이터 로딩중..")
    pgDialog.show()
    # pgDialog.start()
    #### 로그인
    loginProcess = AutoLogin()
    ecountDataCrawler = Crawler()

    resultLogin = loginProcess.run()

    if resultLogin[0]:
        
        myWindow.lozenLoginSession = loginProcess.login_session
        myWindow.lozenLoginData1 = resultLogin[1]
        myWindow.lozenLoginData2 = resultLogin[2]
        myWindow.ZONE = resultLogin[3]
        myWindow.SESSION_ID = resultLogin[4]
        
        Logger.debug("### resultLogin : " + str(resultLogin))
        
        Logger.info("login end")
    else :
        pgDialog.close()
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setIcon(QMessageBox.Critical)
        msg.setText("로그인에 실패하여 프로그램을 사용할 수 없습니다.\n config/config.properties 파일의 로그인 정보를 확인해주세요.")
        msg.setDefaultButton(QMessageBox.Escape)
        sys.exit(msg.exec_())

    while(not ecountDataCrawler.run()):
        #msg.setDefaultButton(QMessageBox.Escape)
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setIcon(QMessageBox.Critical)
        msg.setText("이카운트 거래처, 품목데이터를 가져오는데 실패하였습니다. \n 재시도해도 같은 문제 발생 시,\n"+
                "ghdry2563@gmail.com 으로 문의주세요.")
        msg.addButton('재시도', QMessageBox.YesRole)
        msg.addButton('취소', QMessageBox.RejectRole)
        flags = Qt.WindowFlags(Qt.WindowStaysOnTopHint)
        msg.setWindowFlags(flags)

        result = msg.exec_()
        if result == 0:
            continue
        elif result == 1:
            sys.exit()
    
    pgDialog.close()
    
    myWindow.prodSearchData = ecountDataCrawler.searchData
    myWindow.prodSearchDict = ecountDataCrawler.searchDict
    myWindow.prodCodeData = ecountDataCrawler.prodData
    myWindow.customCodeData = ecountDataCrawler.customData
    
    #데이터 뿌리기
    # myWindow.reflash()

    #프로그램 화면을 보여주는 코드
    myWindow.show()



    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()