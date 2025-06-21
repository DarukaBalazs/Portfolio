from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.common.exceptions import NoSuchElementException
import time
import string
import xlsxwriter
import os
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen


class Dentist:
    def __init__(self):
        self.name = ""
        self.address = ""
        self.email = ["Nincs"]
        self.phone = ""
    def kimenet(self):
        self.address = self.address[4:]
        self.email = self.email[0]
        self.phone = self.phone[13:]

def extract_emails(url):
    response = urlopen(url).read()
    time.sleep(5)   
    soup = BeautifulSoup(response, features='html.parser')
    time.sleep(2)
    # Use a regular expression to find email addresses
    emails = re.findall(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4})', soup.get_text())
    if len(emails)==0:
        return ["Nincs"]
    else:
        return emails
#google megnyitás
driver = webdriver.Chrome()
wait = WebDriverWait(driver,5)

#google maps megnyitása
driver.get("https://www.google.com/maps")
time.sleep(6)

#sütik elfogadás
widget = driver.find_element(By.XPATH,'//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button')
widget.click()

#fogorvosok keresése
driver.switch_to.default_content()
searchbox = driver.find_element(By.ID,"searchboxinput")
location = "Budapest fogorvos"
searchbox.send_keys(location)
searchbox.send_keys(Keys.ENTER)
time.sleep(10)

divSideBar=driver.find_element(By.CSS_SELECTOR,"#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd")

keepScrolling=True
while(keepScrolling):
    divSideBar.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)
    divSideBar.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)
    html =driver.find_element(By.TAG_NAME, "html").get_attribute('outerHTML')
    if(html.find("A lista végére ért.")!=-1):
        keepScrolling=False
#divek megnyitása
entries = driver.find_elements(By.CLASS_NAME,'hfpxzc')
 
#excel elkőkészítése
workbook = xlsxwriter.Workbook("Fogorvosok.xlsx")
worksheet = workbook.add_worksheet()
#excel ki
row = 1
worksheet.write(0,0,"Név")
worksheet.write(0,1,"Cím")
worksheet.write(0,2,"Telefonszám")
worksheet.write(0,3,"Email")

for entry in entries:
    dentist = Dentist()
    href = entry.get_attribute("href")
    dentist.name = entry.get_attribute("aria-label")
    driver.execute_script(f"window.open('{href}','_blank');")
    time.sleep(5)
    driver.switch_to.window(driver.window_handles[-1])
    sites = driver.find_elements(By.CLASS_NAME,"CsEnBe")
    for site in sites:
        if site.get_attribute("data-item-id")=="address":
            dentist.address = site.get_attribute("aria-label")
        if site.get_attribute("data-item-id").startswith("phone:tel:"):
            dentist.phone = site.get_attribute("aria-label")
        if site.get_attribute("data-item-id")=="authority":
            time.sleep(3)
            url = site.get_attribute('href')
            try:
                dentist.email = extract_emails(url)
            except:
                dentist.email = ["Nincs"]
    dentist.kimenet()
    worksheet.write(row,0,dentist.name)
    worksheet.write(row,1,dentist.address)
    worksheet.write(row,2,dentist.phone)
    worksheet.write(row,3,dentist.email)
    row += 1
    del dentist
    driver.close()
    time.sleep(3)
    driver.switch_to.window(driver.window_handles[0])

workbook.close()
