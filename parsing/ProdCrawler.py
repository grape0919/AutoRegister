import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait       
from selenium.webdriver.common.by import By       
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path

from config.Configuration import Config

import pandas as pd

import time
from log.Logger import Logger


class Crawler:
  downloadPath = Path(__file__)
  downloadPath = str(Path(downloadPath).parent.parent) + "\\data"

  customDataFileName = "ESA001M.xls"
  prodDataFileName = "ESA009M.xls"

  customData = None
  prodData = None

  def __init__(self):
      self.config = Config()

  def run(self):
    # try:
    Logger.debug("downloadPath : "  + self.downloadPath)
    options = webdriver.ChromeOptions()


    options.add_argument("headless")
    options.add_argument("disable-gpu")
    options.add_argument("lang=ko_KR") # 한국어!
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

    options.add_experimental_option("prefs", {
    "download.default_directory": self.downloadPath,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
    })

    driver = webdriver.Chrome("./lib/chromedriver.exe", chrome_options=options)

    driver.get("https://logincc.ecounterp.com/ECERP/LOGIN/ERPLogin?vrqa=mMQ%2Bk8KPqxYEwADSAix%2FmA%3D%3D&vrqb=5456564d5d47535b5b465b4d504d5b4c0f1053535c400f4c5d025d450a4c06545c175d4d005609405a40555b584c4044&vrqc=1")

    driver.implicitly_wait(5)

    #로그인

    driver.find_element_by_xpath("/html/body/div[6]/form/div[1]/div/div[2]/div[1]/div[1]/input").send_keys(self.config.ecountComCode)

    driver.find_element_by_xpath("/html/body/div[6]/form/div[1]/div/div[2]/div[1]/div[2]/input").send_keys(self.config.ecountId)

    driver.find_element_by_xpath("/html/body/div[6]/form/div[1]/div/div[2]/div[1]/div[3]/input[1]").send_keys(self.config.ecountPwd)

    driver.find_element_by_id("save").click()

    driver.implicitly_wait(1)
    try:
    #로그인정보 등록안함 클릭
      driver.find_element_by_xpath("/html/body/div[7]/div[2]/div/div[3]/div/button[2]").click()
    except:
      Logger.warn("로그인 정보 등록 되어있음")
      
    driver.implicitly_wait(5)

    #재고1 -> 기초등록 -> 품목등록

    Logger.debug("재고1 클릭")
    driver.find_element_by_xpath("/html/body/div[7]/div/div[2]/div[2]/div[1]/ul/li[4]/a").click()

    driver.implicitly_wait(1)
    Logger.debug("기초등록 클릭")
    driver.find_element_by_xpath("/html/body/div[7]/div/div[2]/div[2]/div[2]/ul[4]/li[1]/a").click()

    time.sleep(3)
    Logger.debug("품목등록 클릭")
    driver.find_element_by_xpath("/html/body/div[7]/div/div[2]/div[2]/div[3]/ul/li[4]/a").click()

    driver.implicitly_wait(5)
    time.sleep(3)

    Logger.debug("엑셀 클릭")
    excelElement = driver.find_element_by_xpath("/html/body/div[8]/div/div[4]/div[3]/div/div[1]/div[8]/div/button")
    driver.execute_script("arguments[0].click();", excelElement)

    driver.implicitly_wait(5)

    Logger.debug("거래처 등록 클릭")
    driver.find_element_by_xpath("/html/body/div[7]/div/div[2]/div[2]/div[3]/ul/li[1]/a").click()

    driver.implicitly_wait(5)
    time.sleep(8)

    Logger.debug("엑셀 클릭")
    excelElement = driver.find_element_by_xpath("/html/body/div[8]/div/div[4]/div[3]/div/div[1]/div[6]/div/button[1]")
    driver.execute_script("arguments[0].click();", excelElement)

    driver.implicitly_wait(5)
    time.sleep(5)

    driver.close()

    customDataFilePath = Path(self.downloadPath).joinpath(self.customDataFileName)
    Logger.debug(customDataFilePath)
    check_file = customDataFilePath.is_file()
    Logger.debug(check_file)
    
    prodDataFilePath = Path(self.downloadPath).joinpath(self.prodDataFileName)
    Logger.debug(prodDataFilePath)
    check_file = check_file and prodDataFilePath.is_file()
    Logger.debug(check_file)

    if check_file:
      Logger.info("read excel")
      df = pd.read_excel(customDataFilePath,
                sheet_name='거래처등록',
                header=1,
                index_col='거래처명',
                dtype={'거래처코드':str})
      
      Logger.debug("df.A : " + str(df['거래처코드']))

      self.customData = df['거래처코드']

      df = pd.read_excel(prodDataFilePath,
                sheet_name='품목등록',
                header=1,
                index_col='품목명',
                dtype={'품목코드':str})
      
      Logger.debug("df.A : " + str(df['품목코드']))

      self.prodData = df['품목코드']

      print("!@#!@# prodData : ", self.prodData)
      tempSearchKey = df['검색창내용']
      tempV = []
      tempI = []

      self.searchDict = {}

      for idx, value in tempSearchKey.items():
        
        if(type(value) == type('')):
          for key in value.split(' '):
            tempV.append(self.prodData[idx])
            tempI.append(key)

            self.searchDict[key] = idx
            # self.prodData.append(pd.Series([self.prodData[idx]], index=[key]))
      self.searchData = pd.Series(tempV,index=tempI)

      customDataFilePath.unlink()
      prodDataFilePath.unlink()

      if type(self.customData) == type(None) or type(self.prodData) == type(None):
        Logger.error("품목, 거래처 목록을 다운로드 중 문제가 발생하였습니다.")
        return False
      else :
        return True
    else :
      customDataFilePath.unlink()
      prodDataFilePath.unlink()
      Logger.error("다운로드 실패 : " + self.customDataFileName + ", "  + self.prodDataFileName)
      return False
  # except:
  #   Logger.error("품목, 거래처 목록을 다운로드 중 문제가 발생하였습니다.")
  #   return False


  def run2(self):
    return True