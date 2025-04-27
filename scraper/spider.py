from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time


class Booking(webdriver.Chrome):
    def __init__(self,teardown=False):
        self.teardown = teardown
        chrome_options = Options()

        # Run in incognito mode
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")  
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-browser-side-navigation")
        chrome_options.add_argument("--enable-features=MemorySavings")  
        chrome_options.add_argument("--force-fieldtrials=MemorySavings/Enabled")
        
        chrome_options.page_load_strategy = 'eager'
      
        super(Booking, self).__init__(options=chrome_options)
        self.implicitly_wait(3)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get("https://magicpin.in/")

    def setting_up_page(self):
        wait = WebDriverWait(self, 10)
        container = wait.until(EC.presence_of_element_located((By.ID, "city-popup-builder")))
        print("Container found.")

        # Step 1: Click on the city button inside the container
        city_button = container.find_element(By.CLASS_NAME, "searchLocation")
        city_button.click()
        print("City button clicked.")

        location_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#city-popup-builder input.location")))
        print("Location input field found.")

        location_input.clear()
        location_input.send_keys("Andheri, Mumbai")
        location_input.send_keys(Keys.RETURN)
        print("Location input filled and submitted.")
        time.sleep(5)

        # Step 2: Locate the search results container
        search_results_container = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "searchLocationResults")))
        print("Search results container found.")

        # Step 3: Print the content of the search results container
        print("Search results content:")
        print(search_results_container.get_attribute("outerHTML"))
  
        time.sleep(5)  # optional wait if suggestions drop down
    


if __name__ == "__main__":

    with Booking(teardown=True) as bot:
        bot.land_first_page()
        bot.setting_up_page()
        # Add any additional actions you want to perform on the first page here