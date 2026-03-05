import json
import base64
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from tkinter import messagebox, TclError
from app.settings import PRINT_OPTIONS, NEGATIVE_URL

def save_pdf(driver, output_dir):

    # wait for page load
    time.sleep(2)
        
    # print page
    result = driver.execute_cdp_cmd("Page.printToPDF", PRINT_OPTIONS)
    
    # save pdf
    with open(output_dir, "wb") as f:
        f.write(base64.b64decode(result['data']))


def save_google_search_to_pdf(url, output_dir, mode=False):

    chrome_options = Options()

    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        driver.get(url)

        # detect CAPTCHA try 1
        while "google.com/sorry" in driver.current_url or "not a robot" in driver.page_source:
            try:
                user_input = messagebox.askyesnocancel("Captcha Detected", "!!! CAPTCHA detected. Please solve it in the browser window and click on Yes if solved!")
            except (AttributeError, TclError):
                raise AttributeError("Error! Tkinter window not found, please ensure the main tkinter window is running!")

            if user_input is None:
                return
            
            elif user_input:
                break

        save_pdf(driver, output_dir)
        
        print("Successfully saved PDF!")

        #take page 2 if avaliable and is negative search
        if mode == NEGATIVE_URL:
            elements = driver.find_elements(By.XPATH, '//*[@aria-label="Page 2"]')

            if len(elements) > 0:
                elements[0].click()
                save_pdf(driver, str(output_dir)[:-4]+' 2.pdf')

    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        driver.quit()


