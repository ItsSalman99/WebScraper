# Importing required modules
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

# Define a function to scrape jobs from a given location and job title
def scrape_jobs(job_title, locations, update_status):
    # Set up Selenium options for headless scraping
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument(f"user-agent={user_agent}")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Create the WebDriver instance
    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Create a list to hold all job data
    job_data = []

    # Loop through each location and scrape the data
    for location in locations:
        base_url = f"https://{location}.indeed.com/jobs?q={{job_title}}"
        url = base_url.format(job_title=job_title)

        try:
            driver.get(url)
            timeout = 10
            WebDriverWait(driver, timeout).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".job_seen_beacon"))
            )

            job_cards = driver.find_elements(By.CSS_SELECTOR, ".job_seen_beacon")

            for card in job_cards:
                # Scrape details like job title, company name, location, and salary range
                job_title_text = card.find_element(By.CSS_SELECTOR, "h2.jobTitle").text
                company_name = "Not Found"
                job_location = "Not Found"
                salary_range = "Not Defined"

                try:
                    company_name_element = card.find_element(By.CSS_SELECTOR, '[data-testid="company-name"]')
                    company_name = company_name_element.text

                    location_element = card.find_element(By.CSS_SELECTOR, '[data-testid="text-location"]')
                    job_location = location_element.text

                    salary_range_element = card.find_element(By.CSS_SELECTOR, '[data-testid="attribute_snippet_testid"]')
                    salary_range = salary_range_element.text

                except Exception as e:
                    pass

                job_data.append({
                    "Company Name": company_name,
                    "Location": job_location,
                    "Salary Range": salary_range,
                    "Job Title": job_title_text,
                    "From": location + " Indeed"
                })

        except Exception as e:
            update_status(f"Error during scraping at {location}.indeed.com")
            messagebox.showerror("Error", f"An error occurred at {location}.indeed.com: {str(e)}")

    # Write all job data to an Excel file
    df = pd.DataFrame(job_data)
    df.to_excel("job_listings.xlsx", index=False)

    # Update status and notify the user upon completion
    update_status("Data has been written to job_listings.xlsx")
    messagebox.showinfo("Success", "Data has been written to job_listings.xlsx")

    driver.quit()

# Function to start scraping in a new thread
def start_scraping():
    # Get job title from the input field
    job_title = entry_job_title.get().strip()

    # Define the locations to scrape from
    locations = ["pk", "in", "sa"]

    if not job_title:
        messagebox.showerror("Error", "Please enter a job title")
        return

    status_label.config(text="Scraping in progress...")

    # Use threading to run the scraping in the background
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
