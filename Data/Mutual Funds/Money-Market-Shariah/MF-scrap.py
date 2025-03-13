from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json
import pandas as pd

# Path to your WebDriver
driver_path = "E:\\Final Semester\\FYP\\Data\\Scraping\\Mutual Funds\\chromedriver.exe"

# Chrome options
options = Options()
options.add_argument("--disable-gpu")  # Suppress GPU errors
options.add_argument("--ignore-certificate-errors")  # Suppress SSL errors

# Initialize the WebDriver
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

fund = "ABL-Money-Fund"
# URL of the page
# url = "https://sarmaaya.pk/mutual-funds/fund/9747efd9-f18e-435e-985e-7bd1e98a9de1" # AKD Islamic Daily Fund Dividend
url = "https://sarmaaya.pk/mutual-funds/fund/bc148449-d667-4cb2-9cd9-86d900a2e1ed" # ABL Money Market Plan I
# url = "https://sarmaaya.pk/mutual-funds/fund/6eaf7ec6-0633-4003-96d9-d131951370f0" # HBL ISF
# url= "https://sarmaaya.pk/mutual-funds/fund/97c814f9-3854-4ac1-9043-044381d9ac72" #FICF Faysal Islamic Cash-Fund
# url = "https://sarmaaya.pk/mutual-funds/fund/6142c280-ada7-45cf-8a7f-32e8f4db37ba" # AIMF Atlas Islamic


driver.get(url)

# Wait for the page and the "All" tab to load
wait = WebDriverWait(driver, 15)
try:
    # Wait for the "All" tab to be clickable
    all_tab = wait.until(EC.element_to_be_clickable((By.ID, "nav-all-tab")))
    all_tab.click()
    print("Selected the 'All' tab successfully.")

    # Wait for the graph data to update
    WebDriverWait(driver, 10).until(
        lambda d: "active" in d.find_element(By.ID, "nav-all-tab").get_attribute("class")
    )
    print("Graph data for 'All' loaded.")
except Exception as e:
    print(f"Failed to select the 'All' tab: {e}")
    driver.quit()
    exit()

# Extract the JavaScript variable after clicking "All"
try:
    driver.implicitly_wait(5)
    script_content = driver.execute_script("return jsonfile;")  # Assuming `jsonfile` contains the updated data
    print("JavaScript variable fetched.")
except Exception as e:
    print(f"Error while executing JavaScript: {e}")
    script_content = None

# Close the WebDriver
driver.quit()

# Parse the JSON content and format the data
if script_content and "data" in script_content:
    data = script_content["data"]

    # Ensure we have a list of dictionaries for DataFrame conversion
    if isinstance(data, list):
        # Extract only 'Date' and 'Price' (assuming 'price' corresponds to the price field)
        formatted_data = []
        for entry in data:
            formatted_entry = {
                'Date': entry.get('date', ''),
                'Price': entry.get('price', '')  # Assuming 'price' is the price field
            }
            formatted_data.append(formatted_entry)

        # Convert to a DataFrame
        df = pd.DataFrame(formatted_data)

        # Save to CSV
        csv_path = f"E:\\Final Semester\\Github Repos\\FYP-FinSage-Data-Collection\\Data\\Mutual Funds\\Money-Market-Shariah\\{fund}.csv"
        df.to_csv(csv_path, index=False)
        print(f"Data saved to {csv_path}")
    else:
        print("Data format is not a list, unable to process.")
else:
    print("Data not found in the extracted JavaScript.")
