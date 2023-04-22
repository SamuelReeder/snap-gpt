import subprocess
import json
from selenium import webdriver
import time
import os

def load_session_details(filename):
    with open(filename, "r") as file:
        return json.load(file)

def create_driver_with_session(session_details):
    chrome_profile_path = os.getcwd + '\profile'

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"user-data-dir={chrome_profile_path}")
    driver = webdriver.Chrome(options=chrome_options)
    # driver = webdriver.Remote(command_executor=session_details["executor_url"])
    # driver.session_id = session_details["session_id"]
    for cookie in session_details["cookies"]:
        driver.add_cookie(cookie) 
    return driver

def main() -> None:
    try:
        session_details = load_session_details("data/session.json")
        driver = create_driver_with_session(session_details)
        driver.get(session_details["url"])
        # Specify the directory for the Chrome profile
        
        
        # print('hey')
        time.sleep(1000)
        # print('he')
        # driver.quit()
        driver.quit()

    except Exception as e:
        print("Please login:", e)
        subprocess.run(["python", "src/login.py"])

if __name__ == "__main__":
    main()