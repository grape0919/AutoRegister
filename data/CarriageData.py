
import requests
import json

class Data:
    carriageNumber = "0"
    UPLOAD_SER_NO = "0"
    WH_CD = '00002'
    carriageNumber = "0"
    IO_DATE = 'YYYYMMDD'
    CUST_DES = '상호명'
    sanghoName = '상호명'
    phoneNumber = '000-0000-0000'
    address = '주소'
    item = '품목'
    QTY = '수량'

    def toArray(self):
        array = [self.UPLOAD_SER_NO, self.carriageNumber, self.IO_DATE, self.sanghoName, self.phoneNumber, self.item, self.QTY, self.address]
        return array

    def toJson(self):
        # data = [self.UPLOAD_SER_NO, self.CUST_DES, self.IO_DATE, self.WH_CD]
        data.UPLOAD_SER_NO = self.UPLOAD_SER_NO
        data.CUST_DES = self.sanghoName + " / " + self.phoneNumber + " / " + self.address
        data.IO_DATE = self.IO_DATE
        data.WH_CD = self.WH_CD

        #jsString = { "SaleList": json.dumps({"Line":"0", "BulkDatas":})}

        return json.dumps(data.__dict__)

    def __str__(self):
        return "CarriageData : EMPTY"


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
        post = data.toJson()
        print("post: " , post)
        response = requests.post(self.registrationUrl, data=post, headers=self.headers)
        print("response : " ,response.text)

    def registrationList(self, dataList):
        print("CarriageData Registraion")

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