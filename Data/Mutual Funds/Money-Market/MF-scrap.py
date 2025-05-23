from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json
import pandas as pd

# Path to your WebDriver
# driver_path = "D:\\FYP\\Data\\Scraping\\Mutual Funds\\chromedriver.exe"

# Chrome options
options = Options()
options.add_argument("--disable-gpu")  # Suppress GPU errors
options.add_argument("--ignore-certificate-errors")  # Suppress SSL errors

# Initialize the WebDriver
# service = Service(driver_path)
service = Service()
driver = webdriver.Chrome(service=service, options=options)

# fund = "ABL-MMP-Money-Fund" # ABL-MMP-Money-Fund 
from datetime import datetime

# Path to your WebDriver
# driver_path = "E:\\Final Semester\\FYP\\Data\\Scraping\\Mutual Funds\\chromedriver.exe"

# Initialize the WebDriver
# service = Service(driver_path)
# service = Service()
# driver = webdriver.Chrome(service=service, options=options)

# URL of the page
# fund = "UMMF-UBL-Money-Fund"  # UMMF-UBL-Money-Fund
# fund = "ABL-MMP-Money-Fund"  # ABL-MMP-Money-Fund
# fund = "ALF-Atlas-Liquid-Fund"  # ALF-Atlas-Liquid-Fund
# fund = "JS-Money-Fund"  # JS-Money-Fund
fund = "NIT-NMMF-Money-Fund"  # NIT-NMMF-Money-Fund

# url = "https://sarmaaya.pk/mutual-funds/fund/625a9cf0-94b5-46b7-b7fb-ab60b774cf17" # Money Market Fund UBL
# url = "https://sarmaaya.pk/mutual-funds/fund/8e2cfcb1-fe71-43f7-b79c-f3d0739f047c" # ALF Atlas Liquid Fund
# url = "https://sarmaaya.pk/mutual-funds/fund/b05df539-9fff-4857-9d11-6acf6e75d754" # ABL Money Market Fund
# url = "https://sarmaaya.pk/mutual-funds/fund/a6c292ea-1911-4404-b779-d75ecbd7d29b" # JS Money Market Fund
url = "https://sarmaaya.pk/mutual-funds/fund/f33db54f-7d15-4f54-aa0a-e4090ed63570" # NIT NMMF Money Market Fund


driver.get(url)

# Wait for the page and the "All" tab to load
wait = WebDriverWait(driver, 15)
try:
    # Wait for the "All" tab to be clickable
    all_tab = wait.until(EC.element_to_be_clickable((By.ID, "nav-all-tab")))
    all_tab.click()
    print("Selected the 'All' tab successfully.")

    # Wait for the graph data to update (adjust condition based on the page's behavior)
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
    # Wait for the data to update in the JavaScript variable
    driver.implicitly_wait(5)
    script_content = driver.execute_script("return jsonfile;")  # Assuming `jsonfile` contains the updated data
    print("JavaScript variable fetched.")
except Exception as e:
    print(f"Error while executing JavaScript: {e}")
    script_content = None

# Close the WebDriver
driver.quit()

# Parse the JSON content and process the data
if script_content and "data" in script_content:
    data = script_content["data"]
    
    # Create a new list to store the formatted data
    formatted_data = []
    
    for entry in data:
        # Extract the date and price
        price = entry.get("s_close", "")
        date_str = entry.get("s_date", "")
        
        if price and date_str:
            # Convert the date to the format YYYY-MM-DD
            try:
                # Assuming the date is in the format "Jul 08, 2008"
                date_obj = datetime.strptime(date_str, "%b %d, %Y")
                formatted_date = date_obj.strftime("%Y-%m-%d")
                
                # Append the formatted data
                formatted_data.append([formatted_date, price])
            except ValueError as e:
                print(f"Error while formatting date: {e}")
    
    # Convert to a DataFrame
    df = pd.DataFrame(formatted_data, columns=["Date", "Price"])

    # Save to CSV
    csv_path = f"D:\\Github Repos\\FYP-FinSage-Data-Collection\\Data\\Mutual Funds\\Money-Market\\{fund}.csv"
    df.to_csv(csv_path, index=False)
    print(f"Data saved to {csv_path}")
else:
    print("Data not found in the extracted JavaScript.")
