import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

#Loads the dataset
file_path = 'data/QB.csv'
data = pd.read_csv(file_path)

#Reformat the data to include relevant columns and fill in missing data
relevant_columns = [
    'name', 'year', 'age', 'team_name_abbr', 'pass_cmp', 
    'pass_att', 'pass_yds', 'pass_td', 'pass_int', 
    'qbr', 'games'
]
data = data[relevant_columns]
data = data.dropna()

# Create imitated weekly average statistics
data['weekly_pass_yds'] = data['pass_yds'] / data['games']
data['weekly_pass_cmp'] = data['pass_cmp'] / data['games']
data['weekly_pass_att'] = data['pass_att'] / data['games']
data['weekly_pass_td'] = data['pass_td'] / data['games']
data['weekly_pass_int'] = data['pass_int'] / data['games']

# Features: weekly completions, attempts, touchdowns, interceptions, QB rating
features = ['weekly_pass_cmp', 'weekly_pass_att', 'weekly_pass_td', 'weekly_pass_int', 'qbr']

X = data[features]
y = data['weekly_pass_yds'] 

# Split the data: 80% training, 20% testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Initialize the Linear Regression model
model = LinearRegression()

# Train the model on the training data
model.fit(X_train, y_train)

# Predict on the testing set
y_pred = model.predict(X_test)

# Calculate performance metrics
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)


print(f"\nModel Performance on Test Set:")
print(f"Mean Squared Error (MSE): {mse:.2f}")
print(f"R² Score: {r2:.2f}")