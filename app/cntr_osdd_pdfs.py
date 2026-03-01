import json
import base64
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from tkinter import messagebox, TclError


def save_google_search_to_pdf(url, output_dir):

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

        # wait for page load
        time.sleep(2)
        
        print_options = {
            'landscape': False,
            'displayHeaderFooter': False,
            'printBackground': True,
            'preferCSSPageSize': True
        }
        
        # print data
        result = driver.execute_cdp_cmd("Page.printToPDF", print_options)
        
        # save file
        with open(output_dir, "wb") as f:
            f.write(base64.b64decode(result['data']))
            
        print("Successfully saved PDF.")

    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        driver.quit()


