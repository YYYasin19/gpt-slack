import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
BROWSER_SETTINGS = webdriver.EdgeOptions()
BROWSER_SETTINGS.add_argument("user-data-dir=selenium")

class GPT:

    def __init__(self) -> None:
        self.browser = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=BROWSER_SETTINGS)
        self.browser.get("https://chat.openai.com")

    def _load_gpt_page(self):
        self._check_login()

    def _check_login(self) -> bool:
        return True

    def _get_input_element(self):
        self._check_login()
        # return self.page.query_selector("div[class*='PromptTextarea__TextareaWrapper']").query_selector("textarea")
        # return self.page.wait_for_selector("div[class*='PromptTextarea__TextareaWrapper").wait_for_selector("textarea").bounding_box()
        return self.browser.find_element(By.CSS_SELECTOR, "div[class*='PromptTextarea__TextareaWrapper']").find_element(By.CSS_SELECTOR, "textarea")
    
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