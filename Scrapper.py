from selenium import webdriver
import time
import os
import pandas as pd
import random
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc #type: ignore
from selenium.webdriver.common.keys import Keys  # Import Keys for pressing "Enter" or other keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import yaml

class Scrapper:
    
    def __init__(self) -> None:
        """
        Initializes the SimplyHired class with Chrome driver and options.
        """
        self.chrome_options = uc.ChromeOptions()
        self.chrome_options.add_argument("--start-maximized")
        self.chrome_options.add_argument(
            r"--user-data-dir=C:\Users\shaha\AppData\Local\Google\Chrome\User Data\Profile 1"
        )
        self.driver = uc.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=self.chrome_options
        )
    @staticmethod
    def random_sleep(low: float = 3.0, high: float = 5.0) -> None:
        time.sleep(random.uniform(low, high))
        
    @staticmethod 
    def natural_input( element: webdriver, text: str, clear: bool = False) -> None:
        if clear:
            element.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
        for char in text:
            element.send_keys(char)
        time.sleep(random.uniform(0.5,1))


    
    def scrape_page(self, job_elements ):
        page_data_list = []
        for i, job_element in enumerate(job_elements):
            try:
                job_element.click()
                time.sleep(7)  
                job_link_element = job_element.find_element(By.TAG_NAME, "a")
                job_link = job_link_element.get_attribute("href")

                try:
                    job_type = self.driver.find_element(By.XPATH, "//span[@data-testid='viewJobBodyJobDetailsJobType']//span[@data-testid='detailText']").text
                except Exception as e:
                    job_type = None
                    print(f"No job type for job {i + 1} ")

                try:
                    compensation = self.driver.find_element(By.XPATH, "//span[@data-testid='viewJobBodyJobCompensation']//span[@data-testid='detailText']").text
                except Exception as e:
                    compensation = None
                    print(f"No compensation for job {i + 1} ")

                try:
                    posted_time = self.driver.find_element(By.XPATH, "//span[@data-testid='viewJobBodyJobPostingTimestamp']//span[@data-testid='detailText']").text
                except Exception as e:
                    posted_time = None
                    print(f"No posted time for job {i + 1} ")

                try:
                    qualifications = self.driver.find_elements(By.XPATH, "//ul[@class='chakra-wrap__list css-19lo6pj']//li[@class='chakra-wrap__listitem css-1yp4ln']//span[@data-testid='viewJobQualificationItem']")
                    qualifications = [qualification.text for qualification in qualifications]
                except Exception as e:
                    qualifications = None
                    print(f"No qualifications for job {i + 1} ")

                try:
                    company_name_elements = self.driver.find_elements(By.XPATH, "(//span[@data-testid='detailText'])[1]")
                    company_name = company_name_elements[0].text if company_name_elements else None
                except Exception as e:
                    company_name = None
                    print(f"No company name for the job: {e}")
                try:
                    job_title_element = self.driver.find_element(By.XPATH, "//h2[@data-testid='viewJobTitle']")
                    job_title = job_title_element.text
                except Exception as e:
                    job_title = None
                    print(f"No job_title for job  ")

                job_description = self.driver.find_element(By.XPATH, "//div[@data-testid='viewJobBodyJobFullDescriptionContent']").text

                page_data = {
                    "link": job_link,
                    "company_name": company_name,
                    "job_title": job_title,
                    "desc": job_description,
                    "job_type": job_type,
                    "compensation": compensation,
                    "posted_time": posted_time,
                    "qualifications": qualifications if qualifications else [],
                    "job_description": job_description
                }

                page_data_list.append(page_data)
                print(f"Scraped job: {i + 1}")                
            except Exception as e:
                print(f"Error scraping job {i + 1}: {e}")

        return page_data_list

    def scrape_jobs_with_title(self, title):
        job_data = []
        try:
            # Navigate to SimplyHired
            self.driver.get("https://www.simplyhired.com/jobs")
            time.sleep(10)

            # Input the job title
            search_field = self.driver.find_element(By.XPATH, "//input[@name='q']")
            search_field.clear()
            self.natural_input(search_field, title)

            self.random_sleep()

            # Input the location
            location = self.driver.find_element(By.XPATH, "//input[@name='l']")
            location.send_keys(Keys.CONTROL + 'a')  # Select all text
            location.send_keys(Keys.BACKSPACE)
            location.send_keys("Remote")

            self.random_sleep()

            # Click the search button
            self.driver.find_element(By.XPATH, "(//button[@type='submit'])[2]").click()
            time.sleep(5)

            # Filter results to the last 24 hours
            self.driver.find_element(By.XPATH, "(//button[@data-testid='dropdown'])[4]").click()
            self.random_sleep()
            self.driver.find_element(By.XPATH, "(//button[@data-testid='dropdown-option'])[2]").click()
            self.random_sleep()


            pagination_links = self.driver.find_elements(By.XPATH, "//nav[@role='navigation' and @aria-label='pagination']//a[contains(@class, 'chakra-link')]")

            # Ensure output directory exists
            os.makedirs("Output", exist_ok=True)
            # Extract pagination links
            ls = ['',]
            i = 1

            # Loop through pages and scrape data
            for link in pagination_links:
                if link.text:
                    ls.append(link.get_attribute('href'))
            
            for j in ls:
                try:

                    while True:
                        try:
                            job_elements = self.driver.find_elements(By.XPATH, "//li[@class='css-0']")
                            if not job_elements:
                                print("No job elements found on the page.")
                                break

                            page_data = self.scrape_page(job_elements)
                            job_data.extend(page_data)



                        except Exception as e:
                            print(f"An error occurred: {e}")
                            break
                        break
                    try:
                        self.driver.get(ls[i])
                        i+=1
                        time.sleep(5)
                    except Exception :
                        print("All pages have been scraped: ")

                        break
                except Exception as e:
                    pass
            df = pd.DataFrame(job_data)
            df.to_csv(f"Output/{title}.csv", index=False)
        except Exception as e:
            df = pd.DataFrame(job_data)
            df.to_csv(f"Output/{title}.csv", index=False)
            
            