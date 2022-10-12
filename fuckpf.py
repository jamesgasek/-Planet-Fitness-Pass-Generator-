from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import os
import glob
#time
import time

options = webdriver.ChromeOptions()
#options.add_argument('headless')


pfdriver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
maildriver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


maildriver.get("https://hottempmail.com/")

pfdriver.get('https://daypass.planetfitness.com/')

select = Select(pfdriver.find_element('id','ContentPlaceHolder1_cmbCountry'))
select.select_by_visible_text('USA')

select = Select(pfdriver.find_element('id','ContentPlaceHolder1_cmbState'))
select.select_by_visible_text('PA')

select = Select(pfdriver.find_element('id','ContentPlaceHolder1_cmbCity'))
select.select_by_visible_text('Bethlehem')

print("Inserting name")
time.sleep(10)

fname = pfdriver.find_element('id','ContentPlaceHolder1_txtFirstName')
fname.send_keys('John')

lname = pfdriver.find_element('id','ContentPlaceHolder1_txtLastName')
lname.send_keys('Doe')

select = Select(pfdriver.find_element('id','ContentPlaceHolder1_ddlDOBMonth'))
select.select_by_visible_text('8')

select = Select(pfdriver.find_element('id','ContentPlaceHolder1_ddlDOBDay'))
select.select_by_visible_text('8')

select = Select(pfdriver.find_element('id','ContentPlaceHolder1_ddlDOBYear'))
select.select_by_visible_text('1990')

address = maildriver.find_element('id','email_id')
print(address.text)

email = pfdriver.find_element('id','ContentPlaceHolder1_txtEmailAddress')
email.send_keys(address.text)

#click button with id ContentPlaceHolder1_btnContinue
pfdriver.find_element('id','ContentPlaceHolder1_btnContinue').click()

#wait until we can find "Welcome to Planet Fitness" on the temporary email page
while True:
    try:
        maildriver.find_element('xpath','//*[contains(text(),"Welcome to Planet Fitness")]')
        break
    except:
        time.sleep(1)

print("Found email")
#click on the email
maildriver.find_element('xpath','//*[contains(text(),"Welcome to Planet Fitness")]').click()
#click on download
#maildriver.find_element('xpath','//*[contains(text(),"Download")]').click()
#get the src of the image with width = 300
time.sleep(1000)

img = maildriver.find_element('xpath','//img[@width="300"]')
print(img.get_attribute('src'))
#get the most recent download from the downloads folder


time.sleep(1000)


pfdriver.quit()
maildriver.quit()