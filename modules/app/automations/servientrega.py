import os
import glob
from time import sleep

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
#from selenium.common.exceptions import TimeoutException

import zipfile


##credentials
username_credential = "19157568"
password_credential = "Servi2021**"

## Constants
open_login_button = "/html/body/main/div/header/section[1]/section[2]/nav/ul/li[6]/a"
select_customer_type_option = '/html/body/main/div/header/section[1]/section[2]/div[2]/div/form/fieldset[1]/select/option[2]'
select_identification_type_option = '/html/body/main/div/header/section[1]/section[2]/div[2]/div/form/fieldset[3]/div/select/option[3]'
transaction_button = '/html/body/main/div/header/section[1]/section[2]/nav/ul/li[4]/a'
safezone_menu_button = "/html/body/main/div/div[1]/nav/ul/li/ul/li[1]/div[1]/a"
sismilenio_submenu_button = "/html/body/main/div/div[1]/nav/ul/li/ul/li[1]/div[2]/ul/li[1]/a"
sismilenio_login_button = "/html/body/main/div/div[2]/div/div/div[2]/div/div[1]/div[1]/section/div[3]/section/section/section/div[2]/div/p/a"
sismilenio_first_select_option = "/html/body/form/div[3]/table/tbody/tr[4]/td/div/div/table/tbody/tr[2]/td[1]/input"

default_sismilenio_frame = '//*[@id="InternalFrame"]/frame[1]'
step1_sismilenio_menu = "/html/body/form/table/tbody/tr/td/div/table[1]/tbody/tr/td[2]/a"
step2_sismilenio_menu = "/html/body/form/table/tbody/tr/td/div/div/table/tbody/tr/td[3]/a"
step3_sismilenio_menu = "/html/body/form/table/tbody/tr/td/div/div/div/table/tbody/tr/td[4]/a"

sismilenio_content_frame = '//*[@id="InternalFrame"]/frame[2]'

username_id = "userID"
password_id = "password"
login_button_id = "login.button.login"


start_date_id = '//*[@id="txtFechaIni"]'
end_date_id = '//*[@id="txtFechaFin"]'
generate_report_button = '/html/body/form/table/tbody/tr[1]/td/table[2]/tbody/tr[2]/td[1]/input'

first_date = "02/01/2021"
end_date = "02/28/2021"

#download path
download_path = "/Users/jesusvega/Downloads/*"

class servientrega_automation():

    def __init__(self):

        #start point
        self.browser = webdriver.Chrome()
        self.browser.get(url="https://www.servientrega.com/")
        sleep(5)

    def execute_alert(self,message):
        try:
            self.browser.execute_script("alert('"+message+"');")
        except WebDriverException:
            print("Alert error")

    def element_presence(self,by, xpath, time):
        print("loading")
        element_present = EC.presence_of_element_located((By.XPATH, xpath))
        WebDriverWait(self.browser, time).until(element_present)

    def openLoginMenu(self):
        print("!web loaded¡")
        sleep(1.5)
        self.browser.find_element_by_xpath(open_login_button).click()
        sleep(2)
        # setting form input
        print("setting form")
        username = self.browser.find_element_by_id(username_id)
        password = self.browser.find_element_by_id(password_id)
        username.send_keys(username_credential)
        password.send_keys(password_credential)
        self.browser.find_element_by_xpath(select_customer_type_option).click()
        sleep(1)
        self.browser.find_element_by_xpath(select_identification_type_option).click()
        self.browser.find_element_by_id(login_button_id).click()
        self.element_presence(By.XPATH,transaction_button,1)
        self.operation_on_transaction_view()

    def operation_on_transaction_view(self):
        print("on transaction view")
        self.browser.find_element_by_xpath(transaction_button).click()
        self.element_presence(By.XPATH,safezone_menu_button,5)
        self.browser.find_element_by_xpath(safezone_menu_button).click()
        sleep(0.5)
        self.browser.find_element_by_xpath(sismilenio_submenu_button).click()
        self.element_presence(By.XPATH,sismilenio_login_button,5)
        sleep(0.5)
        self.browser.find_element_by_xpath(sismilenio_login_button).click()  
        sleep(0.5)
        self.download_file()


    def download_file(self):
        print("on sismilenio")
        self.browser.switch_to.window(self.browser.window_handles[1])   
        print("select first menu")
        self.element_presence(By.XPATH,sismilenio_first_select_option,5)
        self.browser.find_element_by_xpath(sismilenio_first_select_option).click() 
        print("switching to frame")
        self.element_presence(By.XPATH,default_sismilenio_frame,5)
        self.browser.switch_to.frame(self.browser.find_element_by_xpath(default_sismilenio_frame))   
        sleep(1)
        print("clicking multiple menus")    
        self.browser.find_element_by_xpath(step1_sismilenio_menu).click() 
        sleep(0.5)
        self.browser.find_element_by_xpath(step2_sismilenio_menu).click() 
        sleep(0.5)
        self.browser.find_element_by_xpath(step3_sismilenio_menu).click() 
        self.browser.switch_to.window(self.browser.window_handles[1]) 
        self.element_presence(By.XPATH,sismilenio_content_frame,5)
        print("content frame ready") 
        self.browser.switch_to.frame(self.browser.find_element_by_xpath(sismilenio_content_frame))  
        print("setting form")
        #print(self.browser.page_source)
        self.element_presence(By.XPATH,start_date_id,5)
        sleep(1)
        print("after wait a while .................................................")
        #print(self.browser.page_source)
        self.browser.execute_script("arguments[0].removeAttribute('readonly')", WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.XPATH, start_date_id))))
        self.browser.execute_script("arguments[0].removeAttribute('readonly')", WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.XPATH, end_date_id))))
        self.browser.execute_script("arguments[0].setAttribute('value','"+first_date+"')", WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.XPATH, start_date_id))))
        self.browser.execute_script("arguments[0].setAttribute('value','"+end_date+"')", WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.XPATH, end_date_id))))
        sleep(0.5)
        self.browser.find_element_by_xpath(generate_report_button).click()
        sleep(4)
        self.unzipAndOpenFile()

    def unzipAndOpenFile(self):
        list_of_files = glob.glob(download_path)
        latest_file = max(list_of_files, key=os.path.getctime)
        #we need to check if zip file
        print(latest_file)    
        with zipfile.ZipFile(latest_file,"r") as zip_ref:
            zip_ref.extractall("/Users/jesusvega/Desktop")
        sleep(1)
        list_of_files = glob.glob("/Users/jesusvega/Desktop/*")
        latest_file = max(list_of_files, key=os.path.getctime)
        #we need to check if zip file and escape the string better
        print("open "+latest_file) 
        os.system("open "+"'"+latest_file+"'")

    def start_script(self):
        print("start servientrega script")
        try:
            self.element_presence(By.XPATH,open_login_button,1)
            self.openLoginMenu()
        
        except Exception as e:
            print("Could not load site: "+str(e))

#if __name__ == '__main__':
#    main()



