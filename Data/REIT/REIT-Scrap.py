from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json
import pandas as pd
from datetime import datetime

# Path to your WebDriver
driver_path = "E:\\Final Semester\\FYP\\Data\\Scraping\\REIT\\chromedriver.exe"

# Chrome options
options = Options()
options.add_argument("--disable-gpu")  # Suppress GPU errors
options.add_argument("--ignore-certificate-errors")  # Suppress SSL errors

# Initialize the WebDriver
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

fund = "TPLRF1" # DCR TPLRF1 GRR
# URL of the page
url = f"https://sarmaaya.pk/psx/company/{fund}"

driver.get(url)

# Wait for the page and the "All" tab to load
wait = WebDriverWait(driver, 15)
try:
    all_tab = wait.until(EC.element_to_be_clickable((By.ID, "nav-20y-tab")))
    all_tab.click()
    print("Selected the 'All' tab successfully.")

    WebDriverWait(driver, 10).until(
        lambda d: "active" in d.find_element(By.ID, "nav-20y-tab").get_attribute("class")
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

# Debug: Print the structure of 'script_content'
# print(json.dumps(script_content, indent=4))  # Pretty-print the data

# Parse the JSON content
if script_content and "data" in script_content:
    data = script_content["data"]
    
    # Create empty lists to store the formatted data
    formatted_dates = []
    formatted_prices = []
    
    # Iterate over the data to extract and format the date and price
    for entry in data:
        # Extract date and price from the dictionary
        date_str = entry.get("s_date", "")
        price = entry.get("s_close", None)

        if date_str and price is not None:
            # Convert the date from "Feb 28, 25" format to "2025-02-28"
            date_obj = datetime.strptime(date_str, "%b %d, %y")
            formatted_date = date_obj.strftime("%Y-%m-%d")
            
            # Append the formatted data to the lists
            formatted_dates.append(formatted_date)
            formatted_prices.append(price)
    
    # Convert the lists to a DataFrame
    df = pd.DataFrame({
        'Date': formatted_dates,
        'Price': formatted_prices
    })

    # Save to CSV
    csv_path = f"E:\\Final Semester\\Github Repos\\FYP-FinSage-Data-Collection\\Data\\REIT\\{fund}.csv"
    df.to_csv(csv_path, index=False)
    print(f"Data saved to {csv_path}")
else:
    print("Data not found in the extracted JavaScript.")
