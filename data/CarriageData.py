
from logging import error
import requests
import json
from log.Logger import Logger
from PyQt5.QtWidgets import QMessageBox
class Data:
    checkValue = "0"
    carriageNumber = "0"
    # UPLOAD_SER_NO = "0" #필수
    WH_CD = '00002' #필수
    carriageNumber = "0"
    IO_DATE = 'YYYYMMDD'
    CUST_DES = '거래처 명'
    CUST = '거래처 코드'
    phoneNumber = '000-0000-0000'
    address = '주소'
    PROD_DES = '품목'
    PROD_CD = '품목 코드'  #필수
    QTY = '수량' #필수

    def toArray(self):
        array = [self.carriageNumber, self.IO_DATE, self.CUST_DES, self.phoneNumber, self.PROD_DES, self.QTY, self.address, self.PROD_CD]
        return array

    def __str__(self):
        return "CarriageData : EMPTY"
    
    def __repr__(self):
        return (str(self.toArray()))


class Register:
    headers = {'Content-Type': 'application/json; charset=utf-8'}

    registrationUrl = 'https://oapi{ZONE}.ecounterp.com/OAPI/V2/Sale/SaveSale?SESSION_ID={SESSION_ID}'
    inquiryUrl = 'https://oapi{ZONE}.ecounterp.com/OAPI/V2/InventoryBasic/GetBasicProduct?SESSION_ID={SESSION_ID}'

    def __init__(self, ZONE, SESSION_ID):
        Logger.info("CarriageRegister.init")
        self.ZONE = ZONE
        self.SESSION_ID = SESSION_ID
        self.registrationUrl = self.registrationUrl.format(ZONE=self.ZONE, SESSION_ID=self.SESSION_ID)
        self.inquiryUrl = self.inquiryUrl.format(ZONE=self.ZONE, SESSION_ID=self.SESSION_ID)


    def registration(self, data):
        Logger.info("CarriageData Registraion")

        post = """{
                    "SaleList": ["""
        for i in range(len(data.PROD_CD)):
            post +=     """
                        {{
                            "Line": "0",
                            "BulkDatas": {{
                            "IO_DATE": "{IO_DATE}",
                            "UPLOAD_SER_NO": "",
                            "CUST": "{CUST}",
                            "CUST_DES": "{CUST_DES2}",
                            "WH_CD": "00002",
                            "PROD_CD": "{PROD_CD}",
                            "PROD_DES": "{PROD_DES}",
                            "QTY": "{QTY}",
                            "U_MEMO3": "{CUST_DES1} / {PHONE}",
                            "U_MEMO4": "{ADDRESS}",
                            "U_MEMO5": "{ECT}",
                            }}
                        }}
                        """.format(IO_DATE=data.IO_DATE, CUST=data.CUST, CUST_DES2=data.CUST_DES if data.CUST != "TRA2008008" else "택배발송",# UPLOAD_SER_NO=data.UPLOAD_SER_NO
                     CUST_DES1 = data.CUST_DES, PROD_CD=data.PROD_CD[i], PROD_DES=data.PROD_DES[i], QTY=data.QTY[i], PHONE=data.phoneNumber
                     , ADDRESS=data.address, ECT="")
            if(i != len(data.PROD_CD)-1):
                post += """,
                        """

        post += """]
                }"""
        post = post.encode("utf-8")
        Logger.debug("post: "  + str(post))
        response = requests.post(self.registrationUrl, data=post, headers=self.headers)
        Logger.debug("response : " + response.text)
        status = response.json()["Status"]
        success_cnt = ""
        fail_cnt = ""
        error_msg = ""

        if(status == "200"):
            success_cnt = response.json()["Data"]["SuccessCnt"]
            fail_cnt = response.json()["Data"]["FailCnt"]
            return (True, success_cnt, fail_cnt)
        else:
            error_msg = response.json()["Error"]["Message"]
            return (False, error_msg)

    def registrationList(self, dataList):
        Logger.info("CarriageData List Registraion")
        Logger.debug("regist Data List : " + str(dataList))
        check_resp = []
        c = False
        for d in dataList:
            a = self.registration(d)
            if not a[0]:
                check_resp.append(a[1])

        msg = QMessageBox()
        if len(check_resp) > 0:
            msg.setWindowTitle("판매 등록 실패")
            msg.setIcon(QMessageBox.Critical)
            msg.setText("판매 등록에 실패 했습니다. 아래 리스트를 확인해주세요.\n"+"\n".join(check_resp))
        else :
            msg.setWindowTitle("판매 등록 성공")
            msg.setIcon(QMessageBox.Information)
            msg.setText("판매 등록에 성공 했습니다.")


        msg.setDefaultButton(QMessageBox.Escape)
        msg.exec_()

    def inquiryProduct(self, prodNm):
        return 0

if __name__ == "__main__" :
    ZONE = "CC"
    SESSION_ID = "36363532357c50415243454c:CC-AN16HBmxKKJ49"
    reg = Register(ZONE, SESSION_ID)

    data = Data()
    data.UPLOAD_SER_NO = "0"
    data.WH_CD = '00002'
    data.carriageNumber = "0"
    data.IO_DATE = '20200816'
    data.CUST_DES = '테스트고객정보'
    data.phoneNumber = '000-0000-0000'
    data.address = '주소'
    data.item = '품목'
    data.QTY = '5'

    # print(data.__dict__)

    Logger.info(data.toJson())
    reg.registration(data)
    # reg.registration(data)