from manager import Manager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time

class SnapAPI(Manager):
    """
    Class to manage and perform Snapchat actions
    """
    
    def send_message(self, message: str, name: str = None) -> None:
        """
        Send a message to a snapchat user
        """
        if self._state is None:
            self.access_conversation(name)
        
        self.wait()
        message_box = self._driver.find_element(by=By.CLASS_NAME, value="euyIb")
        message_box.send_keys(message)
        message_box.send_keys(Keys.ENTER)
         
    
    def get_messages(self, name: str = None) -> list[str]:
        """
        Get the context of a conversation
        """
        if self._state is None:
            self.access_conversation(name)
        
        self.wait()
        element = self._driver.find_elements(by=By.CLASS_NAME, value="bJaPL")[-1]
        text = element.find_elements(by=By.CSS_SELECTOR, value="span.ogn1z")

        return [str(i.text) for i in text]
    
    def access_conversation(self, name: str) -> None:
        """
        Access conversation 
        """
        if name is None:
            raise ValueError()
        
        WebDriverWait(self._driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "' + name + '")]'))
        ).click()  
        
        self._state = name
        
    def close_conversation(self, name: str) -> None:
        """
        Access conversation 
        """
        if name is None:
            raise ValueError()
        
        WebDriverWait(self._driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "' + name + '")]'))
        ).click()  
        
        self._state = None
    
    def update_conversation(self, name: str) -> None:
        """
        Full process for updating a conversation
        """
        messages = self.get_messages(name)
        if len(messages) != 0:
            reply = self.generate_message(messages)
            self.send_message(reply)
        self.close_conversation(name)
        
    def changed(self) -> bool:
        """
        Return whether new messages appear
        """
        self.wait()
        names = [str(i.text) for i in self._driver.find_elements(by=By.XPATH, value='//span[@class="FiLwP"][not(span)] | //span[@class="FiLwP"]/span[@dir="auto"]')]
        messages = [str(i.text) for i in self._driver.find_elements(by=By.XPATH, value='//div[contains(@class, "ovUsZ")]//*[contains(@class, "GQKvA")]')]
        
        changed = False
        for i in range(len(names)):
            try:
                if self._order[i] != names[i]:
                    self._order.remove(names[i])
                    self._order.insert(i, names[i])
                    self._archive[names[i]]["subtext"] = messages[i]
                    if 'New' in messages[i]:
                        self._archive[names[i]]["status"] = True
                        changed = True
                elif self._archive[names[i]]["subtext"] != messages[i]:
                    self._archive[names[i]]["subtext"] = messages[i]
                    if 'New' in messages[i]:
                        self._archive[names[i]]["status"] = True
                        changed = True
            except IndexError as e:
                print(e)
                
        return changed
    
        
    def monitor(self) -> None:
        """
        Monitor for new messages 
        """
        self.wait()
        names = [str(i.text) for i in self._driver.find_elements(by=By.XPATH, value='//span[@class="FiLwP"][not(span)] | //span[@class="FiLwP"]/span[@dir="auto"]')]
        messages = [str(i.text) for i in self._driver.find_elements(by=By.XPATH, value='//div[contains(@class, "ovUsZ")]//*[contains(@class, "GQKvA")]')]
        
        for i in range(len(names)):
            self._order.append(names[i])
            self._archive[names[i]] = {"status": False, "subtext": messages[i], "position": i}

        print(self._archive)        
        print(self._order)
        wait = WebDriverWait(self._driver, 10)
        while True:
            try:
                wait.until(lambda _: self.changed())

                print('hey')
                for key in self._archive:
                    if self._archive[key]["status"]:
                        print(key)
                        self.update_conversation(key)
                        self._archive[key]["status"] = False
                    # else:
                    #     break
                time.sleep(2)
                
            except TimeoutException as e:
                print(f"Error occurred: {e}")