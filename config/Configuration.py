import configparser
import os
from log.Logger import Logger

class Config:
    configFilePath = os.getcwd() + "\\config\\config.properties"

    lozenHeader = "Login.lozen"
    lozenIdKey = "login.lozen.id"
    lozenPwdKey = "login.lozen.pwd"

    ecountHeader = "Login.ecount"
    ecountIdKey = "login.ecount.id"
    ecountPwdKey = "login.ecount.pwd"
    ecountComKey = "login.ecount.comcode"
    ecountApiKeyKey = "ecount.api.key"

    lozenId = ""
    lozenPwd = ""

    lozenLoginData1 = ""
    lozenLoginData2 = ""

    ecountId = ""
    ecountPwd = ""
    ecountComCode = ""
    ecountApiKey = ""

    def __init__(self):
        config = configparser.ConfigParser()
        try :
            config.read(self.configFilePath)
            if (self.lozenHeader in config):
                self.lozenId = config[self.lozenHeader][self.lozenIdKey]
                self.lozenPwd = config[self.lozenHeader][self.lozenPwdKey]
            else:
                Logger.error("LOZEN 로그인 정보 불러오기 실패 : " + self.configFilePath + " 설정을 불러오는데 실패했습니다.")

            Logger.info("ecount login")
            config.read(self.ecountId)
            if (self.ecountHeader in config):
                self.ecountId = config[self.ecountHeader][self.ecountIdKey]
                self.ecountPwd = config[self.ecountHeader][self.ecountPwdKey]
                self.ecountComCode = config[self.ecountHeader][self.ecountComKey]
                self.ecountApiKey = config[self.ecountHeader][self.ecountApiKeyKey]

                Logger.debug("apikey: "  + self.ecountApiKey)

            else:
                Logger.error("ECOUNT 로그인 정보 불러오기 실패 : " + self.configFilePath + " 설정을 불러오는데 실패했습니다.")
        except :
            Logger.error("로그인 정보 불러오기 실패 : " + self.configFilePath + " 설정을 불러오는데 실패했습니다.")
            