import time
import os
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException

# Set up download preferences
download_dir = os.path.join(os.getcwd(), "Excel-Files")

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless=new")

prefs = {"download.default_directory": download_dir}
chrome_options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=chrome_options)

url = "https://www.emiratesline.com/our-offices/"


def reset_browser_session():
    global driver
    try:
        driver.quit()
    except:
        pass
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    return driver

try:
    driver.get(url)
    
    # Get all countries
    country_input = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "officeCountrySearch"))
    )
    country_input.send_keys("*")
    
    countries = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//ul[contains(@class, 'ui-autocomplete')]//li"))
    )
    all_countries = [c.text for c in countries]
    print(f"Found {len(all_countries)} countries to process\n")

    for country_index, country_name in enumerate(all_countries, 1):
        try:
            # Reset browser every 3 countries to prevent crashes
            if country_index % 3 == 0:
                print("Performing periodic browser reset...")
                driver = reset_browser_session()
                country_input = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.ID, "officeCountrySearch"))
                )
                country_input.send_keys("*")
            
            driver.get(url)  # Reset page
            
            # Select country
            country_input = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, "officeCountrySearch"))
            )
            country_input.send_keys("*")
            
            country_element = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, f"//li[contains(., '{country_name}')]"))
            )
            country_element.click()
            
            # Click search button
            WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
            ).click()
            
            # Navigate to Demurrage tab
            try:
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="tab-3"]'))
                ).click()
            except Exception as e:
                print(f"Skipping {country_name} - Demurrage tab not found")
                continue

            # Get all ports
            WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'select-menu')]"))
            ).click()
            
            ports = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.XPATH, "//ul[@id='portSelect']/li"))
            )
            port_names = [p.text for p in ports]
            
            for port_name in port_names:
                try:
                    # Select port
                    WebDriverWait(driver, 15).until(
                        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'select-menu')]"))
                    ).click()
                    
                    port_element = WebDriverWait(driver, 15).until(
                        EC.element_to_be_clickable((By.XPATH, f"//li[contains(., '{port_name}')]"))
                    )
                    port_element.click()
                    
                    # Expand accordion
                    WebDriverWait(driver, 15).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Detention and Demurrage charges')]"))
                    ).click()
                    
                    # Check for Excel button
                    try:
                        export_btn = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Export to Excel')]"))
                        )
                        
                        initial_files = set(os.listdir(download_dir))
                        export_btn.click()
                        
                        start_time = time.time()
                        while time.time() - start_time < 10:
                            current_files = set(os.listdir(download_dir))
                            new_files = current_files - initial_files
                            xlsx_files = [f for f in new_files if f.endswith(".xlsx")]
                            if xlsx_files:
                                safe_country = re.sub(r'[\\/*?:"<>|]', '_', country_name)
                                safe_port = re.sub(r'[\\/*?:"<>|]', '_', port_name)
                                new_name = f"{safe_country.title()}-{safe_port}.xlsx"
                                os.rename(
                                    os.path.join(download_dir, xlsx_files[0]),
                                    os.path.join(download_dir, new_name)
                                )
                                print(f"Downloaded: {new_name}")
                                break
                            time.sleep(2)
                    except:
                        print(f"No Excel for {country_name.title()}/{port_name}")
                        
                except Exception as e:
                    print(f"Error processing {port_name}: {str(e)}")
                    continue
                    
            print(f"Completed {country_name.title()} ({country_index}/{len(all_countries)})\n")
            
        except WebDriverException as e:
            print(f"Session error: {str(e)}")
            driver = reset_browser_session()
            continue

except Exception as e:
    print("Fatal error:", str(e))
finally:
    driver.quit()
    print("\nBrowser closed. Processing complete.")