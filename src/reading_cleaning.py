from turtle import pd
import numpy as np
import pandas as np
import matplotlib.pyplot as plt


# ========= Data Reading and Cleaning ==========
# Reasding data from CSV file 
data = pd.read_csv('data.csv').convert_dtypes()
print(data.head())

#Reading data from Excel file
data = pd.read_excel('data.xlsx').convert_dtypes()
print(data.head())

# Cleaning data: removing duplicates
data.drop_duplicates(inplace=True)
print(f"Data shape after removing duplicates: {data.shape}")

# Handeling missing values by removing rows with any missing values
data.dropna(inplace=True)
print(f"Data shape after removing missing values: {data.shape}")

# correct invalid data types
data['column_name'] = pd.to_numeric(data['column_name'], errors='coerce')

# Fixing inconsistent data entries
data['category_column'] = data['category_column'].str.lower().str.strip()

# correcting spelling errors
data['text_column'] = data['text_column'].replace({'teh': 'the','recieve': 'receive'})

# Checking for invalid data ranges
data = data[(data['numeric_column'] >= 0) & (data['numeric_column'] <= 100)]
print(f"Data shape after fixing invalid ranges: {data.shape}")


# Save cleaned data to a new CSV file
data.to_csv('cleaned_data.csv', index=False)
print("Cleaned data saved to 'cleaned_data.csv'")

# Save cleaned data to a new Excel file
data.to_excel('cleaned_data.xlsx', index=False)
print("Cleaned data saved to 'cleaned_data.xlsx'")



