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
# driver_path = "E:\\Final Semester\\FYP\\Data\\Scraping\\Mutual Funds\\chrome.exe"

# Chrome options
options = Options()
options.add_argument("--disable-gpu")  # Suppress GPU errors
options.add_argument("--ignore-certificate-errors")  # Suppress SSL errors

# Initialize the WebDriver
service = Service()
driver = webdriver.Chrome()

# URL of the page
url = "https://sarmaaya.pk/mutual-funds/fund/3e357642-41f4-47f9-8ec2-8af48c889e77"  # Index Tracker AKDITF
fund = "AKDITF-Index-Tracker-Fund"
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
    csv_path = f"D:\\Github Repos\\FYP-FinSage-Data-Collection\\Data\\Mutual Funds\\Index-Tracker\\{fund}.csv"
    df.to_csv(csv_path, index=False)
    print(f"Data saved to {csv_path}")
else:
    print("Data not found in the extracted JavaScript.")
