from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import requests
import pandas as pd

name = input("Enter name: ")

url_get_player_id = f"https://www.rslashfakebaseball.com/api/players/name/{name}"

# Send a GET request to the URL
response = requests.get(url_get_player_id)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON data from the response
    data = response.json()

    df = pd.DataFrame(data, index=[0])
    
    player_id = df.loc[0,"playerID"]
    print(f"Found playerID: {player_id}")
else:
    print("Failed to fetch data. Status code:", response.status_code)


url = f"https://www.rslashfakebaseball.com/api/plateappearances/pitching/MLR/{player_id}"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON data from the response
    data = response.json()

    df = pd.DataFrame(data)

    print("Found data")
else:
    print("Failed to fetch data. Status code:", response.status_code)

string_columns = df.select_dtypes(include=['object']).columns
y = df['pitch']
X = df.drop(columns=["pitch", "paID", "season", "session", "gameID", "inningID", "playNumber", "pitcherID", "hitterID"], inplace=True)
#X = df.drop(columns=["pitch"], inplace=True)
X = df.drop(columns=string_columns)

# Assuming you have a DataFrame 'df' with your data
# Separate your labels (if necessary) and features
# For this example, let's assume labels are in 'labels' and features are in 'features'

# Standardize the features (recommended for PCA)

scaler = StandardScaler()
features_standardized = scaler.fit_transform(X)

# Create a PCA model
pca = PCA()

# Fit the PCA model to your standardized features
pca.fit(features_standardized)

# Get the explained variance ratio for each component
explained_variance_ratio = pca.explained_variance_ratio_

# Get the feature names
feature_names = X.columns


# Create a DataFrame to hold the feature names and their explained variance ratio
explained_variance_df = pd.DataFrame({'Feature': feature_names, 'Explained Variance': explained_variance_ratio})

# Sort the DataFrame by explained variance in descending order
explained_variance_df = explained_variance_df.sort_values(by='Explained Variance', ascending=False)

# Print the top features explaining the most variance
print(explained_variance_df)

top_n_features = int(input("Enter how many features you want: "))  # Replace with the number of top features you want
selected_features = explained_variance_df['Feature'].head(top_n_features).to_list()

# Assuming you have a DataFrame called 'features' with all your features
selected_features_df = df[selected_features]

# Assuming you have labels in a variable 'labels'
X_train, X_test, y_train, y_test = train_test_split(selected_features_df, y, test_size=0.2, random_state=42)

param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
}

best_params_ = input("Do you want to find best params, or just go with standard? [y/n] ")

match (best_params_):
    case "y" | "Y":
        # Create the Random Forest Regressor model
        model = RandomForestRegressor(random_state=42)

        print("Finding best params, please wait - this might take several minutes")

        # Initialize the GridSearchCV with cross-validation
        grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=5, scoring='neg_mean_squared_error', verbose=1)

        # Fit the grid search to the data
        grid_search.fit(X_train, y_train)

        # Get the best parameters from the grid search
        best_params = grid_search.best_params_
        print("Best Hyperparameters:", best_params)

        # Train a Random Forest model with the best hyperparameters
        best_model = RandomForestRegressor(random_state=42, **best_params)
        best_model.fit(X_train, y_train)

        # Make predictions
        y_pred = best_model.predict(X_test)
        
        # Evaluate the model
        mse = mean_squared_error(y_test, y_pred)
        print(f"Mean Squared Error: {mse}")

        last_row_as_dataframe = pd.DataFrame(selected_features_df.iloc[-1]).T 
        predicted_next_number = best_model.predict(last_row_as_dataframe)
        print(f"Predicted Next Number: {int(predicted_next_number[0])}")    
    case _:
        # Train a Random Forest model with the best hyperparameters
        best_model = RandomForestRegressor(random_state=42, n_estimators=100, min_samples_split=5, min_samples_leaf=2, max_depth=None)
        best_model.fit(X_train, y_train)

        # Make predictions
        y_pred = best_model.predict(X_test)
        
        # Evaluate the model
        mse = mean_squared_error(y_test, y_pred)
        print(f"Mean Squared Error: {mse}")

        last_row_as_dataframe = pd.DataFrame(selected_features_df.iloc[-1]).T 
        predicted_next_number = best_model.predict(last_row_as_dataframe)
        print(f"Predicted Next Number: {int(predicted_next_number[0])}")
     


