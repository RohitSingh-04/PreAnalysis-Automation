import json
import base64
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def save_google_search_to_pdf(url, output_filename):

    chrome_options = Options()

    # Adding an argument to make it look slightly more like a real user
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        driver.get(url)

        # 2. CAPTCHA Check
        # Google usually identifies CAPTCHA pages with 'sorry/index' in the URL or specific text
        while "google.com/sorry" in driver.current_url or "not a robot" in driver.page_source:
            print("!!! CAPTCHA detected. Please solve it in the browser window and press Enter here.")
            input("Press Enter once you have solved the CAPTCHA and the results are visible...")

        # Give the page a moment to fully render after the CAPTCHA or initial load
        time.sleep(2)

        # 3. Save as PDF using Chrome DevTools Protocol (CDP)
        print(f"Saving page to {output_filename}...")
        
        # Parameters for the PDF layout
        print_options = {
            'landscape': False,
            'displayHeaderFooter': False,
            'printBackground': True,
            'preferCSSPageSize': True
        }
        
        # Execute the print command
        result = driver.execute_cdp_cmd("Page.printToPDF", print_options)
        
        # Decode the base64 result and save to file
        with open(output_filename, "wb") as f:
            f.write(base64.b64decode(result['data']))
            
        print("Successfully saved PDF.")

    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        driver.quit()


