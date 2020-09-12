import requests

import re
from data.CarriageData import Data
from log.Logger import Logger

class Parser:

    def __init__(self, loginData1, loginData2, session):
        self.loginData1 = loginData1
        self.loginData2 = loginData2
        self.session = session

    def parse(self, fromDate, toDate):
        
        headers_common = {'Content-Length':'32','Accept':'*/*','X-Requested-With':'XMLHttpRequest','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','Origin':'http://203.247.141.92:8080','Referer':'http://203.247.141.92:8080/SmartLogen/login','Accept-Encoding':'gzip, deflate','Accept-Language':'ko,ko-KR;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6','Connection':'close'}
        
        url = 'http://203.247.141.92:8080/SmartLogen/OrderRecordSelect'
        try:
            post = {'branchCd':self.loginData1,'tradeCd':self.loginData2,'fromDate':fromDate,'toDate':toDate ,'personNm':'','ziphaGb':'A','delieverGb':'A','unsongjangGb':'F'}

        except:
            Logger.error("로젠 로그인 설정이 잘못 되었습니다. ID : ", self.loginData1, " PASSWORD : ", self.loginData2)
            return None
        response = self.session.post(url,data=post,headers=headers_common)
        main_list = response.text.split('≡')
        dataList = []


        sangho_name = ''
        phone = ''
        address = ''
        unsong_address = ''
        first_counter = 0
        for main_data_temp in main_list[:-1]:
            main_id = main_data_temp.split('Ξ')[3]
            url = 'http://203.247.141.92:8080/SmartLogen/SlipInfoSelect'
            post = {'waybillNo':main_data_temp.split('Ξ')[3].replace('-',''),'UserID':self.loginData2}
            response = self.session.post(url,data=post,headers=headers_common)
            main_data=response.text

            date_str = main_data.split('Ξ')[12].replace('-','')
            sangho_name = main_data.split('Ξ')[0]
            phone = main_data.split('Ξ')[3]
            address = main_data.split('Ξ')[2]#+' '+main_data.split('Ξ')[1]
            
            
            splited_prods = re.split('[\,\.]',main_data.split('Ξ')[28])
            prod_datas = ""
            prod_eas = ""
            for prod in splited_prods:
                pd = prod.strip().split(' ')
                prod_datas += str(pd[0]) + "\n"
                if(len(pd) != 2):
                    prod_eas += str(1) + "\n"
                else:
                    try: 
                        ea = int(str(pd[1].replace('개','')))                    
                        prod_eas += str(pd[1].replace('개','')) + "\n"
                    except:
                        prod_datas += pd[1] + "\n"
                        prod_eas += str(1) + "\n" + str(1) + "\n"

                        

            data = Data()

            data.carriageNumber = main_id
            data.IO_DATE = date_str
            data.CUST_DES = sangho_name
            data.phoneNumber = phone
            data.PROD_DES = prod_datas.strip()
            data.QTY = prod_eas.strip()
            data.address = address

            dataList.append(data)

        return dataList