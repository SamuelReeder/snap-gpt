from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import getpass
import re
import sys
import os


def is_valid_email(email):
    email_pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

    if re.match(email_pattern, email):
        return True
    else:
        return False

def create_visible_driver(session_id, executor_url):
    driver = webdriver.Chrome()
    driver.session_id = session_id
    driver.command_executor._url = executor_url
    return driver

def retry(msg: str) -> bool:
        retry = input(f"{msg} Would you like to retry? y/n")
        if retry == 'y':
            return True
        else:
            print('Exiting...')
            time.sleep(2)
            if sys.platform == "win32":
                os.system("taskkill /F /IM cmd.exe")
            elif sys.platform in ("linux", "linux2", "darwin"):
                os.system("kill -9 $(ps -p $PPID -o ppid=)")
            return False\
                
drive = None
    
driver = webdriver.Chrome()
# chrome_options.add_argument("--headless")

# Create a new instance of the browser driver with the headless option
# driver = webdriver.Chrome(options=chrome_options)

while True:
                
    # id = input("Please enter your snapchat associated email: ").lower()
    id = 'samuel.reeder8@gmail.com'
    password = 'KqK+sua6?C4GQwQ'

    if is_valid_email(id) and password is not None:
        print("Success")
        
    driver.get("https://web.snapchat.com")
    
    driver.implicitly_wait(10)

    driver.find_element(by=By.ID, value="accountIdentifier").send_keys(id)
    driver.find_element(by=By.CSS_SELECTOR, value=".primary_action.login-button > button.btn.btn-lg.btn-default").click()
 
    # driver.find_element(by=By.ID, value="password").send_keys(password)
    # driver.find_element(by=By.CSS_SELECTOR, value=".primary_action.login-button > button.btn.btn-lg.btn-default").click()    
    
    # print("Waiting...", end="", flush=True)
    # driver.implicitly_wait(0.5)
    # print("\r" + " " * len("Waiting..."), end="", flush=True)

    # if "Is This You?" in driver.page_source:
    #     print("Login successful, 2FA page displayed. Please check your Snapchat app to verify the login. We will then continue.")
    # else:
    #     if retry('Login failed.'):
    #         continue

    # auth_url = driver.current_url
    success_url = 'https://web.snapchat.com/'
    WebDriverWait(driver, 500).until(lambda d: d.current_url == success_url)
    print("Successful")
    break
    # try:
    #     print("Login succesful.")
    #     # session_id, exec_url= driver.session_id, driver.command_executor._url
    #     # driver.quit()
    #     # driver = create_visible_driver(session_id,exec_url)
    #     break
    #     # else:
    #     #     if retry('The 2FA might have been rejected.'):
    #     #         continue
    # except WebDriverWait.TimeoutException:
    #     if retry('Timeout exceeded.'):
    #         continue
        
    # print()
    

driver.implicitly_wait(1000)
driver.quit()