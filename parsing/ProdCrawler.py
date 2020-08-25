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
downloadPath = downloadPath + "\\..\\..\\data"
downloadPath = str(Path(downloadPath).absolute())

print("downloadPath: " + downloadPath)

options = webdriver.ChromeOptions()

options.add_argument("disable-gpu")
options.add_argument("lang=ko_KR") # 한국어!
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

options.add_experimental_option("prefs", {
  "download.default_directory": r"./data/",
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True
})

browser = webdriver.Chrome("./resources/chromedriver.exe", chrome_options=options)

browser.get("https://logincc.ecounterp.com/ECERP/LOGIN/ERPLogin?vrqa=mMQ%2Bk8KPqxYEwADSAix%2FmA%3D%3D&vrqb=5456564d5d47535b5b465b4d504d5b4c0f1053535c400f4c5d025d450a4c06545c175d4d005609405a40555b584c4044&vrqc=1")

browser.implicitly_wait(5)

#로그인

browser.find_element_by_xpath("/html/body/div[6]/form/div[1]/div/div[2]/div[1]/div[1]/input").send_keys("66525")

browser.find_element_by_xpath("/html/body/div[6]/form/div[1]/div/div[2]/div[1]/div[2]/input").send_keys("PARCEL")

browser.find_element_by_xpath("/html/body/div[6]/form/div[1]/div/div[2]/div[1]/div[3]/input[1]").send_keys("skdlszh9")

browser.find_element_by_id("save").click()

time.sleep(1)

#로그인정보 등록안함 클릭
browser.find_element_by_xpath("/html/body/div[7]/div[2]/div/div[3]/div/button[2]").click()

browser.implicitly_wait(5)

time.sleep(1)
#재고1 -> 기초등록 -> 품목등록

print("재고1 클릭")
browser.find_element_by_xpath("/html/body/div[7]/div/div[2]/div[2]/div[1]/ul/li[4]/a").click()

time.sleep(1)
print("기초등록 클릭")
browser.find_element_by_xpath("/html/body/div[7]/div/div[2]/div[2]/div[2]/ul[4]/li[1]/a").click()

time.sleep(1)
print("품목등록 클릭")
browser.find_element_by_xpath("/html/body/div[7]/div/div[2]/div[2]/div[3]/ul/li[4]/a").click()

browser.implicitly_wait(5)
time.sleep(2)

print("엑셀 클릭")
excelElement = browser.find_element_by_xpath("/html/body/div[8]/div/div[4]/div[3]/div/div[1]/div[8]/div/button")
webdriver.ActionChains(browser).move_to_element(excelElement).click(excelElement).perform()

# browser.execute_script("arguments[0].click();", WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div[4]/div[3]/div/div[1]/div[8]/div/button"))))
#browser.execute_script("arguments[0].click();", excelElement)

time.sleep(200)


