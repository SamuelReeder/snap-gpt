from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import openai, os, time


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def run(driver) -> None:
        
    will_oberlin_element = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Will Oberlin")]'))
    )
    will_oberlin_element.click()    
    
    driver.implicitly_wait(10) 
    
    element = driver.find_elements(by=By.CLASS_NAME, value="bJaPL")[-1]
    text = element.find_elements(by=By.CSS_SELECTOR, value="span.ogn1z")

    messages = [str(i.text) for i in text]
    result = "\n".join(messages)
    SYSTEM = 'You are to treat this conversation as a message exchange between young adults on snapchat. As in, you are pretending to be a young adult using snapchat. The implications of that are you will provide short responses with no capitalization, lots of acronyms, limited punctuation, slang and no emojiis. You are to act as a snapchat user.'
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": result},
        ]
    )   

    msg = response['choices'][0]['message']['content']
    driver.implicitly_wait(10) 
    textbox = driver.find_element(by=By.CLASS_NAME, value="euyIb")
    textbox.send_keys(msg)
    textbox.send_keys(Keys.ENTER)
    # FiLwP
    time.sleep(10000)
    return 
    


