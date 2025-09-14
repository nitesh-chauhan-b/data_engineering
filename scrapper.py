from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
# For waiting for page to load
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time


def get_driver():
    # Adding options to the driver 
    options = webdriver.ChromeOptions()

    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    # This removes the warnings
    options.add_argument("--log-level=3")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )

    # Creating webdriver 
    driver = webdriver.Chrome(options=options)

    return driver

def get_job_links(url,query,max_page):

    # Getting the Driver 
    driver = get_driver()

    # For waiting 
    wait = WebDriverWait(driver,10)

    # Proving URL to the driver
    driver.get(url)
    
    # Waiting for the website to load
    wait.until(EC.presence_of_element_located((By.CLASS_NAME,"suggestor-input")))

    # Searching the given query
    driver.find_element(By.CLASS_NAME,"suggestor-input").send_keys(query)
    # Clicking on the search button
    driver.find_element(By.CLASS_NAME,"qsbSubmit").click()

    # Waiting for the results to load on webpage

    job_urls = []
    for page in range(max_page+1):
        try:

            # Waiting for the page to fully load
            wait.until(EC.presence_of_element_located((By.ID,"listContainer")))
            
            if page<max_page:
                print("Scrapping page ",page+1)

            # Getting the jobs anchor tags
            job_links = driver.find_elements(By.CSS_SELECTOR,"a.title")

            # Getting links for the job_links
            for link in job_links:
                job_urls.append(link.get_attribute('href'))
            
            time.sleep(2)

            # Clicking next only when the page is not the last page 
            if page < max_page-1:
                # Clicking on the next page to get the more jobs urls
                next_btn = driver.find_element(By.XPATH,"//a[span[text()='Next']]")
                next_btn.click()
                time.sleep(2)
        except Exception as e:
            print(f"Got Error While Scrapping page no : {page+1}")
    driver.quit()

    return job_urls

def store_job_details(job_urls):
    # Loading the page with the selenium driver
    driver = get_driver()

    raw_job_data = []
    for i,url in enumerate(job_urls):
        try:  
            driver.get(url)

            # Creating a wait driver 
            wait = WebDriverWait(driver,10)
            
            print(f"Scrapping job {i+1}/{len(job_urls)} : {url}")
            
            # Waiting for the page to load
            wait.until(EC.presence_of_element_located((By.ID,"job_header")))


            # Using Beautiful Soup to Extract the details
            soup = BeautifulSoup(driver.page_source,"html.parser")
            
            # Finding the Job Header Section
            header = soup.find("section",id="job_header")
            
            # print(header)

            # Using dict to store the job data
            job_data = {"url":url}

            # Getting the Job details 
            
            # Job Title
            job_title = header.find("h1").getText()

            company_div = header.find("div",class_="styles_jd-header-comp-name__MvqAI")
            company_name =company_div.find("a").get_text(strip=True)

            # Expereince 
            experience = header.find("i",class_="ni-icon-bag").next_element.get_text(strip=True)

            # Salary if available 
            salary = header.find("i",class_="ni-icon-salary").next_element.get_text(strip=True)

            # Job Location 
            location = header.find("i",class_="ni-icon-location").next_element.get_text(strip=True)

            # Getting the job description container
            job_details = soup.find("section",class_="styles_job-desc-container__txpYf")

            # Job Description 
            job_description = job_details.find("div",class_="styles_JDC__dang-inner-html__h0K4t").get_text(strip=True,separator="\n")

            # Getting Skills container
            skills_container = job_details.find("div",class_="styles_key-skill__GIPn_")

            # Getting all the skills
            skills = [span.get_text(strip=True) for span in skills_container.find_all("span")]

            # print(job_title)
            # print(company_name)
            # print(experience)
            # print(salary)
            # print(location)
            # print(job_description)
            # print(skills)
            
            # Converting list of skills into a string
            filtered_skills = ""
            for skill in skills:
                filtered_skills = filtered_skills + f"{skill}, "

            job_data["job_title"] = job_title
            job_data["company_name"] = company_name
            job_data["experience"] = experience
            job_data["salary"] = salary
            job_data["location"] = location
            job_data["job_description"] = job_description
            job_data["skills"] = filtered_skills

            # Adding this data to the row data
            raw_job_data.append(job_data)
            # break
        except Exception as e:
            print("Got Error while scrapping : ",e)

    # Quitting the driver after scraping job details
    driver.quit()
    
    # Saving the data into the csv file
    df = pd.DataFrame(raw_job_data)
    df.to_csv("./datasets/raw_data.csv",index=False)


    print("Raw data saved to raw_data.csv")

if __name__=="__main__":

    # Using Naukari Platform for scrapping software Engineering Jobs
    url = "https://www.naukri.com/"

    # The Search Query for which scrapping will be done
    query = "Software Engineer"

    # Number of pages to scrap
    max_page =10
    
    job_post_links = get_job_links(url,query,max_page)

    # print("Jobs Links : \n",job_post_links)

    print("Total Jobs : ",len(job_post_links))

    store_job_details(job_post_links)

