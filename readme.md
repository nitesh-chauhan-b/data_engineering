# 📝 Job Scraping from Naukri

## 📌 Overview
This project focuses on collecting, cleaning, and annotating job postings from the **Software Engineering domain** using the **Naukri.com platform**. The workflow involves three main steps:

1. **Data Collection (Scraping)** – Scraping job listings (title, company, experience, salary, location, description, skills).  
2. **Data Cleaning** – Removing duplicates, normalizing formats, and preparing structured datasets.  
3. **Data Annotation** – Labeling cleaned data with domain-specific attributes for further analysis.  


## ⚙️ Approach

### **Step 1: Data Scraping**
- Used **Selenium WebDriver** to search queries on Naukri and collect job listing URLs across multiple pages (user-defined).  
- For each URL, extracted:
  - `job_title`
  - `company_name`
  - `experience`
  - `salary`
  - `location`
  - `job_description`
  - `skills`
- Stored results into a raw dataset (`raw_data.csv`).



### **Step 2: Data Cleaning**
- Implemented in `cleaner.py`.  
- Main operations:
  - Removed **empty rows**.
  - Removed **duplicates** based on (`job_title + company_name`).
  - **Normalized** columns:
    - Job titles and company names → title case, stripped spaces, removed special characters.
    - Location → standardized casing and commas.
    - Job description → removed excessive spaces.
    - Skills → lowercased, cleaned, normalized with commas.

Result stored as `cleaned_data.csv`.


### **Step 3: Data Annotation**
Defined **three annotation labels**:

1. **Skill Category** → Groups like Web Development, Data Science, Cloud, etc.  
2. **Experience Level** → Based on ranges (`Fresher`, `Junior`, `Mid-Level`, `Senior`, `Expert`).  
3. **Job Type** → Tags like Full-time, Internship, Contract.  

Annotated dataset saved as `annotated_data.csv` (15–20 rows).



## 🛠️ Tools & Libraries Used
**Selenium** → For scraping dynamic content and handling JavaScript-rendered job pages.  
**BeautifulSoup** → For parsing and extracting structured text from job pages.  
**Pandas** → For cleaning, normalizing, and managing datasets.  


## 🚀 Setup Instructions

It is recommended to use a virtual environment for Python projects. Follow the steps given below:

```powershell
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```


## 🚧 Challenges Faced
- **Dynamic Page Loading**: Initially tried using the `requests` library, but Naukri served dummy HTML without job details.  
  - ✅ Solved by switching to **Selenium WebDriver** to load the full page with JavaScript execution.  
- **Normalization Complexity**: Ensuring job titles, company names, and skill sets followed consistent formatting took multiple iterations.  
- **Duplicate Handling**: Identifying duplicates required combining multiple fields (`job_title + company_name`) instead of just one column.  

