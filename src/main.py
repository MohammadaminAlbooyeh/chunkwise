from turtle import pd
import numpy as np
import pandas as np
import matplotlib.pyplot as plt


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





# Basic data statistics
print(data.describe())

#Scraping HTML table data
url = 'https://example.com/data-table'
tables = pd.read_html(url)
data = tables[0]
print(data.head())

# Data visualization
plt.figure(figsize=(10, 6))
plt.hist(data['column_name'], bins=30, alpha=0.7, color='blue')
plt.title('Distribution of Column Name')
plt.xlabel('Column Name')
plt.ylabel('Frequency')
plt.grid(axis='y', alpha=0.75)
plt.show()

# Correlation matrix
correlation_matrix = data.corr()
print(correlation_matrix)

# Scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(data['column_x'], data['column_y'], alpha=0.5)
plt.title('Scatter Plot of Column X vs Column Y')
plt.xlabel('Column X')
plt.ylabel('Column Y')
plt.grid()
plt.show()

# Save cleaned data to a new CSV file
data.to_csv('cleaned_data.csv', index=False)
print("Cleaned data saved to 'cleaned_data.csv'")

# Save cleaned data to a new Excel file
data.to_excel('cleaned_data.xlsx', index=False)
print("Cleaned data saved to 'cleaned_data.xlsx'")

# Advanced visualization - Box plot
plt.figure(figsize=(10, 6))
plt.boxplot([data['column_a'], data['column_b']], labels=['Column A', 'Column B'])
plt.title('Box Plot of Column A and Column B')
plt.ylabel('Values')
plt.grid()
plt.show()

