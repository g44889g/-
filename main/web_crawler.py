from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
from datetime import datetime
import sys
import os




# Web scraping function
def scrape_fields(url):
    # Set headless mode for Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # 指定 ChromeDriver 的執行檔路徑
    service = Service('chromedriver.exe')

    # Initialize WebDriver with the path to the ChromeDriver executable
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)  # 使用動態路徑
    driver.get(url)
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()  # Close driver after scraping

    # Get title and field data
    center_content = soup.find("center")
    title = center_content.get_text(strip=True) if center_content else "標題未知"
    fields = soup.find_all("span", class_="field")
    content = "\n".join([field.get_text(strip=True) for field in fields])
    return title, content


# Function to save data to CSV
def save_to_csv(data):
    # Define the file name
    filename = "國際鋁銅價格.csv"

    # Convert to DataFrame
    df = pd.DataFrame(data, columns=["日期", "標題", "內容"])

    # Append to CSV, creating the file if it doesn't exist
    try:
        df.to_csv(
            filename,
            mode="a",
            index=False,
            header=not pd.io.common.file_exists(filename),
            encoding="utf-8-sig",
        )
        print("Data saved successfully")
    except Exception as e:
        print(f"Failed to save data: {e}")


# Main script
if __name__ == "__main__":
    urls = [
        "https://fubon-ebrokerdj.fbs.com.tw/z/ze/zeq/zeqa_D0990050.djhtm",
        "https://fubon-ebrokerdj.fbs.com.tw/z/ze/zeq/zeqa_D0160190.djhtm",
    ]

    # Initialize data list to store results
    data = []
    for url in urls:
        title, content = scrape_fields(url)
        today_date = datetime.now().strftime("%Y-%m-%d")
        data.append([today_date, title, content])

    # Save data to CSV
    save_to_csv(data)
