import configparser
import os
import time
import requests
import json
import sys
from config.Configuration import Config

class AutoLogin:

    headers_common = {'Content-Length':'32','Accept':'*/*','X-Requested-With':'XMLHttpRequest','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','Origin':'http://203.247.141.92:8080','Referer':'http://203.247.141.92:8080/SmartLogen/login','Accept-Encoding':'gzip, deflate','Accept-Language':'ko,ko-KR;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6','Connection':'close'}

    def __init__(self):
        self.login_session = requests.Session()
        self.config = Config()

    def lozenLogin(self):
        print("lozenLogin")
        
        url = 'http://203.247.141.92:8080/SmartLogen/UserLogin'
        post = {'userid':self.config.lozenId,'userpw':self.config.lozenPwd}
        try:
            response = self.login_session.post(url,data=post,headers=self.headers_common)
        except:
            print("lozen 로그인 중 네트워크 연결에 문제가 있습니다. ")
            sys.exit()
        print("response", response.text)
        login_data = response.text.split('Ξ')
        self.lozenLoginData1 = login_data[1]
        self.lozenLoginData2 = login_data[3]


    def ecountLogin(self):
        print("ecountLogin")
        url = 'https://oapi.ecounterp.com/OAPI/V2/Zone'
        print("COM_CODE : ", self.config.ecountComCode)
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        post = {'COM_CODE': self.config.ecountComCode}
        
        try:
            response = requests.post(url, data=json.dumps(post), headers=headers)
        except:
            print("ecount 로그인 중 네트워크 연결에 문제가 있습니다. ")
            sys.exit()

        print("response", response.json)
        print("Data : ", response.json()["Data"]["ZONE"])
        self.ZONE = response.json()["Data"]["ZONE"]

        url = 'https://oapi{ZONE}.ecounterp.com/OAPI/V2/OAPILogin'.format(ZONE=self.ZONE)
        post = {'COM_CODE': self.config.ecountComCode, 'USER_ID':self.config.ecountId, 'API_CERT_KEY':self.config.ecountApiKey, 'LAN_TYPE':'ko-KR', 'ZONE':self.ZONE}
        response = requests.post(url, data=json.dumps(post), headers=headers)

        self.SESSION_ID = response.json()["Data"]["Datas"]["SESSION_ID"]
        

    def run(self):
        print("run")
        self.lozenLogin()
        self.ecountLogin()

        if self.lozenLoginData1 == "" or self.lozenLoginData2 == "" or self.ZONE == "" or self.SESSION_ID == "" :
            returnVal = (False)
        else :
            returnVal = (True, self.lozenLoginData1, self.lozenLoginData2, self.ZONE, self.SESSION_ID)
        return returnVal
