import tkinter as tk
from tkinter import messagebox
import pandas as pd
import re

def extract_emails(text):
    return re.findall(r'[\w\.-]+@[\w\.-]+', text)

def compare_and_append_to_excel():
    try:
        # Load data from Excel file
        df = pd.read_excel("job_listings.xlsx")

        # Check for missing values
        print("Missing values before handling:", df.isnull().sum())

        # Handle missing values
        df.dropna(inplace=True)

        # Separate data from Indeed and Rozee
        df_inindeed = df[df['From'] == 'pk Indeed']
        df_pkindeed = df[df['From'] == 'in Indeed']
        df_saindeed = df[df['From'] == 'sa Indeed']
        df_rozee = df[df['From'] == 'Rozee.pk']

        # Compare job titles from Indeed and Rozee
        in_indeed_job_titles = set(df_inindeed['Job Title'])
        pk_indeed_job_titles = set(df_pkindeed['Job Title'])
        sa_indeed_job_titles = set(df_saindeed['Job Title'])
        rozee_job_titles = set(df_rozee['Job Title'])

        # Print common job titles
        common_job_titles_in = in_indeed_job_titles.intersection(rozee_job_titles)
        common_job_titles_pk = pk_indeed_job_titles.intersection(rozee_job_titles)
        common_job_titles_sa = sa_indeed_job_titles.intersection(rozee_job_titles)
        print("Common job titles (pk Indeed):", common_job_titles_in)
        print("Common job titles (in Indeed):", common_job_titles_pk)
        print("Common job titles (sa Indeed):", common_job_titles_sa)

        # Print job titles unique to Indeed
        indeed_unique_job_titles_in = in_indeed_job_titles - rozee_job_titles
        indeed_unique_job_titles_pk = pk_indeed_job_titles - rozee_job_titles
        indeed_unique_job_titles_sa = sa_indeed_job_titles - rozee_job_titles
        print("Job titles unique to Indeed (pk Indeed):", indeed_unique_job_titles_in)
        print("Job titles unique to Indeed (in Indeed):", indeed_unique_job_titles_pk)
        print("Job titles unique to Indeed (sa Indeed):", indeed_unique_job_titles_sa)

        # Print job titles unique to Rozee
        rozee_unique_job_titles = rozee_job_titles - in_indeed_job_titles - pk_indeed_job_titles - sa_indeed_job_titles
        print("Job titles unique to Rozee:", rozee_unique_job_titles)

        messagebox.showinfo("Success", "Comparison results computed")

        # Display the results in the UI
        display_comparison_results(common_job_titles_in, common_job_titles_pk, common_job_titles_sa,
                                    indeed_unique_job_titles_in, indeed_unique_job_titles_pk, indeed_unique_job_titles_sa,
                                    rozee_unique_job_titles)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def display_comparison_results(common_job_titles_in, common_job_titles_pk, common_job_titles_sa,
                                indeed_unique_job_titles_in, indeed_unique_job_titles_pk, indeed_unique_job_titles_sa,
                                rozee_unique_job_titles):
    root = tk.Tk()
    root.title("Job Details Comparison Results")
    root.minsize(1000, 1000)

    # Create frames to contain each Listbox and its title
    frame_common_in = tk.Frame(root)
    frame_common_pk = tk.Frame(root)
    frame_common_sa = tk.Frame(root)
    frame_in_unique_in = tk.Frame(root)
    frame_in_unique_pk = tk.Frame(root)
    frame_in_unique_sa = tk.Frame(root)
    frame_rozee_unique = tk.Frame(root)

    # Title labels
    label_common_in = tk.Label(frame_common_in, text="Common Job Titles (pk Indeed):")
    label_common_pk = tk.Label(frame_common_pk, text="Common Job Titles (in Indeed):")
    label_common_sa = tk.Label(frame_common_sa, text="Common Job Titles (sa Indeed):")
    label_in_unique_in = tk.Label(frame_in_unique_in, text="Job Titles Unique to Indeed (pk Indeed):")
    label_in_unique_pk = tk.Label(frame_in_unique_pk, text="Job Titles Unique to Indeed (in Indeed):")
    label_in_unique_sa = tk.Label(frame_in_unique_sa, text="Job Titles Unique to Indeed (sa Indeed):")
    label_rozee_unique = tk.Label(frame_rozee_unique, text="Job Titles Unique to Rozee:")

    # Configure titles
    label_common_in.pack(side=tk.TOP, padx=5, pady=5)
    label_common_pk.pack(side=tk.TOP, padx=5, pady=5)
    label_common_sa.pack(side=tk.TOP, padx=5, pady=5)
    label_in_unique_in.pack(side=tk.TOP, padx=5, pady=5)
    label_in_unique_pk.pack(side=tk.TOP, padx=5, pady=5)
    label_in_unique_sa.pack(side=tk.TOP, padx=5, pady=5)
    label_rozee_unique.pack(side=tk.TOP, padx=5, pady=5)

    # Configure Listbox inside each frame
    listbox_common_in = tk.Listbox(frame_common_in)
    listbox_common_pk = tk.Listbox(frame_common_pk)
    listbox_common_sa = tk.Listbox(frame_common_sa)
    listbox_in_unique_in = tk.Listbox(frame_in_unique_in)
    listbox_in_unique_pk = tk.Listbox(frame_in_unique_pk)
    listbox_in_unique_sa = tk.Listbox(frame_in_unique_sa)
    listbox_rozee_unique = tk.Listbox(frame_rozee_unique)

    # Insert data into Listbox
    for job_title in common_job_titles_in:
        listbox_common_in.insert(tk.END, job_title)
    for job_title in common_job_titles_pk:
        listbox_common_pk.insert(tk.END, job_title)
    for job_title in common_job_titles_sa:
        listbox_common_sa.insert(tk.END, job_title)
    for job_title in indeed_unique_job_titles_in:
        listbox_in_unique_in.insert(tk.END, job_title)
    for job_title in indeed_unique_job_titles_pk:
        listbox_in_unique_pk.insert(tk.END, job_title)
    for job_title in indeed_unique_job_titles_sa:
        listbox_in_unique_sa.insert(tk.END, job_title)
    for job_title in rozee_unique_job_titles:
        listbox_rozee_unique.insert(tk.END, job_title)

    # Create Scrollbars
    scrollbar_common_in = tk.Scrollbar(frame_common_in, orient=tk.VERTICAL, command=listbox_common_in.yview)
    scrollbar_common_pk = tk.Scrollbar(frame_common_pk, orient=tk.VERTICAL, command=listbox_common_pk.yview)
    scrollbar_common_sa = tk.Scrollbar(frame_common_sa, orient=tk.VERTICAL, command=listbox_common_sa.yview)
    scrollbar_in_unique_in = tk.Scrollbar(frame_in_unique_in, orient=tk.VERTICAL, command=listbox_in_unique_in.yview)
    scrollbar_in_unique_pk = tk.Scrollbar(frame_in_unique_pk, orient=tk.VERTICAL, command=listbox_in_unique_pk.yview)
    scrollbar_in_unique_sa = tk.Scrollbar(frame_in_unique_sa, orient=tk.VERTICAL, command=listbox_in_unique_sa.yview)
    scrollbar_rozee_unique = tk.Scrollbar(frame_rozee_unique, orient=tk.VERTICAL, command=listbox_rozee_unique.yview)

    # Configure Listbox to use scrollbar
    listbox_common_in.config(yscrollcommand=scrollbar_common_in.set)
    listbox_common_pk.config(yscrollcommand=scrollbar_common_pk.set)
    listbox_common_sa.config(yscrollcommand=scrollbar_common_sa.set)
    listbox_in_unique_in.config(yscrollcommand=scrollbar_in_unique_in.set)
    listbox_in_unique_pk.config(yscrollcommand=scrollbar_in_unique_pk.set)
    listbox_in_unique_sa.config(yscrollcommand=scrollbar_in_unique_sa.set)
    listbox_rozee_unique.config(yscrollcommand=scrollbar_rozee_unique.set)

    # Pack Listbox and Scrollbar widgets
    listbox_common_in.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar_common_in.pack(side=tk.RIGHT, fill=tk.Y)
    listbox_common_pk.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar_common_pk.pack(side=tk.RIGHT, fill=tk.Y)
    listbox_common_sa.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar_common_sa.pack(side=tk.RIGHT, fill=tk.Y)
    listbox_in_unique_in.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar_in_unique_in.pack(side=tk.RIGHT, fill=tk.Y)
    listbox_in_unique_pk.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar_in_unique_pk.pack(side=tk.RIGHT, fill=tk.Y)
    listbox_in_unique_sa.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar_in_unique_sa.pack(side=tk.RIGHT, fill=tk.Y)
    listbox_rozee_unique.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar_rozee_unique.pack(side=tk.RIGHT, fill=tk.Y)

    # Pack frames
    frame_common_in.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    frame_common_pk.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    frame_common_sa.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    frame_in_unique_in.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    frame_in_unique_pk.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    frame_in_unique_sa.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    frame_rozee_unique.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    root.mainloop()

# GUI
root = tk.Tk()
root.title("Job Details Comparison")

compare_button = tk.Button(root, text="Compare and Display Results", command=compare_and_append_to_excel)
compare_button.pack(pady=10)

root.mainloop()
