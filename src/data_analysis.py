# Regression analysis
import skitlearn.linear_model as lm
from sklearn.tree import DecisionTreeClassifier 
import pandas as pd

# Load dataset
data = pd.read_csv('data.csv')
X = data[['feature1', 'feature2', 'feature3']]
y = data['target']

# Create a linear regression model
model = lm.LinearRegression()
model.fit(X, y)
print("Regression coefficients:", model.coef_)
predictions = model.predict(X)
print("First 5 predictions:", predictions[:5])

# Save regression results to a new CSV file
results = pd.DataFrame({'Actual': y, 'Predicted': predictions})
results.to_csv('regression_results.csv', index=False)
print("Regression results saved to 'regression_results.csv'")

# Classification analysis
classifier = DecisionTreeClassifier()
classifier.fit(X, y)
class_predictions = classifier.predict(X)
print("First 5 classification predictions:", class_predictions[:5])

# Save classification results to a new CSV file
class_results = pd.DataFrame({'Actual': y, 'Predicted': class_predictions})
class_results.to_csv('classification_results.csv', index=False)
print("Classification results saved to 'classification_results.csv'")