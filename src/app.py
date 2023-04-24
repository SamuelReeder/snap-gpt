from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
from snap_api import SnapAPI
import openai, os, time


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def run(driver) -> None:
        
    snap = SnapAPI(driver)
    snap.monitor()
    time.sleep(10000)
    return 
    
    


