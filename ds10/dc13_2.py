import pandas as pd
import os

c_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(c_dir, 'global_freelancers_raw.csv')
df = pd.read_csv(file_path)
gender_value1 = ['F', 'f', 'FEMALE', 'female']
df['gender'] = df['gender'].replace(gender_value1, 'Female')
gender_value2 = ['m', 'M', 'male', 'MALE']
df['gender'] = df['gender'].replace(gender_value2, 'Male')  

df['years_of_experience'] = pd.to_numeric(df['years_of_experience'], errors='coerce')

df = df.fillna({
    "is_active": "Unknown"
})

df['years_of_experience'] = pd.to_numeric(df['years_of_experience'], errors='coerce').astype('Int64')
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

active_status1 = ['0', 'N', 'no']
df['is_active'] = df['is_active'].replace(active_status1, 'False')

active_status2 = ['1', 'Y', 'yes']
df['is_active'] = df['is_active'].replace(active_status2, 'True')

df['hourly_rate (USD)'] = df['hourly_rate (USD)'].astype(str).str.replace(r'[^\d.]', '', regex=True)
df['hourly_rate (USD)'] = pd.to_numeric(df['hourly_rate (USD)'], errors='coerce')

df['client_satisfaction'] = df['client_satisfaction'].astype(str).str.rstrip('%')
df['client_satisfaction'] = pd.to_numeric(df['client_satisfaction'], errors='coerce')
print(f"current column type:  {df['hourly_rate (USD)'].dtype}")
print(df['hourly_rate (USD)'].dropna().head())

df['age'] = pd.to_numeric(df['age'], errors='coerce')
df['age'] = df['age'].astype('Int64')

print(df.columns)
print("-----gender----")
print(df['gender'].unique())
print(df['gender'].value_counts())
print("----isnull----")
print(df.isnull().sum())
print("---is he active? prob no lol---")
print(df['is_active'].unique())
print(df['is_active'].value_counts())
print("---DATA TYPE---")
print(df.dtypes)
print(df['years_of_experience'].unique())
print("hourly rate ect:___")
print(df['hourly_rate (USD)'].unique())
print("-----")
print(df['rating'].unique())
print("-----------")
print(df['client_satisfaction'].unique())
print("----------")
print("missing skills:", df['primary_skill'].isnull().sum())
print("unique skills:", df['primary_skill'].unique())
print("---------")
print(df['age'].unique())
df.to_csv('cleaned_global_freelance.csv', index=False)