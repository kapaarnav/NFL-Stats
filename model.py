import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

def preprocess_data(df):
    # Fill missing numeric values with the mean of the respective columns
    df.fillna(df.mean(numeric_only=True), inplace=True)
    
    # Define the target variable and the features
    X = df.drop(columns=['pass_yds'])
    y = df['pass_yds']

    # Remove non-numeric columns
    X = X.select_dtypes(include=[np.number])
    
    return X, y

def main(filepath):
    # Load the data
    data = pd.read_csv(filepath)
    
    # Preprocess the data
    X, y = preprocess_data(data)
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train the Linear Regression model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate performance metrics
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"Mean Squared Error: {mse}")
    print(f"R^2 Score: {r2}")
    
    # Plot the actual vs predicted values
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred, color='blue', alpha=0.5)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color='red', linewidth=2)
    plt.xlabel('Actual Passing Yards')
    plt.ylabel('Predicted Passing Yards')
    plt.title('Actual vs Predicted Passing Yards')
    plt.show()

if __name__ == '__main__':
    # Change the path to your dataset
    main('data/QB.csv')
