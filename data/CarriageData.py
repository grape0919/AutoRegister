
import requests
import json

class Data:
    checkValue = "0"
    carriageNumber = "0"
    UPLOAD_SER_NO = "0" #필수
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
        array = [self.UPLOAD_SER_NO, self.carriageNumber, self.IO_DATE, self.CUST_DES, self.phoneNumber, self.PROD_DES, self.QTY, self.address, self.PROD_CD]
        return array

    def toJson(self):
        data = [self.UPLOAD_SER_NO, self.CUST_DES, self.IO_DATE, self.WH_CD]
        data.UPLOAD_SER_NO = self.UPLOAD_SER_NO
        data.CUST_DES = self.CUST_DES
        data.IO_DATE = self.IO_DATE
        data.WH_CD = self.WH_CD

        # if type(self.PROD_DES) == type(list):


        # jsString = { "SaleList": {"Line":"0", "BulkDatas":json.(datas)})}

        return ""#json.dumps(data.__dict__)

    def __str__(self):
        return "CarriageData : EMPTY"
    
    def __repr__(self):
        return (str(self.toArray()))


class Register:
    headers = {'Content-Type': 'application/json; charset=utf-8'}

    registrationUrl = 'https://oapi{ZONE}.ecounterp.com/OAPI/V2/Sale/SaveSale?SESSION_ID={SESSION_ID}'
    inquiryUrl = 'https://oapi{ZONE}.ecounterp.com/OAPI/V2/InventoryBasic/GetBasicProduct?SESSION_ID={SESSION_ID}'

    def __init__(self, ZONE, SESSION_ID):
        print("CarriageRegister.init")
        self.ZONE = ZONE
        self.SESSION_ID = SESSION_ID
        self.registrationUrl = self.registrationUrl.format(ZONE=self.ZONE, SESSION_ID=self.SESSION_ID)
        self.inquiryUrl = self.inquiryUrl.format(ZONE=self.ZONE, SESSION_ID=self.SESSION_ID)


    def registration(self, data):
        print("CarriageData Registraion")

        post = """{{
                    "SaleList": ["""
        for i in range(len(data.PROD_CD)):
            post +=     """
                        {{
                            "Line": "0",
                            "BulkDatas": {{
                            "IO_DATE": "{IO_DATE}",
                            "UPLOAD_SER_NO": "",
                            "CUST": "{CUST}",
                            "CUST_DES": "{CUST_DES}",
                            "WH_CD": "00002",
                            "PROD_CD": "{PROD_CD}",
                            "PROD_DES": "{PROD_DES}",
                            "QTY": "{QTY}",
                            "U_MEMO3": "{CUST_DES} / {PHONE}",
                            "U_MEMO4": "{ADDRESS}",
                            "U_MEMO5": "{ECT}",
                            }}
                        }}
                        """.format(IO_DATE=data.IO_DATE, CUST=data.CUST, CUST_DES=data.CUST_DES,# UPLOAD_SER_NO=data.UPLOAD_SER_NO
                     PROD_CD=data.PROD_CD[i], PROD_DES=data.PROD_DES[i], QTY=data.QTY[i], PHONE=data.phoneNumber
                     , ADDRESS=data.address, ECT="")
            if(i != len(data.PROD_CD)-1):
                post += ",\n"

        post += """]
                }}""".encode("utf-8")
        print("post: " , post)
        response = requests.post(self.registrationUrl, data=post, headers=self.headers)
        print("response : " ,response.text)

    def registrationList(self, dataList):
        print("CarriageData List Registraion")
        print("regist Data List : ", dataList)
        for d in dataList:
            self.registration(d)

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

    print(data.toJson())
    reg.registration(data)
    # reg.registration(data)