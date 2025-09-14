import pandas as pd

def remove_duplicates(df):

    print("Before Removing the duplicates : ",len(df))
    # Removing the duplicate job entries with the same job_title and company_name

    # Creating a new column with combination of the both and removing the duplicate data based on that column
    df["composite_key"] = df["job_title"]+"_"+df["company_name"]

    # Dropping the duplicate entries from the same company
    clean_df = df.drop_duplicates(subset=["composite_key"],keep="first")
    clean_df = clean_df.drop("composite_key",axis=1)

    print("After Removign the duplicates : ",len(clean_df))

    return clean_df

def remove_empty_rows(df):

    print("Before Removing Emptry rows : ",len(df))

    # Removing the records with empty job_title or company name
    clean_df = df.dropna(subset=["job_title","company_name"])

    # Removing the rows with white spaces in the job title or compnay name
    clean_df = clean_df[
        (df["job_title"].str.strip()!="") & 
        (df["company_name"].str.strip()!="")
    ]

    print("After Removing empty rows : ",len(clean_df))

    return clean_df


def normalize_df(df):

    # Normalizing the columns in the dataset
    
    df['url'] = df['url'].str.strip()

    df["job_title"] = (
        df["job_title"]
        .str.strip() # Removing the trailing and leading white spaces
        .str.title() # For Making it into a title case where first latter of each word is capitalized
        .str.replace(r"[^a-zA-Z0-9\s]","",regex=True) # Removing the speacial Characters 
        )

    df["company_name"] = (
        df["company_name"]
        .str.strip() # Removing the trailing and leading white spaces
        .str.title() # For Making it into a title case where first latter of each word is capitalized
        .str.replace(r"[^a-zA-Z0-9\s]","",regex=True) # Removing the speacial Characters 
        )
    
    # # Converting Experience into number from (0-1 years) to (0-1)
    # df["experience"] = (
    #     df["experience"]
    #     .str.extract(r"(\d+\s*-\s*\d+|\d+)")
    #     .apply(lambda x: f"'{x}")
    #     )

    df["location"] = (
        df["location"]
        .str.strip()
        .str.title()
        .str.replace(r"[^a-zA-Z\s]","",regex=True)
        .str.replace(",",", ")
    )

    df["job_description"] = (
        df["job_description"]
        .str.replace(r"\s+"," ",regex=True) # Removign multiple spaces with one space
        .str.strip()
    )

    df["skills"] = (
        df["skills"]
        .str.lower()
        .str.replace(r"[^a-z,\s]","",regex=True) # Removing the special characters
        .str.replace(r"\s*,\s*",", ",regex=True) # Normalizing the commas
    )

    return df



if __name__=="__main__":

    # Loading the dataset
    df = pd.read_csv("./datasets/raw_data.csv")

    # Removing the Empty Rows from dataset     
    clean_df = remove_empty_rows(df)

    # Removing the duplicate jobs from with same job_title and company_name
    clean_df = remove_duplicates(clean_df)

    # Normalizing text
    print("Nomalizing Dataset...")
    clean_df = normalize_df(clean_df)

    # Saving cleaned df
    clean_df.to_csv("./datasets/cleaned_data.csv",index=False)
    
    print("Cleaned Dataset is saved at ./datasets/cleaned_data.csv")




