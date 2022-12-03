import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import os
load_dotenv()
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
BROWSER_SETTINGS = webdriver.EdgeOptions()
BROWSER_SETTINGS.add_argument("user-data-dir=selenium3")

class GPT:

    def __init__(self) -> None:
        self.browser = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=BROWSER_SETTINGS)
        self.browser.get("https://chat.openai.com")
        self._check_login()

    def _get_input_element(self):
        self._check_login()
        # return self.page.query_selector("div[class*='PromptTextarea__TextareaWrapper']").query_selector("textarea")
        # return self.page.wait_for_selector("div[class*='PromptTextarea__TextareaWrapper").wait_for_selector("textarea").bounding_box()
        return self.browser.find_element(By.CSS_SELECTOR, "div[class*='PromptTextarea__TextareaWrapper']").find_element(By.CSS_SELECTOR, "textarea")
    
    def _check_login(self):
        if 'login' in self.browser.current_url or 'Log in with your OpenAI account to continue' in self.browser.page_source:
            user, passw = os.environ['USERNAME'], os.environ['PASSWORD']
            login_btn = self.browser.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[4]/button[1]')
            login_btn.click()

            user_field = self.browser.find_element(By.XPATH, '//*[@id="username"]')
            user_field.send_keys(user)
            user_field.send_keys(Keys.ENTER)

            passw_field = self.browser.find_element(By.XPATH, '//*[@id="password"]')
            passw_field.send_keys(passw)
            passw_field.send_keys(Keys.ENTER)
            time.sleep(10) # safety, wait 10 seconds

            while (nxt := self.browser.find_element(By.XPATH, "//*[text()='Next' or text()='Done']")):
                nxt.click()
                time.sleep(1)

    
    def query(self, query_str:str)->str:
        
        text_field = self._get_input_element()
        text_field.send_keys(query_str)
        text_field.send_keys(Keys.ENTER) # TODO: button

        # wait for a response
        # TODO: this does wait for the wrong element, of course
        time.sleep(5)
        # WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.ID, "div[class*='PromptTextarea__TextareaWrapper']")))

        # Get the current conversations
        conversation = self.browser.find_elements(By.CSS_SELECTOR, "div[class*='ConversationItem__Message']")

        # Return the search results
        return conversation[-1].text

    def __del__(self) -> None:
        self.browser.quit()