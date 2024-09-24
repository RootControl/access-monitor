import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import os
import argparse
import re


access_monitor_url = "https://accessmonitor.acessibilidade.gov.pt/"

# Change the path to your driver
chrome_driver_path = "drivers/chromedriver-mac-arm64/chromedriver"

# AccessMonitor don't allow multiple request at once
# Need a break between requests
seconds_between_requests = 7

# AccessMonitor takes a fill seconds to generate the score
seconds_to_get_result = 4

# The score page takes a fill seconds to load all contents
seconds_to_screenshot = 3


def main():
    parser = argparse.ArgumentParser(
        description="Uses AccessMonitor to get scores from websites"
    )
    parser.add_argument("xlsx", metavar="X", type=str, help="xlsx file path")
    parser.add_argument("-s", action="store_true", help="take screenshots")

    args = parser.parse_args()

    try:
        driver = setup_web_driver()
        urls = get_all_urls(args.xlsx)

        results = []
        for url in urls:
            print(f"\nProcessing {url}...")

            score = get_score(driver, url, args.s)
            results.append({"URL": url, "Score": score})

            time.sleep(seconds_between_requests)

        create_xlsx_file(results, args.xlsx)
        print("\nProcess finished")
    except Exception as e:
        print(f"Error processing: {e}")

    # Close the WebDriver
    driver.quit()


def setup_web_driver() -> webdriver:
    # Ser up Selenium options and WebDriver
    driver_options = Options()
    driver_options.add_argument("--window-size=1920,1080")
    driver_options.add_argument("--disable-infobars")
    driver_options.add_argument("--disable-popup-blocking")
    driver_options.add_argument("--disable-notifications")
    driver_options.add_argument("--disable-extensions")
    driver_options.add_argument("--disable-geolocation")
    driver_options.add_argument("--disable-notifications")
    driver_options.add_argument("--disable-browser-side-navigation")

    # Initialize the WebDriver
    return webdriver.Chrome(
        service=Service(chrome_driver_path),
        options=driver_options,
    )


def get_all_urls(file_path: str):
    if not file_path:
        raise Exception("xlsx file not found.")

    df = pd.read_excel(file_path)
    return df["URL"]


def find_score(driver: webdriver):
    return float(
        driver.find_element(By.CSS_SELECTOR, "text.ama-typography-display-6.bold").text
    )


def get_screenshot_path(url: str, directory="screenshots"):
    os.makedirs(directory, exist_ok=True)
    return os.path.join(directory, f"{extract_name(url)}.png")


def submit_request(driver: webdriver, url: str) -> None:
    # Open the AccessMonitor website
    driver.get(access_monitor_url)

    # Find the input field and submit the URL
    input_field = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "url"))
    )
    input_field.send_keys(url)

    # Submit the form
    submit_button = driver.find_element(By.ID, "btn-url")
    submit_button.click()


def get_screenshot(driver: webdriver, screenshot_path: str) -> None:
    section_element = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "section.sumary_container.bg-white")
        )
    )

    driver.execute_script("arguments[0].scrollIntoView(true);", section_element)
    time.sleep(seconds_to_screenshot)
    section_element.screenshot(screenshot_path)


def get_score(driver: webdriver, url: str, take_screenshot: bool):
    try:
        submit_request(driver, url)

        # Wait for the page to load
        time.sleep(seconds_to_get_result)

        div_error = driver.find_elements(By.CSS_SELECTOR, "div.container_error")

        if div_error:
            raise Exception("webpage not found.")

        if take_screenshot:
            screenshot_path = get_screenshot_path(url)
            get_screenshot(driver, screenshot_path)

        score = f"{find_score(driver):.1f}"
        print(f"Score: {score}")

        return score
    except Exception as e:
        print(f"Error: {e}")
        return 0


def create_xlsx_file(results: list, xlsx_file_path: str) -> None:
    # Convert results to a DataFrame
    df = pd.DataFrame(results)

    # Save the upload DataFrame back to Excel
    df.to_excel(f"New_{xlsx_file_path}", index=False)


def extract_name(url: str):
    # Define the regex pattern
    pattern = r"https?://(?:www\.)?([^/]+)(?:/([^/]+))?"

    # Match the pattern in the URL
    match = re.search(pattern, url, re.IGNORECASE)

    if match:
        domain_part = match.group(1)
        path_part = match.group(2)

        # Return the path part if it exists, otherwise the domain part
        return path_part if path_part else domain_part
    return None


if __name__ == "__main__":
    main()
