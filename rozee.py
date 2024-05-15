import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tkinter as tk
from tkinter import messagebox
import threading
import time
import re
import os

def scrape_jobs(job_title, locations, update_status):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument(f"user-agent={user_agent}")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)

    job_data = []

    
    base_url = f"https://rozee.pk/job/jsearch/q/{{job_title}}"
    url = base_url.format(job_title=job_title)

    try:
        driver.get(url)
        timeout = 10
        WebDriverWait(driver, timeout).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'job')]"))
        )

        # Define the XPath expressions for the job elements
        job_elements_xpath = '//div[@class="job "]'

        # Find all job elements
        job_elements = driver.find_elements(By.XPATH, job_elements_xpath)
        salary_range = 'Not Defined!'
        posted_date = 'Not Defined!'
        experience = 'Not Defined!'
        company_name = 'Not Defined!'
        job_location = 'Not Defined!'
        posted_date = 'Not Defined!'
        job_description = 'Not Defined!'
        # Iterate over each job element
        for job_element in job_elements:
            # Title
            try:
                title_element = job_element.find_element(By.XPATH, './/h3/a/bdi')
                job_title_text = title_element.text
                
                # Company and Location
                company_location_element = job_element.find_element(By.XPATH, './/div[@class="cname "]/bdi/a')
                company_name = company_location_element.text
                job_location = company_location_element.find_element(By.XPATH, './following-sibling::a[1]').text
                
                # Salary (if available)
                try:
                    salary_element = job_element.find_element(By.XPATH, './/span[@class="sal rz-salary"]')
                    salary_range = salary_element.text.split(': ')[-1]  
                except Exception as e:
                    salary_range = "Not specified"
                
                # Date
                date_element = job_element.find_element(By.XPATH, './/span[@title="Posted On"]')
                posted_date = date_element.text
                
                # Experience
                experience_element = job_element.find_element(By.XPATH, './/span[@class="func-area-drn"]')
                experience = experience_element.text
                
                # Description
                description_element = job_element.find_element(By.XPATH, './/div[@class="jbody"]/bdi')
                job_description = description_element.text
                

            except Exception as e:
                # Print errors for debugging
                print("Error fetching additional details:", str(e))

            job_data.append({
                "Company Name": company_name,
                "Location": job_location,
                "Salary Range/Type": salary_range,
                "Job Title": job_title_text,
                "Job Description": job_description,
                "Job Posted Date": posted_date,
                "From": " Rozee.pk"
            })

    except Exception as e:
        update_status(f"Error during scraping at rozee.pk")
        messagebox.showerror("Error", f"An error occurred at rozee.pk: {str(e)}")

    # Save the job data to an Excel file
    df = pd.DataFrame(job_data)
    
    # If the file exists, load existing data and append new data
    file_path = "job_listings.xlsx"
    if os.path.exists(file_path):
        existing_data = pd.read_excel(file_path, engine='openpyxl')
        df = pd.concat([existing_data, df], ignore_index=True)

    
    df.to_excel(file_path, index=False)

    # Update status and notify the user upon completion
    update_status("Data has been written to job_listings.xlsx")
    messagebox.showinfo("Success", "Data has been written to job_listings.xlsx")

    driver.quit()


# Function to start scraping in a new thread
def start_scraping():
    job_title = entry_job_title.get().strip()

    locations = ["pk", "in", "sa"]

    if not job_title:
        messagebox.showerror("Error", "Please enter a job title")
        return

    status_label.config(text="Scraping in progress...")

    threading.Thread(target=scrape_jobs, args=(job_title, locations, update_status)).start()


# Function to update status message in the GUI
def update_status(message):
    status_label.config(text=message)


# Create a simple tkinter GUI
root = tk.Tk()
root.title("Job Scraper")

tk.Label(root, text="Job Title:").pack(pady=5)
entry_job_title = tk.Entry(root, width=30)
entry_job_title.pack(pady=5)

tk.Button(root, text="Scrape Jobs", command=start_scraping).pack(pady=10)

status_label = tk.Label(root, text="")
status_label.pack(pady=5)

root.mainloop()
