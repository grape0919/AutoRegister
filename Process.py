import sys

from AutoRegister import WindowClass

from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QProgressDialog
from view.PrograssDialog import Ui_Form

from login.AutoLogin import AutoLogin

import threading

import time


if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)
    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    ## 로그인
    
    print("login start")
    pgDialog = Ui_Form()
    pgDialog.setupUi()
    pgDialog.progLabel.setText("로그인 중..")
    pgDialog.show()
    # pgDialog.start()
    #### 로그인
    loginProcess = AutoLogin()

    resultLogin = loginProcess.run()
    if resultLogin[0] :
        pgDialog.close()
        myWindow.lozenLoginSession = loginProcess.login_session
        myWindow.lozenLoginData1 = resultLogin[1]
        myWindow.lozenLoginData2 = resultLogin[2]
        myWindow.ZONE = resultLogin[3]
        myWindow.SESSION_ID = resultLogin[4]
        
        print("### resultLogin : ", resultLogin)
    else :
        pgDialog.close()
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setIcon(QMessageBox.Critical)
        msg.setText("로그인에 실패하여 프로그램을 사용할 수 없습니다.\n config/config.properties 파일의 로그인 정보를 확인해주세요.")
        msg.setDefaultButton(QMessageBox.Escape)
        sys.exit(msg.exec_())

    
    print("login end")
    #데이터 뿌리기
    # myWindow.reflash()

    #프로그램 화면을 보여주는 코드
    myWindow.show()



    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()