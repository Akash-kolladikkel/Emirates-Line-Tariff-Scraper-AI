import time
import os
import re
import gc

from chromedriver_py import binary_path 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException

# Configure Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--log-level=3')
chrome_options.add_argument('--disable-machine-learning')
chrome_options.add_argument("--headless=new")

# Set up download directory
download_dir = os.path.join(os.getcwd(), "Excel-Files")
# Ensure download directory exists
if not os.path.exists(download_dir):
    os.makedirs(download_dir)
    
prefs = {"download.default_directory": download_dir}
chrome_options.add_experimental_option("prefs", prefs)

# Executable filepath 
svc = webdriver.ChromeService(executable_path=binary_path)

def initialize_driver():
    """Initialize and return a new Chrome driver"""
    try:
        return webdriver.Chrome(options=chrome_options, service=svc)
    except Exception as e:
        print(f"Error initializing driver: {str(e)}")
        raise

# Initialize driver
driver = initialize_driver()
url = "https://www.emiratesline.com/our-offices/"

def process_country(country_name):
    try:
        # Select country
        country_input = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "officeCountrySearch"))
        )
        country_input.clear()
        country_input.send_keys("*")
        
        country_element = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, f"//li[contains(., '{country_name}')]"))
        )
        country_element.click()

        # Click search button
        search_btn = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
        )
        search_btn.click()

        # Navigate to Demurrage tab
        try:
            demurrage_tab = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="tab-3"]'))
            )
            demurrage_tab.click()
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Skipping {country_name} - Demurrage tab not found: {str(e)}")
            return False

        return True
    except Exception as e:
        print(f"Error processing country {country_name}: {str(e)}")
        return False

def process_port(country_name,port_name):
    try:
        # Select port
        port_menu = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'select-menu')]"))
        )
        port_menu.click()

        try:
            port_element = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, f"//li[contains(., '{port_name}')]"))
            )
            port_element.click()
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Port not found: {port_name} - {str(e)}")
            return False

        # Expand accordion
        try:
            accordion = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Detention and Demurrage charges')]"))
            )
            accordion.click()
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Accordion not found for {port_name}: {str(e)}")
            return False

        # Handle Excel download
        try:
            export_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Export to Excel')]"))
            )
            
            initial_files = set(os.listdir(download_dir))
            export_btn.click()
            
            # Wait for download
            start_time = time.time()
            while time.time() - start_time < 30:  # Increased timeout for slower connections
                current_files = set(os.listdir(download_dir))
                new_files = current_files - initial_files
                xlsx_files = [f for f in new_files if f.endswith(".xlsx")]
                if xlsx_files:
                    safe_country = re.sub(r'[\\/*?:"<>|]', '_', country_name)
                    safe_port = re.sub(r'[\\/*?:"<>|]', '_', port_name)
                    new_name = f"{safe_country.title()}-{safe_port}.xlsx"
                    
                    try:
                        os.rename(
                            os.path.join(download_dir, xlsx_files[0]),
                            os.path.join(download_dir, new_name)
                        )
                        print(f"Downloaded: {new_name}")
                        return True
                    except PermissionError:
                        print(f"File in use, waiting to rename {xlsx_files[0]}...")
                        time.sleep(2)
                    except Exception as e:
                        print(f"Error renaming file: {str(e)}")
                        return False
                time.sleep(1)
                
            print(f"Download timeout for {port_name}")
            return False
        except (TimeoutException, NoSuchElementException) as e:
            print(f"No Excel export available for {country_name}/{port_name}: {str(e)}")
            return False
            
    except Exception as e:
        print(f"Error processing port {port_name}: {str(e)}")
        return False

def main():
    global driver
    try:
        driver.get(url)
        
        # Get all countries
        try:
            country_input = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, "officeCountrySearch"))
            )
            country_input.send_keys("*")
            
            countries = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//ul[contains(@class, 'ui-autocomplete')]//li"))
            )
            all_countries = [c.text for c in countries]
            print(f"Found {len(all_countries)} countries to process\n")
        except Exception as e:
            print(f"Failed to get countries list: {str(e)}")
            return

        for country_index, country_name in enumerate(all_countries, 1):
            try:
                driver.get(url)  # Reset page
                
                if not process_country(country_name):
                    continue

                # Get all ports
                try:
                    WebDriverWait(driver, 15).until(
                        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'select-menu')]"))
                    ).click()
                    
                    ports = WebDriverWait(driver, 20).until(
                        EC.presence_of_all_elements_located((By.XPATH, "//ul[@id='portSelect']/li"))
                    )
                    port_names = [p.text for p in ports]
                    
                    for port_name in port_names:
                        process_port(country_name,port_name)
                        
                    print(f"Completed {country_name.title()} ({country_index}/{len(all_countries)})\n")
                except Exception as e:
                    print(f"Error getting ports for {country_name}: {str(e)}")
                
                # Clean up resources between countries
                gc.collect()
                
            except WebDriverException as e:
                print(f"Session error for {country_name}: {str(e)}")
                try:
                    driver.quit()
                except:
                    pass
                # Reinitialize driver
                driver = initialize_driver()
                driver.get(url)
                continue

    except Exception as e:
        print("Fatal error:", str(e))
    finally:
        try:
            driver.quit()
        except:
            pass
        print("\nBrowser closed. Processing complete.")

if __name__ == "__main__":
    main()
