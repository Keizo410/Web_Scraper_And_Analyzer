# from selenium import webdriver
# from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
# import time
# import pandas as pd
# from selenium.webdriver.common.by import By
# from selenium import webdriver

# class JobDescriptionCollector:
#     def __init__(self, num_jobs, **kwargs):
#         chrome_options = webdriver.ChromeOptions()
#         chrome_options.add_argument('--no-sandbox')
#         chrome_options.add_argument('--disable-dev-shm-usage')

#         # Connect to the Selenium server in the 'chrome' container
#         self.driver = webdriver.Remote(
#             command_executor='http://chrome:4444/wd/hub',
#             options=chrome_options,
#         )

#         # self.options = webdriver.ChromeOptions()
#         # self.driver = webdriver.Chrome(options=self.options)
#         self.jobs = []
#         self.num_jobs = num_jobs
#         self.keyword = kwargs.get('keyword', '')
#         self.file_name = kwargs.get('file_name', 'job_data')
#         self.set_driver()
#         self.path_to_modal = "//div[@class='closeButtonWrapper']//button[@class='CloseButton']"
#         self.path_to_next = "//div[@class='JobsList_buttonWrapper__ticwb']//button[@class='button_Button__MlD2g button-base_Button__knLaX']"
#         self.path_to_lists = "//div[@class='JobsList_wrapper__EyUF6']//ul/li[@data-test='jobListing']"
#         self.path_to_companyName = '//div[@class="EmployerProfile_employerInfo__d8uSE EmployerProfile_employerWithLogo__E_JPs"]//h4[@class="heading_Heading__BqX5J heading_Subhead__Ip1aW"]'
#         self.path_to_jobTitle = '//h1[@class="heading_Heading__BqX5J heading_Level1__soLZs"]'
#         self.path_to_location = '//div[@class="JobDetails_location__mSg5h"]'
#         self.path_to_description = '//div[@class="JobDetails_jobDescription__uW_fK JobDetails_blurDescription__vN7nh"]'
    
#     def set_driver(self):
#         self.driver.set_window_size(1120, 1000)
    
#     def get_driver(self, url):
#         self.driver.get(url+f'/{self.keyword}')

#     def extract(self, url, verbose=False):
#         self.get_driver(url)
#         done = False

#         while len(self.jobs) < self.num_jobs and not done:
#             print("Loading the page for job for: ", len(self.jobs))

#             # 1. Close signup prompt
#             self.handle_signup_popup()

#             id = 0

#             while not done:
#                 job_cards = self.driver.find_elements(By.XPATH, self.path_to_lists)  # Use find_elements
#                 job_cards = job_cards[id:]  # Slice the list of job cards

#                 print(f"found {len(job_cards)} cards")

#                 for card in job_cards:
#                     print(f"Progress: {len(self.jobs)}/{self.num_jobs}")

#                     if len(self.jobs) >= self.num_jobs:
#                         done = True
#                         break
                    
#                     print("Still job left...so let's get it done!")
    
#                     try:
#                         # Scroll into view
#                         time.sleep(1)
#                         card.click()
#                     except ElementClickInterceptedException:
#                         self.handle_no_elements_error()
#                         time.sleep(1)
                        
#                     self.handle_signup_popup()

#                     try:
#                         company_name = self.driver.find_element(By.XPATH, self.path_to_companyName).text
#                         location = self.driver.find_element(By.XPATH, self.path_to_location).text
#                         job_title = self.driver.find_element(By.XPATH, self.path_to_jobTitle).text
#                         job_description = self.driver.find_element(By.XPATH, self.path_to_description).get_attribute("innerText")
#                     except NoSuchElementException:
#                         time.sleep(5)
#                         continue
                    
#                     if verbose:
#                         print("Job Title: {}".format(job_title))
#                         print("Job Description: {}".format(job_description[:1000]))
#                         print("Company Name: {}".format(company_name))
#                         print("Location: {}".format(location))
                    
#                     self.jobs.append({
#                         "Job Title": job_title,
#                         "Job Description": job_description,
#                         "Company Name": company_name,
#                         "Location": location
#                     })

#                     print("len of Jobs: ", len(self.jobs))

#                     id += 1
                

#                 print('should move to next page')

#                 # 2. Expand in show more jobs
#                 done = self.handle_show_more()
            
#         df = pd.DataFrame(self.jobs)
#         df.to_csv(f'{self.file_name}.csv', index=False)
#         print(f"Scraping finished. Result: {id} jobs")

#     def handle_no_elements_error(self):
#         try:
#             self.driver.find_element(By.CSS_SELECTOR, '[alt="Close"]').click() 
#         except NoSuchElementException:
#             pass

#     def handle_signup_popup(self):
#         try:
#             self.driver.find_element(By.XPATH, self.path_to_modal).click()
#             time.sleep(2)
#             print("signup popup is discarded")
#         except NoSuchElementException:
#             print("no popup detected...")
#             time.sleep(2)
#             pass
    
