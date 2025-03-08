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
driver_path = "E:\\Final Semester\\Github Repos\\FYP-FinSage-Data-Collection\\Data\\ETF\\chromedriver.exe"

# Chrome options
options = Options()
options.add_argument("--disable-gpu")  # Suppress GPU errors
options.add_argument("--ignore-certificate-errors")  # Suppress SSL errors

# Initialize the WebDriver
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

fund = "MP-ETF"  # MP-ETF
# URL of the page
url = f"https://sarmaaya.pk/mutual-funds/fund/{fund}"
# url = "https://sarmaaya.pk/psx/etf/MIIETF"
# url = "https://sarmaaya.pk/psx/etf/HBLTETF"
# url = "https://sarmaaya.pk/psx/etf/UBLPETF"
# url = "https://sarmaaya.pk/psx/etf/JSGBPETF" ***** ask Hamza bhai ******
# url = "https://sarmaaya.pk/psx/etf/NITGETF"
# url = "https://sarmaaya.pk/psx/etf/NBPGETF"
# url = "https://sarmaaya.pk/psx/etf/ACIETF"
# url = "https://sarmaaya.pk/psx/etf/JSMFETF"

driver.get(url)

# Wait for the page and the "All" tab to load
wait = WebDriverWait(driver, 15)
try:
    # Wait for the "All" tab to be clickable
    all_tab = wait.until(EC.element_to_be_clickable((By.ID, "nav-all-tab")))
    # all_tab = wait.until(EC.element_to_be_clickable((By.ID, "nav-20y-tab")))

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

# Parse the JSON content
if script_content and "data" in script_content:
    data = script_content["data"]
    # Convert to a DataFrame
    df = pd.DataFrame(data)

    # Convert the 's_date' to a datetime object and then format it to 'YYYY-MM-DD'
    df['Date'] = pd.to_datetime(df['s_date'], format='%b %d, %Y').dt.strftime('%Y-%m-%d')

    # Rename the columns
    df = df[['Date', 's_close']]  # Keep only 'Date' and 's_close'
    df.columns = ['Date', 'Price']  # Rename columns to 'Date' and 'Price'

    # Save to CSV
    csv_path = f"E:\\Final Semester\\Github Repos\\FYP-FinSage-Data-Collection\\Data\\ETF\\{fund}.csv"
    df.to_csv(csv_path, index=False)
    print(f"Data saved to {csv_path}")
else:
    print("Data not found in the extracted JavaScript.")
