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
                # Extract general information
                job_title_text = card.find_element(By.CSS_SELECTOR, "h2.jobTitle").text
                company_name = "Not Found"
                job_location = "Not Found"
                salary_range = "Not Defined"
                job_description = "Not Defined"
                posted_date = "Not Defined"

                try:
                    company_name_element = card.find_element(By.CSS_SELECTOR, '[data-testid="company-name"]')
                    company_name = company_name_element.text

                    location_element = card.find_element(By.CSS_SELECTOR, '[data-testid="text-location"]')
                    job_location = location_element.text

                    salary_range_element = card.find_element(By.CSS_SELECTOR, '[data-testid="attribute_snippet_testid"]')
                    salary_range = salary_range_element.text

                    # Find job description from underShelfFooter (with explicit wait)
                    underShelfFooter = WebDriverWait(card, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".underShelfFooter ul"))
                    )
                    description_items = underShelfFooter.find_elements(By.TAG_NAME, "li")
                    job_description = "\n".join([item.text for item in description_items])
                    
                    # Scrape posted date from the same section
                    posted_date_element = card.find_element(By.CSS_SELECTOR, ".css-qvloho")
                    posted_date = posted_date_element.text

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
                    "From": location + " Indeed"
                })

        except Exception as e:
            update_status(f"Error during scraping at {location}.indeed.com")
            messagebox.showerror("Error", f"An error occurred at {location}.indeed.com: {str(e)}")

    # Save the job data to an Excel file
    df = pd.DataFrame(job_data)
    df.to_excel("job_listings.xlsx", index=False)

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