#     def handle_show_more(self):
#         try:
#             load_more_button = self.driver.find_element(By.XPATH, self.path_to_next)
#             load_more_button.click()
#             time.sleep(2)
#             print("show more job clicked")
#             return False
#         except NoSuchElementException:
#             print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(self.num_jobs, len(self.jobs)))
#             time.sleep(2)
#             return True
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium import webdriver

class JobDescriptionCollector:
    def __init__(self, num_jobs, **kwargs):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        # Connect to the Selenium server in the 'chrome' container
        self.driver = webdriver.Remote(
            command_executor='http://chrome:4444/wd/hub',
            options=chrome_options,
        )

        # self.options = webdriver.ChromeOptions()
        # self.driver = webdriver.Chrome(options=self.options)
        self.jobs = []
        self.num_jobs = num_jobs
        self.keyword = kwargs.get('keyword', '')
        self.file_name = kwargs.get('file_name', 'job_data')
        self.set_driver()
        self.path_to_modal = "//div[@class='closeButtonWrapper']//button[@class='CloseButton']"
        self.path_to_next = "//div[@class='JobsList_buttonWrapper__ticwb']//button[@class='button_Button__MlD2g button-base_Button__knLaX']"
        self.path_to_lists = "//div[@class='JobsList_wrapper__EyUF6']//ul/li[@data-test='jobListing']"
        self.path_to_companyName = '//div[@class="EmployerProfile_employerInfo__d8uSE EmployerProfile_employerWithLogo__E_JPs"]//h4[@class="heading_Heading__BqX5J heading_Subhead__Ip1aW"]'
        self.path_to_jobTitle = '//h1[@class="heading_Heading__BqX5J heading_Level1__soLZs"]'
        self.path_to_location = '//div[@class="JobDetails_location__mSg5h"]'
        self.path_to_description = '//div[@class="JobDetails_jobDescription__uW_fK JobDetails_blurDescription__vN7nh"]'
    
    def set_driver(self):
        self.driver.set_window_size(1120, 1000)
    
    def get_driver(self, url):
        self.driver.get(url+f'/{self.keyword}')

    def extract(self, url, verbose=False):
        self.get_driver(url)

        while len(self.jobs) < self.num_jobs:
            print("Loading the page for job for: ", len(self.jobs))

            # 1. Close signup prompt
            self.handle_signup_popup()

            # 2. Assign id to each cards for keeping the seen and unseen data
            id = 0
            
            job_cards = self.driver.find_elements(By.XPATH, self.path_to_lists)  # Use find_elements
            job_cards = job_cards[id:]  # Slice the list of job cards

            print(f"found {len(job_cards)} cards")

            for card in job_cards:
                print(f"Progress: {len(self.jobs)}/{self.num_jobs}")

                if len(self.jobs) >= self.num_jobs:
                    break
                
                print("Still job left...so let's get it done!")

                try:
                    # Scroll into view
                    time.sleep(1)
                    card.click()
                except ElementClickInterceptedException:
                    self.handle_no_elements_error()
                    time.sleep(1)
                    
                self.handle_signup_popup()

                company_name, location, job_title, job_description = self.get_card_info()
                
                if verbose:
                    self.print_card_info(company_name, location, job_title, job_description)
                
                self.append_card_info(company_name, location, job_title, job_description)

                print("len of Jobs: ", len(self.jobs))

                id += 1
            
            print('should move to next page')

            # 2. Expand in show more jobs
            done = self.handle_show_more()
            
        df = pd.DataFrame(self.jobs)
        df.to_csv(f'/output/{self.file_name}.csv', index=False)
        print(f"Scraping finished. Result: {id} jobs")

    def append_card_info(self,company_name, location, job_title, job_description):
        self.jobs.append({
                    "Job Title": job_title,
                    "Job Description": job_description,
                    "Company Name": company_name,
                    "Location": location
                })

    def print_card_info(self, company_name, location, job_title, job_description):
        print("Job Title: {}".format(job_title))
        print("Job Description: {}".format(job_description[:1000]))
        print("Company Name: {}".format(company_name))
        print("Location: {}".format(location))

    def get_card_info(self):
        try:
            company_name = self.driver.find_element(By.XPATH, self.path_to_companyName).text
            location = self.driver.find_element(By.XPATH, self.path_to_location).text
            job_title = self.driver.find_element(By.XPATH, self.path_to_jobTitle).text
            job_description = self.driver.find_element(By.XPATH, self.path_to_description).get_attribute("innerText")
            return company_name, location, job_title, job_description
        except NoSuchElementException:
            time.sleep(5)
            return None

    def handle_no_elements_error(self):
        try:
            self.driver.find_element(By.CSS_SELECTOR, '[alt="Close"]').click() 
        except NoSuchElementException:
            pass

    def handle_signup_popup(self):
        try:
            self.driver.find_element(By.XPATH, self.path_to_modal).click()
            time.sleep(2)
            print("signup popup is discarded")
        except NoSuchElementException:
            print("no popup detected...")
            time.sleep(2)
            pass
    
    def handle_show_more(self):
        try:
            load_more_button = self.driver.find_element(By.XPATH, self.path_to_next)
            load_more_button.click()
            time.sleep(2)
            print("show more job clicked")
            return False
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(self.num_jobs, len(self.jobs)))
            time.sleep(2)
            return True
