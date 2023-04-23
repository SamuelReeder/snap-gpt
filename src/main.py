from selenium import webdriver
import json, os, login, snap_manager


def load_session_details(filename):
    with open(filename, "r") as file:
        return json.load(file)

def create_driver_with_session(session_details):
    chrome_profile_path = os.path.join(os.getcwd(), 'profile')

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"user-data-dir={chrome_profile_path}")
    driver = webdriver.Chrome(options=chrome_options)
    # for cookie in session_details["cookies"]:
    #     driver.add_cookie(cookie) 
    return driver

def main() -> None:
    try:
        session_details = load_session_details("data/session.json")
        driver = create_driver_with_session(session_details)
        driver.get(session_details["url"])       
        print('hey') 
        snap_manager.run(driver)
        driver.quit()

    except Exception as e:
        print("Please login:", e)
        # login.login()    
            

if __name__ == "__main__":
    main()