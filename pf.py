import os
import glob
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select


options = webdriver.ChromeOptions()

path = os.path.dirname(os.path.abspath(__file__))
prefs = {}
#config for downloads to be in current directory
prefs["profile.default_content_settings.popups"]=0
prefs["download.default_directory"]=path
options.add_experimental_option("prefs", prefs)

pfdriver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
maildriver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

#create temporary email
maildriver.get("https://hottempmail.com/")

#go to planet fitness form and fill out
pfdriver.get('https://daypass.planetfitness.com/')

select = Select(pfdriver.find_element('id','ContentPlaceHolder1_cmbCountry'))
select.select_by_visible_text('USA')

select = Select(pfdriver.find_element('id','ContentPlaceHolder1_cmbState'))
select.select_by_visible_text('PA')

select = Select(pfdriver.find_element('id','ContentPlaceHolder1_cmbCity'))
select.select_by_visible_text('Bethlehem')


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
#print(address.text)

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

#click on the email
maildriver.find_element('xpath','//*[contains(text(),"Welcome to Planet Fitness")]').click()
#click on download
maildriver.find_element('xpath','//*[contains(text(),"Download")]').click()


#open the .eml file and find the full url of the link containing "bwipjs-api"
#this is the link to the pass
#wait until the file is downloaded
while True:
    try:
        #open the .eml file in this directory
        file = open(glob.glob("*.eml")[0], "r")
        break
    except:
        time.sleep(1)

#open the file
with open(file.name, 'r') as f:
    #read the file
    data = f.read()
    #fget line with link
    line = data.splitlines()[413]
    #extract url
    url = line.split('src="')[1].split('"')[0]
    print(url)

#delete the file
os.remove(file.name)

pfdriver.quit()
maildriver.quit()