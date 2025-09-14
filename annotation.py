import pandas as pd

# Performing Data Anotation for three core categories
# 1. skill_category 
# 2. exprience_level
# 3. job type


# Defining categories with thier values/keywords

# Skills Category
skill_keywords = {
            'Frontend': [
                'react', 'angular', 'vue', 'javascript', 'typescript', 'html', 'css', 
                'jquery', 'bootstrap', 'sass', 'webpack', 'frontend', 'front-end',
                'ui', 'user interface', 'responsive design'
            ],
            'Backend': [
                'java', 'python', 'node.js', 'nodejs', 'spring', 'django', 'flask',
                'express', 'c#', 'php', '.net', 'ruby', 'go', 'scala', 'kotlin',
                'backend', 'back-end', 'server-side', 'api', 'microservices'
            ],
            'Full-Stack': [
                'full stack', 'full-stack', 'fullstack', 'mean', 'mern', 'lamp',
                'full stack developer', 'end-to-end', 'frontend and backend'
            ],
            'DevOps': [
                'devops', 'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins',
                'terraform', 'ansible', 'chef', 'puppet', 'ci/cd', 'deployment',
                'infrastructure', 'cloud', 'linux', 'unix'
            ],
            'Data Science': [
                'data science', 'machine learning', 'ai', 'artificial intelligence',
                'deep learning', 'python', 'r', 'tensorflow', 'pytorch', 'pandas',
                'numpy', 'data analyst', 'data engineer', 'big data', 'spark'
            ],
            'Mobile': [
                'android', 'ios', 'mobile', 'react native', 'flutter', 'swift',
                'kotlin', 'xamarin', 'mobile app', 'app development'
            ],
            'QA/Testing': [
                'testing', 'qa', 'quality assurance', 'test automation', 'selenium',
                'test engineer', 'manual testing', 'automated testing', 'cypress'
            ]
}

# Experience Level
experience_patterns = {
    'Fresher': [
        '0 - 1 years',
        '0 - 2 years',
        '1 - 2 years',
        'fresher',
        'trainee',
        'graduate'
    ],
    'Junior': [
        '1 - 3 years',
        '1 - 4 years',
        '2 - 4 years',
        '2 - 5 years',
        'junior',
        'associate'
    ],
    'Mid-Level': [
        '3 - 5 years',
        '3 - 6 years',
        '3 - 8 years',
        '2 - 6 years',
        '2 - 7 years',
        'mid level'
    ],
    'Senior': [
        '5 - 7 years',
        '5 - 8 years',
        '5 - 9 years',
        '5 - 10 years',
        'senior',
        'lead'
    ],
    'Expert': [
        '8+ years',
        '9+ years',
        '10+ years',
        'architect',
        'principal'
    ]
}


def clean_text(text):
        if pd.isna(text):
            return ""
        return str(text).lower()

# Anotating the skills based on the job_title and skills 
def anotate_skills_category(row):

    # Using the combination of the skills job title and some lines from the job desciption to determine the skills category
    job_title = clean_text(row.get('job_title', ''))
    skills = clean_text(row.get('skills', ''))
    description =clean_text(row.get('job_description', ''))[:500]  # First 500 chars

    combined_text = f"{job_title} {skills} {description}"

    # Scoring each category for skills
    category_scores = {}

    for category, keywords in skill_keywords.items():
        score = 0
        for keyword in keywords:
            keyword_lower = keyword.lower()
            
            # Giving more weightage to the job title for deciding the skills_category
            if keyword_lower in job_title:
                score += 5
            
            # Medium weight for skills matches
            if keyword_lower in skills:
                score += 3
            
            # Lower weight for the job description
            if keyword_lower in description:
                score += 1

        category_scores[category] = score
        
    # Whichever category has the max score will be considered as a final category.
    if max(category_scores.values()) > 0:
        return max(category_scores, key=category_scores.get)
    else:
        return 'General Software'


def anotate_experience_level(row):
    text = clean_text(row.get("experience",""))
    for level, category in experience_patterns.items():
        for p in category:
            if p in text:
                return level
            
    return "Unknown"

def anotate_job_type(text):
    # Now, based on the job title and job description we'll decide the category of the job
    text = clean_text(text)
    
    # Using rules to determine the job category
    if "intern " in text or " internship " in text or " apprentice " in text:
        return "Internship"
    elif "part-time" in text or "part time" in text:
        return "Part-time"
    elif "work from home" in text or "wfh" in text:
        return "Remote" 
    elif "freelance" in text:
        return "Freelance"
    else:
        # If we don't have any keywords in the job title or description then it would be Full time job
        return "Full-time"  

def anotate_dataset(df):
    
    df["skills_category"] = df.apply(anotate_skills_category,axis=1)
    
    df["experience_level"] = df.apply(anotate_experience_level,axis=1)

    # Combining job_title and job_description to descide the job_type
    df["job_type"] = df["job_title"].astype(str) + " " + df["job_description"].astype(str)
    df["job_type"] = df["job_type"].apply(anotate_job_type)

    return df

if __name__=="__main__":
    df = pd.read_csv("./datasets/cleaned_data.csv")

    anotted_df = anotate_dataset(df)
    
    # For Starting index from 1 
    df.index+=1
    
    anotted_df.to_csv("./datasets/annoted_data.csv")

    print("Annoted Dataset is saved at ./datasets/annoted_data.csv")

