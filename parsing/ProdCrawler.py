import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait       
from selenium.webdriver.common.by import By       
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import time
import os

downloadPath = os.path.abspath(__file__)
downloadPath = str(Path(downloadPath).parent)

print("downloadPath: " + downloadPath)

options = webdriver.ChromeOptions()

options.add_argument("disable-gpu")
options.add_argument("lang=ko_KR") # 한국어!
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

options.add_experimental_option("prefs", {
  "download.default_directory": downloadPath,
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True
})

driver = webdriver.Chrome("./resources/chromedriver.exe", chrome_options=options)

driver.get("https://logincc.ecounterp.com/ECERP/LOGIN/ERPLogin?vrqa=mMQ%2Bk8KPqxYEwADSAix%2FmA%3D%3D&vrqb=5456564d5d47535b5b465b4d504d5b4c0f1053535c400f4c5d025d450a4c06545c175d4d005609405a40555b584c4044&vrqc=1")

driver.implicitly_wait(5)

#로그인

driver.find_element_by_xpath("/html/body/div[6]/form/div[1]/div/div[2]/div[1]/div[1]/input").send_keys("66525")

driver.find_element_by_xpath("/html/body/div[6]/form/div[1]/div/div[2]/div[1]/div[2]/input").send_keys("PARCEL")

driver.find_element_by_xpath("/html/body/div[6]/form/div[1]/div/div[2]/div[1]/div[3]/input[1]").send_keys("skdlszh9")

driver.find_element_by_id("save").click()

driver.implicitly_wait(1)

#로그인정보 등록안함 클릭
driver.find_element_by_xpath("/html/body/div[7]/div[2]/div/div[3]/div/button[2]").click()

driver.implicitly_wait(5)

driver.implicitly_wait(1)
#재고1 -> 기초등록 -> 품목등록

print("재고1 클릭")
driver.find_element_by_xpath("/html/body/div[7]/div/div[2]/div[2]/div[1]/ul/li[4]/a").click()

driver.implicitly_wait(1)
print("기초등록 클릭")
driver.find_element_by_xpath("/html/body/div[7]/div/div[2]/div[2]/div[2]/ul[4]/li[1]/a").click()

time.sleep(3)
print("품목등록 클릭")
driver.find_element_by_xpath("/html/body/div[7]/div/div[2]/div[2]/div[3]/ul/li[4]/a").click()

driver.implicitly_wait(5)
time.sleep(3)

print("엑셀 클릭")
excelElement = driver.find_element_by_xpath("/html/body/div[8]/div/div[4]/div[3]/div/div[1]/div[8]/div/button")
driver.execute_script("arguments[0].click();", excelElement)

driver.implicitly_wait(5)

print("거래처 등록 클릭")
driver.find_element_by_xpath("/html/body/div[7]/div/div[2]/div[2]/div[3]/ul/li[1]/a").click()

driver.implicitly_wait(5)
time.sleep(5)

print("엑젤 클릭")
excelElement = driver.find_element_by_xpath("/html/body/div[8]/div/div[4]/div[3]/div/div[1]/div[6]/div/button[1]")
driver.execute_script("arguments[0].click();", excelElement)

driver.implicitly_wait(5)
time.sleep(5)


