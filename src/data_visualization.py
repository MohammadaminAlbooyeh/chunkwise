

# ========= Data Visualization ==========
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

# Advanced visualization - Box plot
plt.figure(figsize=(10, 6))
plt.boxplot([data['column_a'], data['column_b']], labels=['Column A', 'Column B'])
plt.title('Box Plot of Column A and Column B')
plt.ylabel('Values')
plt.grid()
plt.show()