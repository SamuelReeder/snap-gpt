from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time, json, sys, os

def retry(msg: str) -> bool:
        retry = input(f"{msg} Would you like to retry? y/n")
        if retry == 'y':
            return True
        else:
            if sys.platform == "win32":
                os.system("taskkill /F /IM cmd.exe")
            elif sys.platform in ("linux", "linux2", "darwin"):
                os.system("kill -9 $(ps -p $PPID -o ppid=)")
            return False

def save_session_details(driver, file_name: str) -> None:

    folder_path = os.path.join(os.getcwd(), 'data')
    print(folder_path)
    os.makedirs(folder_path, exist_ok=True)

    session_details = {
        "session_id": driver.session_id,
        "executor_url": driver.command_executor._url,
        "url": driver.current_url,
        "cookies": driver.get_cookies()
    }
    with open(os.path.join(folder_path, file_name), "w") as f:
        json.dump(session_details, f)

def login() -> None:
    folder_path = os.path.join(os.getcwd(), 'profile')
    os.makedirs(folder_path, exist_ok=True)

    chrome_profile_path = folder_path
    snap = "https://web.snapchat.com"

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={chrome_profile_path}")
    driver = webdriver.Chrome(options=options)

    while True:
                    
        driver.get(snap)
        time.sleep(5)
        
        try:
            WebDriverWait(driver, 500).until(lambda d: snap in str(d.current_url))
        except TimeoutException:
            if retry("Timeout exceeded."):
                continue

        print('check')
        save_session_details(driver, 'session.json')
        print("Login succesful, session details saved.")
        time.sleep(5)
        driver.quit()
        break
